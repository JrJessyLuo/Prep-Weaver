import pandas as pd
import numpy as np
import re

# Tables are preloaded in `tables`
majors_long = tables["table_1"]   # bird_479e72ee_input_0.pkl
members = tables["table_2"]       # bird_479e72ee_input_1.pkl

# ---- Parse majors mapping (record_id -> school/college) ----
majors_parsed = majors_long.copy()
majors_parsed[["school", "college"]] = majors_parsed["value"].astype(str).str.split(r"\|\|", n=1, expand=True)
majors_parsed["school"] = majors_parsed["school"].where(~majors_parsed["school"].isna(), None)
majors_parsed["college"] = majors_parsed["college"].where(~majors_parsed["college"].isna(), None)

major_record_ids = set(majors_parsed["record_id"].astype(str))

# ---- Helper: locate column referencing majors_long.record_id (likely "Major" link field) ----
cols = list(members.columns)

def find_major_link_column(members_df, major_record_id_set, min_ratio=0.2):
    matches = []
    for i, c in enumerate(members_df.columns):
        s = members_df.iloc[:, i].dropna().astype(str)
        if len(s) == 0:
            continue
        ratio = s.isin(major_record_id_set).mean()
        if ratio >= min_ratio:
            matches.append((ratio, i, c, len(s)))
    matches.sort(reverse=True)
    return matches

major_matches = find_major_link_column(members, major_record_ids, min_ratio=0.2)
if not major_matches:
    raise ValueError("Could not identify a members column that references majors_long.record_id (major link field).")
major_col_i = major_matches[0][1]
major_col_name = cols[major_col_i]

# ---- Helper: infer t-shirt size column ----
TEE_TOKENS = {
    "xs", "x-small", "xsmall",
    "s", "small",
    "m", "med", "medium",
    "l", "large",
    "xl", "x-large", "xlarge",
    "xxl", "2xl", "xx-large", "2x-large",
    "xxxl", "3xl", "3x-large", "xxx-large"
}

def normalize_token(x):
    if pd.isna(x):
        return None
    t = str(x).strip().lower()
    t = re.sub(r"\s+", "", t)
    return t

def tee_score(series):
    vals = [normalize_token(v) for v in series.dropna().unique().tolist()]
    if not vals:
        return 0, 0, set()
    matched = {v for v in vals if v in TEE_TOKENS}
    return len(matched), len(vals), matched

candidate_cols = []
for i in range(members.shape[1]):
    if i == 0 or i == major_col_i:
        continue
    s = members.iloc[:, i]
    nun = s.nunique(dropna=True)
    if 2 <= nun <= 12:
        mcnt, total, matched = tee_score(s)
        if mcnt > 0:
            candidate_cols.append((mcnt, total, i, cols[i], matched))

candidate_cols.sort(reverse=True)

if not candidate_cols:
    fallback = []
    for i in range(members.shape[1]):
        if i == 0 or i == major_col_i:
            continue
        s = members.iloc[:, i].dropna().astype(str)
        if len(s) == 0:
            continue
        has_medium = s.str.contains(r"\bMedium\b", case=False, regex=True).mean()
        has_small = s.str.contains(r"\bSmall\b", case=False, regex=True).mean()
        has_large = s.str.contains(r"\bLarge\b", case=False, regex=True).mean()
        score = has_medium + has_small + has_large
        if score > 0:
            fallback.append((score, i, cols[i]))
    fallback.sort(reverse=True)
    if not fallback:
        raise ValueError("Could not infer a t-shirt size column.")
    tshirt_col_i = fallback[0][1]
else:
    candidate_cols.sort(key=lambda x: (-x[0], x[1], x[2]))
    tshirt_col_i = candidate_cols[0][2]

tshirt_col_name = cols[tshirt_col_i]

# ---- Rebuild member-level tidy DataFrame (same logic as reference code) ----
members_T = members.T.reset_index(drop=False).rename(columns={"index": "record_id"})
member_value_cols = [c for c in members_T.columns if c != "record_id"]

row_member_ids = members.iloc[:, 0].astype(str).tolist()
if len(row_member_ids) != len(member_value_cols):
    if len(member_value_cols) != members.shape[0]:
        raise ValueError(f"Unexpected shape: members.shape={members.shape}, transposed member cols={member_value_cols}")
member_col_to_member_id = {member_value_cols[i]: row_member_ids[i] for i in range(len(member_value_cols))}

long_parts = []
for mc in member_value_cols:
    tmp = members_T[["record_id", mc]].copy()
    tmp = tmp.rename(columns={mc: "value"})
    tmp["member_id"] = member_col_to_member_id[mc]
    long_parts.append(tmp)

members_long = pd.concat(long_parts, ignore_index=True)

target_record_ids = {
    "link_to_major": str(major_col_name),
    "t_shirt_size": str(tshirt_col_name),
}

members_long["field"] = members_long["record_id"].astype(str).map({v: k for k, v in target_record_ids.items()})
members_long_target = members_long.dropna(subset=["field"]).copy()

member_tidy = (
    members_long_target
    .pivot_table(index="member_id", columns="field", values="value", aggfunc="first")
    .reset_index()
)

for c in ["link_to_major", "t_shirt_size"]:
    if c not in member_tidy.columns:
        member_tidy[c] = None

member_tidy["link_to_major"] = member_tidy["link_to_major"].where(~member_tidy["link_to_major"].isna(), None).astype("object")
member_tidy["t_shirt_size"] = member_tidy["t_shirt_size"].where(~member_tidy["t_shirt_size"].isna(), None)
member_tidy.loc[member_tidy["t_shirt_size"].notna(), "t_shirt_size"] = (
    member_tidy.loc[member_tidy["t_shirt_size"].notna(), "t_shirt_size"].astype(str).str.strip()
)

def first_major_id(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    if isinstance(x, (list, tuple, set)):
        return str(next(iter(x))) if len(x) else None
    s = str(x).strip()
    if s.startswith("[") and s.endswith("]"):
        s2 = s.strip("[]").strip()
        if not s2:
            return None
        return s2.split(",")[0].strip().strip("'").strip('"')
    if "," in s:
        return s.split(",")[0].strip()
    return s

member_tidy["link_to_major"] = member_tidy["link_to_major"].apply(first_major_id)

maj_lookup = majors_parsed.set_index(majors_parsed["record_id"].astype(str))[["major_id", "school", "college"]]
member_tidy = member_tidy.join(maj_lookup, on=member_tidy["link_to_major"].astype(str))

filtered = member_tidy[
    (member_tidy["college"] == "School of Business") &
    (member_tidy["t_shirt_size"].astype(str).str.lower() == "medium")
]

count_members = int(filtered["member_id"].nunique())

answer_df = pd.DataFrame(
    {"members_of_business_with_medium_tshirt": [count_members]}
)

result = {"answer": answer_df}