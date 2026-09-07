import pandas as pd
import numpy as np

# Tables are preloaded in scope as: tables['table_1'], tables['table_2'], tables['table_3']
lab = tables["table_2"]

# ---- Compute borderline classification for UN (same logic as reference code) ----
un = pd.to_numeric(lab["UN"], errors="coerce")

ref_low = float(un.quantile(0.025))
ref_high = float(un.quantile(0.975))
width = ref_high - ref_low
eps = 0.05 * width if np.isfinite(width) and width > 0 else np.nan

def classify_un(x):
    if pd.isna(x):
        return "missing"
    if x < ref_low - eps:
        return "low"
    if ref_low - eps <= x < ref_low:
        return "borderline_low_outside"
    if ref_low <= x <= ref_high:
        if x <= ref_low + eps:
            return "borderline_low_inside"
        if x >= ref_high - eps:
            return "borderline_high_inside"
        return "normal"
    if ref_high < x <= ref_high + eps:
        return "borderline_high_outside"
    return "high"

lab_with_un_class = lab.copy()
lab_with_un_class["UN_class"] = un.apply(classify_un)

borderline_inside = lab_with_un_class[
    lab_with_un_class["UN_class"].isin(["borderline_low_inside", "borderline_high_inside"])
].copy()

borderline_ids = borderline_inside[["ID"]].copy()

def normalize_id_series(s: pd.Series) -> pd.Series:
    s_num = pd.to_numeric(s, errors="coerce")
    if s_num.notna().any():
        out = s_num.round().astype("Int64")
        return out.astype("string")
    return s.astype("string").str.strip()

borderline_ids["ID_key"] = normalize_id_series(borderline_ids["ID"])

# ---- Locate correct demographics source among table_1 and table_3 (same scoring as reference) ----
def find_col(df: pd.DataFrame, names):
    cols_lower = {c.lower(): c for c in df.columns}
    for n in names:
        if n in cols_lower:
            return cols_lower[n]
    return None

candidate_dfs = [
    ("table_1", tables["table_1"]),
    ("table_3", tables["table_3"]),
]

demog_best = None
demog_name_used = None
best_score = (-1, -1, -1)  # (non_null_birthday, non_null_sex, total_rows)

for name, obj in candidate_dfs:
    if not isinstance(obj, pd.DataFrame):
        continue

    id_col = find_col(obj, ["id"])
    sex_col = find_col(obj, ["sex", "gender"])
    bday_col = find_col(obj, ["birthday", "birth", "birthdate", "date_of_birth", "dob"])

    if id_col is None or sex_col is None or bday_col is None:
        continue

    non_null_sex = int(obj[sex_col].notna().sum())
    non_null_bday = int(obj[bday_col].notna().sum())
    total_rows = int(len(obj))
    score = (non_null_bday, non_null_sex, total_rows)

    if score > best_score:
        best_score = score
        demog_best = obj.copy()
        demog_name_used = name

id_col = find_col(demog_best, ["id"])
sex_col = find_col(demog_best, ["sex", "gender"])
bday_col = find_col(demog_best, ["birthday", "birth", "birthdate", "date_of_birth", "dob"])

demog_norm = pd.DataFrame(
    {
        "ID": demog_best[id_col],
        "sex": demog_best[sex_col],
        "birthday": demog_best[bday_col],
    }
)
demog_norm["ID_key"] = normalize_id_series(demog_norm["ID"])
demog_norm = demog_norm[~(demog_norm["sex"].isna() & demog_norm["birthday"].isna())].copy()

# ---- Join and output deduplicated ID, sex, birthday ----
joined = borderline_ids.merge(
    demog_norm[["ID_key", "sex", "birthday"]],
    on="ID_key",
    how="left",
)

out = (
    joined[["ID_key", "sex", "birthday"]]
    .rename(columns={"ID_key": "ID"})
    .drop_duplicates(subset=["ID"])
    .reset_index(drop=True)
)

# Final answer per guidelines
result = {"borderline_un_patient_demographics": out}