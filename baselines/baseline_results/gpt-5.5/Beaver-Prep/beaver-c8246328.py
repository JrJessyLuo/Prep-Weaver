import pandas as pd
import numpy as np

def first_mode(s):
    s = s.dropna()
    if s.empty:
        return pd.NA
    s_str = s.astype(str).str.strip()
    s = s[s_str.ne("") & ~s_str.str.lower().isin(["nan", "none", "na", "<na>"])]
    if s.empty:
        return pd.NA
    m = s.mode(dropna=True)
    return m.iloc[0] if not m.empty else s.iloc[0]

def clean_key(s):
    return s.astype("string").str.strip().str.upper()

def count_equivalents(x):
    if pd.isna(x):
        return 0
    x = str(x).strip()
    if x == "" or x.lower() in {"nan", "none", "na", "<na>"}:
        return 0
    return len([p.strip() for p in x.split(",") if p.strip()])

# Main source: subject offerings by term with equivalent-subject information
src = tables["table_4"].copy()

term_col = "SO_TERM_CODE" if "SO_TERM_CODE" in src.columns else "TERM_CODE"
subject_col = "SO_SUBJECT_ID" if "SO_SUBJECT_ID" in src.columns else "SUBJECT_ID"

df = src.copy()
df["TERM_CODE"] = df[term_col].astype("string").str.strip()
df["SUBJECT_ID"] = df[subject_col].astype("string").str.strip()
df["DEPARTMENT_CODE"] = df["DEPARTMENT_CODE"].astype("string").str.strip()
df["DEPARTMENT"] = df["DEPARTMENT_NAME"].astype("string").str.strip()
df["DEPARTMENT"] = df["DEPARTMENT"].fillna(df["DEPARTMENT_CODE"])

df = df[df["TERM_CODE"].notna() & df["SUBJECT_ID"].notna() & df["DEPARTMENT_CODE"].notna()].copy()

df["NUM_EQUIVALENT_SUBJECTS"] = df["EQUIVALENT_SUBJECTS"].apply(count_equivalents)

# One course record per term / department / subject
course = (
    df.sort_values(["TERM_CODE", "DEPARTMENT", "SUBJECT_ID"])
      .drop_duplicates(["TERM_CODE", "DEPARTMENT_CODE", "SUBJECT_ID"], keep="first")
      .copy()
)

# Add school name from subject/department reference tables where available
course["SCHOOL_NAME"] = pd.NA

if "table_6" in tables and not tables["table_6"].empty:
    t6 = tables["table_6"].copy()
    if "SUBJECT_CODE" in course.columns and "SUBJECT_CODE" in t6.columns and "SCHOOL_NAME" in t6.columns:
        subj_school = (
            t6.assign(_SUBJECT_CODE_KEY=clean_key(t6["SUBJECT_CODE"]))
              .groupby("_SUBJECT_CODE_KEY")["SCHOOL_NAME"]
              .agg(first_mode)
        )
        course["_SUBJECT_CODE_KEY"] = clean_key(course["SUBJECT_CODE"])
        course["SCHOOL_NAME"] = course["_SUBJECT_CODE_KEY"].map(subj_school)
        course = course.drop(columns=["_SUBJECT_CODE_KEY"])

    if "DEPARTMENT_CODE" in t6.columns and "SCHOOL_NAME" in t6.columns:
        dept_school = (
            t6.assign(_DEPT_CODE_KEY=clean_key(t6["DEPARTMENT_CODE"]))
              .groupby("_DEPT_CODE_KEY")["SCHOOL_NAME"]
              .agg(first_mode)
        )
        course["_DEPT_CODE_KEY"] = clean_key(course["DEPARTMENT_CODE"])
        course["SCHOOL_NAME"] = course["SCHOOL_NAME"].combine_first(course["_DEPT_CODE_KEY"].map(dept_school))
        course = course.drop(columns=["_DEPT_CODE_KEY"])

if "table_1" in tables and not tables["table_1"].empty:
    t1 = tables["table_1"].copy()
    if {"TERM_CODE", "DEPARTMENT_CODE", "SCHOOL_NAME"}.issubset(t1.columns):
        term_dept_school = (
            t1.assign(
                _TERM=t1["TERM_CODE"].astype("string").str.strip(),
                _DEPT=clean_key(t1["DEPARTMENT_CODE"])
            )
            .groupby(["_TERM", "_DEPT"])["SCHOOL_NAME"]
            .agg(first_mode)
            .reset_index()
        )
        course["_TERM"] = course["TERM_CODE"].astype("string").str.strip()
        course["_DEPT"] = clean_key(course["DEPARTMENT_CODE"])
        course = course.merge(term_dept_school, on=["_TERM", "_DEPT"], how="left", suffixes=("", "_T1"))
        course["SCHOOL_NAME"] = course["SCHOOL_NAME"].combine_first(course["SCHOOL_NAME_T1"])
        course = course.drop(columns=["_TERM", "_DEPT", "SCHOOL_NAME_T1"])

# Add department phone number if any loaded table contains an appropriate phone column;
# otherwise the requested column is retained as missing.
course["DEPARTMENT_PHONE_NUMBER"] = pd.NA

