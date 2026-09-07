import pandas as pd
import numpy as np
import re

def _norm_id(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    if s == "":
        return None
    m = re.search(r"\d+", s)
    if not m:
        return None
    try:
        return str(int(float(m.group(0))))
    except Exception:
        return m.group(0)

def _extract_ids_from_series(s):
    ids = set()
    if s is None:
        return ids
    for v in s.dropna().astype(str):
        for m in re.findall(r"\b\d{6,}\b", v):
            ids.add(_norm_id(m))
    return {x for x in ids if x}

# Summer term codes with financial aid year after 2001
term_frames = []
for tname in ["table_2", "table_4", "table_9"]:
    if tname in tables:
        df = tables[tname].copy()
        cols_lower = {c.lower(): c for c in df.columns}
        if "term_code" in cols_lower:
            code_col = cols_lower["term_code"]
        elif "academic_term_code" in cols_lower:
            code_col = cols_lower["academic_term_code"]
        elif "academic_terms_key" in cols_lower:
            code_col = cols_lower["academic_terms_key"]
        else:
            continue

        fay_col = cols_lower.get("financial_aid_year")
        desc_col = (
            cols_lower.get("term_description")
            or cols_lower.get("academic_term_description")
            or cols_lower.get("term_selector")
        )

        tmp = pd.DataFrame({"term_code": df[code_col]})
        tmp["financial_aid_year"] = pd.to_numeric(df[fay_col], errors="coerce") if fay_col else np.nan
        tmp["term_description"] = df[desc_col].astype(str) if desc_col else ""
        term_frames.append(tmp)

terms = pd.concat(term_frames, ignore_index=True).drop_duplicates() if term_frames else pd.DataFrame(
    columns=["term_code", "financial_aid_year", "term_description"]
)

summer_terms = terms[
    (
        terms["term_code"].astype(str).str.upper().str.endswith("SU")
        | terms["term_description"].str.contains("summer", case=False, na=False)
    )
    & (terms["financial_aid_year"] > 2001)
]
summer_term_codes = set(summer_terms["term_code"].dropna().astype(str).str.upper())

# Faculty who taught in those summer terms
summer_faculty_ids = set()

if "table_5" in tables:
    df = tables["table_5"].copy()
    if {"TERM_CODE", "responsible_faculty_mit_id"}.issubset(df.columns):
        mask = df["TERM_CODE"].astype(str).str.upper().isin(summer_term_codes)
        summer_faculty_ids |= {
            _norm_id(x) for x in df.loc[mask, "responsible_faculty_mit_id"] if _norm_id(x)
        }
    elif {"TERM_CODE", "RESPONSIBLE_FACULTY_MIT_ID"}.issubset(df.columns):
        mask = df["TERM_CODE"].astype(str).str.upper().isin(summer_term_codes)
        summer_faculty_ids |= _extract_ids_from_series(df.loc[mask, "RESPONSIBLE_FACULTY_MIT_ID"])

if "table_7" in tables:
    df = tables["table_7"].copy()
    if {"SO_TERM_CODE", "RESPONSIBLE_FACULTY_MIT_ID"}.issubset(df.columns):
        mask = df["SO_TERM_CODE"].astype(str).str.upper().isin(summer_term_codes)
        summer_faculty_ids |= _extract_ids_from_series(df.loc[mask, "RESPONSIBLE_FACULTY_MIT_ID"])

summer_faculty_ids = {x for x in summer_faculty_ids if x}

# Find and summarize email-list membership tables, if present
outputs = []

for _, df0 in tables.items():
    df = df0.copy()
    if df.empty or len(df.columns) == 0:
        continue

    cols = list(df.columns)
    lower = {c: c.lower() for c in cols}

    list_name_candidates = [
        c for c in cols
        if (
            re.search(r"(^|_)list(_|$)", lower[c])
            or "mailing" in lower[c]
            or "email_list" in lower[c]
        )
        and "name" in lower[c]
    ]
    if not list_name_candidates:
        list_name_candidates = [
            c for c in cols
            if lower[c] in {"list", "list_name", "email_list", "mailing_list"}
            or "list_name" in lower[c]
            or "mailing_list" in lower[c]
        ]
    if not list_name_candidates:
        continue

    list_col = list_name_candidates[0]

    member_candidates = [
        c for c in cols
        if lower[c] in {
            "mit_id", "member_mit_id", "person_mit_id", "person_id", "member_id",
            "email_address", "email", "member_email", "kerberos", "krb_name", "krb_name_uppercase"
        }
        or (
            any(tok in lower[c] for tok in ["member", "person", "subscriber", "recipient"])
            and any(tok in lower[c] for tok in ["mit_id", "id", "email", "kerberos", "krb"])
        )
    ]

    if not member_candidates:
        continue

    member_col = member_candidates[0]

    work = df[[list_col, member_col]].dropna(subset=[list_col, member_col]).copy()
    work["list_name"] = work[list_col].astype(str).str.strip()
    work = work[work["list_name"].str.startswith("C", case=False, na=False)]

    if work.empty:
        continue

    if "email" in lower[member_col] and not summer_faculty_ids:
        continue

    work["member_key"] = work[member_col].map(_norm_id)

    if summer_faculty_ids:
        work["is_target_faculty"] = work["member_key"].isin(summer_faculty_ids)
    else:
        faculty_flag_cols = [
            c for c in cols
            if lower[c] in {"is_faculty", "faculty_flag", "is_member_faculty"}
            or ("faculty" in lower[c] and any(tok in lower[c] for tok in ["flag", "ind", "is_"]))
        ]
        if not faculty_flag_cols:
            continue
        flag_col = faculty_flag_cols[0]
        work["is_target_faculty"] = (
            df.loc[work.index, flag_col].astype(str).str.upper().isin(["Y", "YES", "TRUE", "1"])
        )

    agg = (
        work.drop_duplicates(["list_name", "member_key"])
        .groupby("list_name", as_index=False)
        .agg(
            number_of_people_in_list=("member_key", "nunique"),
            number_of_faculty_in_list=("is_target_faculty", "sum"),
        )
    )
    agg = agg[agg["number_of_faculty_in_list"] > 0]
    outputs.append(agg)

if outputs:
    out = (
        pd.concat(outputs, ignore_index=True)
        .groupby("list_name", as_index=False)
        .agg(
            number_of_people_in_list=("number_of_people_in_list", "max"),
            number_of_faculty_in_list=("number_of_faculty_in_list", "max"),
        )
        .sort_values("list_name", kind="stable")
        .reset_index(drop=True)
    )
else:
    out = pd.DataFrame(
        columns=["list_name", "number_of_people_in_list", "number_of_faculty_in_list"]
    )

result = {"email_lists": out}
