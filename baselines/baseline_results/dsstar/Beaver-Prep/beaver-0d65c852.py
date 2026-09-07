import pandas as pd
import re

# Helper to extract year component from TERM_CODE like '2021FA', '2022SP'
def extract_year(term_code: str):
    if pd.isna(term_code):
        return None
    m = re.match(r"^(\d{4})", str(term_code))
    return int(m.group(1)) if m else None

# Source tables from provided 'tables' dict
df_summ = tables['table_3']  # SUBJECT_OFFERED_SUMMARY.pkl
df_offered = tables['table_5']  # SUBJECT_OFFERED.pkl

# Infer current academic year from SUBJECT_OFFERED
years = df_offered["TERM_CODE"].dropna().astype(str).map(extract_year)
current_year = int(years.max())

# Valid terms for that year
valid_terms = {f"{current_year}SP", f"{current_year}FA"}

# Filter current year Spring/Fall
df_off_curr = df_offered[df_offered["TERM_CODE"].isin(valid_terms)].copy()
df_summ_curr = df_summ[df_summ["TERM_CODE"].isin(valid_terms)].copy()

# Ensure required columns exist
for c in ["RESPONSIBLE_FACULTY_NAME", "responsible_faculty_mit_id"]:
    if c not in df_off_curr.columns:
        df_off_curr[c] = pd.NA

# Aggregate distinct instructors per subject-term
group_keys = ["TERM_CODE", "SUBJECT_ID"]
def agg_instructors(g):
    names = sorted({n for n in g["RESPONSIBLE_FACULTY_NAME"].dropna().astype(str) if n.strip()})
    return pd.Series({
        "NUM_INSTRUCTORS": len(names)
    })

df_instr = df_off_curr.groupby(group_keys, as_index=False).apply(agg_instructors)
if isinstance(df_instr.index, pd.MultiIndex):
    df_instr = df_instr.reset_index(drop=True)

# Prepare subject-term level base with TOTAL_UNITS and metadata
summ_cols = [
    "TERM_CODE",
    "SUBJECT_ID",
    "SUBJECT_TITLE",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "TOTAL_UNITS",
]
present_summ_cols = [c for c in summ_cols if c in df_summ_curr.columns]
df_summ_curr_view = df_summ_curr[present_summ_cols].drop_duplicates(["TERM_CODE", "SUBJECT_ID"]).copy()

# Merge instructors count to summary
df_merged = df_summ_curr_view.merge(df_instr, on=["TERM_CODE", "SUBJECT_ID"], how="left")

# Derive course level from SUBJECT_ID (best-effort: take leading integer before any non-digit)
def course_level_from_subject_id(sid):
    if pd.isna(sid):
        return None
    s = str(sid)
    m = re.match(r"^\s*(\d+)", s)
    if not m:
        return None
    try:
        return int(m.group(1))
    except:
        return None

df_merged["COURSE_LEVEL"] = df_merged["SUBJECT_ID"].map(course_level_from_subject_id)

# Term label and description
def term_label(term_code):
    if pd.isna(term_code):
        return None
    t = str(term_code)
    if t.endswith("SP"):
        return "Spring"
    if t.endswith("FA"):
        return "Fall"
    return None

def term_description(term_code):
    if pd.isna(term_code):
        return None
    y = extract_year(term_code)
    lbl = term_label(term_code)
    if y is None or lbl is None:
        return None
    return f"{lbl} {y}"

df_merged["TERM"] = df_merged["TERM_CODE"].map(term_label)
df_merged["TERM_DESCRIPTION"] = df_merged["TERM_CODE"].map(term_description)

# Pivot instructor counts to have Fall and Spring columns per subject (same academic year)
# We need distinct instructor counts by term per subject; use TERM to split
pivot = df_merged.pivot_table(
    index=["SUBJECT_ID", "SUBJECT_TITLE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME", "TOTAL_UNITS", "COURSE_LEVEL"],
    columns="TERM",
    values="NUM_INSTRUCTORS",
    aggfunc="max"
).reset_index()

# Ensure both columns exist
if "Fall" not in pivot.columns:
    pivot["Fall"] = pd.NA
if "Spring" not in pivot.columns:
    pivot["Spring"] = pd.NA

# We also need rows per subject-term with the requested columns, including TERM and TERM_DESCRIPTION.
# The question asks for department name, school name, subject ID, subject title, course level, total units,
# the term label, term description, number of distinct instructors teaching in Fall, and in Spring.
# Merge pivoted instructor counts back to each subject-term row so each row has both Fall and Spring counts for that subject.
key_cols = ["SUBJECT_ID", "SUBJECT_TITLE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME", "TOTAL_UNITS", "COURSE_LEVEL"]
df_final = df_merged.merge(
    pivot[key_cols + ["Fall", "Spring"]],
    on=key_cols,
    how="left"
).copy()

# Select and order columns
final_cols = [
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "SUBJECT_ID",
    "SUBJECT_TITLE",
    "COURSE_LEVEL",
    "TOTAL_UNITS",
    "TERM",
    "TERM_DESCRIPTION",
    "Fall",
    "Spring",
]
answer = df_final[final_cols].sort_values(["SUBJECT_ID", "TERM"]).reset_index(drop=True)

# Assign to result dict as required
result = {"subjects_offered_fall_spring_this_year": answer}