phone_maps_code = []
phone_maps_name = []
for _, tab in tables.items():
    phone_cols = [
        c for c in tab.columns
        if "PHONE" in c.upper() or "TELEPHONE" in c.upper() or c.upper().endswith("_TEL")
    ]
    if not phone_cols:
        continue
    pcol = phone_cols[0]
    tmp = tab.copy()
    if "DEPARTMENT_CODE" in tmp.columns:
        phone_maps_code.append(
            tmp.assign(_DEPT_CODE_KEY=clean_key(tmp["DEPARTMENT_CODE"]))
               .groupby("_DEPT_CODE_KEY")[pcol]
               .agg(first_mode)
        )
    elif "DEPARTMENT" in tmp.columns:
        phone_maps_code.append(
            tmp.assign(_DEPT_CODE_KEY=clean_key(tmp["DEPARTMENT"]))
               .groupby("_DEPT_CODE_KEY")[pcol]
               .agg(first_mode)
        )
    elif "OFFER_DEPT_CODE" in tmp.columns:
        phone_maps_code.append(
            tmp.assign(_DEPT_CODE_KEY=clean_key(tmp["OFFER_DEPT_CODE"]))
               .groupby("_DEPT_CODE_KEY")[pcol]
               .agg(first_mode)
        )

    if "DEPARTMENT_NAME" in tmp.columns:
        phone_maps_name.append(
            tmp.assign(_DEPT_NAME_KEY=clean_key(tmp["DEPARTMENT_NAME"]))
               .groupby("_DEPT_NAME_KEY")[pcol]
               .agg(first_mode)
        )
    elif "OFFER_DEPT_NAME" in tmp.columns:
        phone_maps_name.append(
            tmp.assign(_DEPT_NAME_KEY=clean_key(tmp["OFFER_DEPT_NAME"]))
               .groupby("_DEPT_NAME_KEY")[pcol]
               .agg(first_mode)
        )

course["_DEPT_CODE_KEY"] = clean_key(course["DEPARTMENT_CODE"])
course["_DEPT_NAME_KEY"] = clean_key(course["DEPARTMENT"])

for mp in phone_maps_code:
    course["DEPARTMENT_PHONE_NUMBER"] = course["DEPARTMENT_PHONE_NUMBER"].combine_first(course["_DEPT_CODE_KEY"].map(mp))
for mp in phone_maps_name:
    course["DEPARTMENT_PHONE_NUMBER"] = course["DEPARTMENT_PHONE_NUMBER"].combine_first(course["_DEPT_NAME_KEY"].map(mp))

course = course.drop(columns=["_DEPT_CODE_KEY", "_DEPT_NAME_KEY"])

# Detail rows
detail = (
    course.groupby(["TERM_CODE", "DEPARTMENT_CODE", "DEPARTMENT"], dropna=False)
          .agg(
              NUMBER_OF_COURSES=("SUBJECT_ID", "size"),
              AVG_NUMBER_OF_EQUIVALENT_SUBJECTS=("NUM_EQUIVALENT_SUBJECTS", "mean"),
              SCHOOL_NAME=("SCHOOL_NAME", first_mode),
              DEPARTMENT_PHONE_NUMBER=("DEPARTMENT_PHONE_NUMBER", first_mode),
          )
          .reset_index()
)
detail["TERM_DISPLAY"] = detail["TERM_CODE"]
detail["SORT_TERM"] = detail["TERM_CODE"]
detail["SORT_DEPARTMENT"] = detail["DEPARTMENT"]
detail["SORT_KIND"] = 0
detail["ROW_KIND"] = "DETAIL"

# Subtotal rows for each term
subtotal = (
    course.groupby("TERM_CODE", dropna=False)
          .agg(
              NUMBER_OF_COURSES=("SUBJECT_ID", "size"),
              AVG_NUMBER_OF_EQUIVALENT_SUBJECTS=("NUM_EQUIVALENT_SUBJECTS", "mean"),
          )
          .reset_index()
)
subtotal["DEPARTMENT_CODE"] = ""
subtotal["DEPARTMENT"] = ""
subtotal["SCHOOL_NAME"] = ""
subtotal["DEPARTMENT_PHONE_NUMBER"] = ""
subtotal["TERM_DISPLAY"] = "SUBTOTAL"
subtotal["SORT_TERM"] = subtotal["TERM_CODE"]
subtotal["SORT_DEPARTMENT"] = ""
subtotal["SORT_KIND"] = 1
subtotal["ROW_KIND"] = "SUBTOTAL"

# Grand total row
grand = pd.DataFrame([{
    "TERM_CODE": "",
    "DEPARTMENT_CODE": "",
    "DEPARTMENT": "",
    "NUMBER_OF_COURSES": len(course),
    "AVG_NUMBER_OF_EQUIVALENT_SUBJECTS": course["NUM_EQUIVALENT_SUBJECTS"].mean(),
    "SCHOOL_NAME": "",
    "DEPARTMENT_PHONE_NUMBER": "",
    "TERM_DISPLAY": "TOTAL",
    "SORT_TERM": "ZZZZZZ",
    "SORT_DEPARTMENT": "",
    "SORT_KIND": 2,
    "ROW_KIND": "TOTAL",
}])

out = pd.concat([detail, subtotal, grand], ignore_index=True, sort=False)

out = out.sort_values(
    ["SORT_TERM", "SORT_KIND", "SORT_DEPARTMENT"],
    ascending=[True, True, True],
    kind="mergesort"
).reset_index(drop=True)

out["TERM"] = out["TERM_DISPLAY"]
repeat_detail_term = (
    out["ROW_KIND"].eq("DETAIL")
    & out["SORT_TERM"].eq(out["SORT_TERM"].shift())
    & out["ROW_KIND"].shift().eq("DETAIL")
)
out.loc[repeat_detail_term, "TERM"] = ""

final_df = out[
    [
        "TERM",
        "DEPARTMENT",
        "NUMBER_OF_COURSES",
        "AVG_NUMBER_OF_EQUIVALENT_SUBJECTS",
        "SCHOOL_NAME",
        "DEPARTMENT_PHONE_NUMBER",
    ]
].reset_index(drop=True)

result = {"term_department_course_summary": final_df}
