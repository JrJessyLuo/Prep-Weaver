import re
import pandas as pd

# Inputs (already loaded)
df0 = tables["table_1"]  # bird_919a2062_input_0.pkl
df1 = tables["table_2"]  # bird_919a2062_input_1.pkl

def to_norm_str(s: pd.Series) -> pd.Series:
    s = s.astype("string")
    s = s.str.strip()
    s = s.str.replace(r"\s+", " ", regex=True)
    return s

# ----------------------------
# Derive admitted_ids from df0 (same logic as reference)
# ----------------------------
id_norm = to_norm_str(df0["ID"])

kw_patterns = [
    r"\badmission\b",
    r"\badmitted\b",
    r"\bhospitali[sz]ed\b",
    r"\binpatient\b",
    r"\bip\b",
    r"\bward\b",
    r"\bhosp\b",
    r"\b入院\b",
    r"\b入 院\b",
    r"\b入院中\b",
    r"\b入院歴\b",
    r"\b入院日\b",
    r"\b入院有無\b",
    r"\b入院区分\b",
    r"\b外来\b",
    r"\b通院\b",
]
kw_re = re.compile("|".join(kw_patterns), flags=re.IGNORECASE)

admission_row_mask = id_norm.fillna("").str.contains(kw_re, na=False)
admission_rows = df0.loc[admission_row_mask].copy()

if admission_rows.shape[0] == 0:
    df0_str = df0.apply(
        lambda col: to_norm_str(col)
        if col.dtype == "object" or str(col.dtype).startswith(("string",))
        else col.astype("string")
    )
    contains_mask = df0_str.apply(lambda col: col.fillna("").str.contains(kw_re, na=False))
    hit_rows = contains_mask.any(axis=1)
    admission_rows = df0.loc[hit_rows].copy()

value_cols = [c for c in df0.columns if c != "ID"]

chosen_row_idx = None
if admission_rows.shape[0] > 0:
    labels = to_norm_str(admission_rows["ID"]).fillna("")
    prefer = labels.str.contains(r"入院|admission|admitted|inpatient", case=False, regex=True, na=False)
    candidates = admission_rows.loc[prefer].copy()
    if candidates.shape[0] == 0:
        candidates = admission_rows.copy()
    candidates["_filled"] = candidates[value_cols].notna().sum(axis=1)
    best = candidates.sort_values("_filled", ascending=False).head(1)
    chosen_row_idx = int(best.index[0])

admission_row = df0.loc[chosen_row_idx, value_cols]
admission_str = to_norm_str(admission_row)

null_like = {"", "na", "n/a", "nan", "none", "null"}
admission_norm = admission_str.mask(admission_str.str.lower().isin(null_like), pd.NA)

pos_tokens = {
    "1", "1.0", "yes", "y", "true", "t", "+", "＋", "入院", "入院中", "有", "あり", "アリ", "admitted", "inpatient"
}
neg_tokens = {
    "0", "0.0", "no", "n", "false", "f", "-", "－", "外来", "無", "なし", "ナシ", "not admitted", "outpatient"
}

admission_lc = admission_norm.str.lower()
is_pos = admission_lc.isin({t.lower() for t in pos_tokens})
is_neg = admission_lc.isin({t.lower() for t in neg_tokens})

num = pd.to_numeric(admission_norm, errors="coerce")
is_pos = is_pos | (num.notna() & (num > 0))
is_neg = is_neg | (num.notna() & (num <= 0))

ambiguous = admission_norm.notna() & (~is_pos) & (~is_neg)
if ambiguous.mean() > 0.20:
    is_pos = is_pos | admission_lc.str.contains(r"admit|inpatient|入院|hospital", na=False)
    is_neg = is_neg | admission_lc.str.contains(r"outpatient|外来", na=False)

admitted_patient_cols = admission_norm.index[is_pos].tolist()
admitted_ids = set()
for c in admitted_patient_cols:
    admitted_ids.add(int(c))

# ----------------------------
# Identify "normal" RNP in df1 and intersect with admitted_ids (same logic as reference)
# ----------------------------
rnp_norm = to_norm_str(df1["RNP"])
rnp_norm = rnp_norm.mask(rnp_norm.str.lower().isin(null_like), pd.NA)
rnp_lc = rnp_norm.str.lower()

normal_tokens = {"-", "－", "negative", "neg", "0", "0.0", "(-)", "（-）", "陰性", "なし", "無"}
abnormal_tokens = {"+", "＋", "positive", "pos", "1", "1.0", "(+)", "（+）", "陽性", "あり", "有"}

is_normal = rnp_lc.isin({t.lower() for t in normal_tokens})
is_abnormal = rnp_lc.isin({t.lower() for t in abnormal_tokens})

rnp_num = pd.to_numeric(rnp_norm, errors="coerce")
is_normal = is_normal | (rnp_num.notna() & (rnp_num <= 0))
is_abnormal = is_abnormal | (rnp_num.notna() & (rnp_num > 0))

unclassified = rnp_norm.notna() & (~is_normal) & (~is_abnormal)
if unclassified.mean() > 0.05:
    is_normal = is_normal | rnp_lc.str.contains(r"\bneg(ative)?\b|陰性", na=False)
    is_abnormal = is_abnormal | rnp_lc.str.contains(r"\bpos(itive)?\b|陽性", na=False)

df1_normal = df1.loc[is_normal].copy()
df1_normal_ids = pd.to_numeric(df1_normal["ID"], errors="coerce").dropna().astype(int)
df1_normal_int_ids = set(df1_normal_ids.tolist())

intersection_ids = df1_normal_int_ids.intersection(admitted_ids)
answer_count = len(intersection_ids)

# Final answer table
final_df = pd.DataFrame(
    {"normal_anti_ribonuclear_protein_and_admitted_patient_count": [answer_count]}
)

result = {"answer": final_df}