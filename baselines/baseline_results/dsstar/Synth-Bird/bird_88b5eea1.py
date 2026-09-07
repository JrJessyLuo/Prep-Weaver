import pandas as pd
import numpy as np
import re

# ----------------------------
# Load tables (already in-scope as `tables`)
# ----------------------------
df0 = tables["table_1"].copy()  # columns: ['ID','patient_id','value']
df_exam = tables["table_3"].copy()  # thrombosis_prediction_Examination.pkl

# ----------------------------
# Helpers (same logic as reference code)
# ----------------------------
def _clean_patient_id(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        s = s[1:-1]
    s = s.strip()
    m = re.fullmatch(r"\d+", s)
    return m.group(0) if m else s

def _sex_from_value(v):
    if pd.isna(v):
        return None
    s = str(v).strip().lower()

    # English tokens
    if s in {"m", "male", "man", "boy"}:
        return "M"
    if s in {"f", "female", "woman", "girl"}:
        return "F"

    # Japanese tokens
    if s in {"男", "男性"}:
        return "M"
    if s in {"女", "女性"}:
        return "F"

    # Ambiguous encodings (do not guess)
    if s in {"0", "1", "+", "-"}:
        return None

    return None

# ----------------------------
# Identify male patient_ids (reproduce reference logic)
# ----------------------------
df0["patient_id_clean"] = df0["patient_id"].map(_clean_patient_id)
df0["ID_str"] = df0["ID"].astype(str).str.strip()
df0["ID_clean"] = df0["ID_str"].str.lower()
df0["value_str"] = df0["value"].astype(str).str.strip()

sex_id_patterns = [
    r"\bsex\b",
    r"\bgender\b",
    r"\bpatient\s*sex\b",
    r"\bpatient\s*gender\b",
]
sex_mask = np.zeros(len(df0), dtype=bool)
for pat in sex_id_patterns:
    sex_mask |= df0["ID_clean"].str.contains(pat, regex=True, na=False)

id_based = df0.loc[sex_mask, ["patient_id_clean", "ID_str", "value_str"]].copy()
id_based["sex"] = id_based["value_str"].map(_sex_from_value)

token_pat = r"^(m|f|male|female|man|woman|男|女|男性|女性)$"
val_token_mask = df0["value_str"].str.lower().str.match(token_pat, na=False)
val_based = df0.loc[val_token_mask, ["patient_id_clean", "ID_str", "value_str"]].copy()
val_based["sex"] = val_based["value_str"].map(_sex_from_value)

sex_rows = pd.concat([id_based, val_based], ignore_index=True).dropna(subset=["patient_id_clean"])
sex_rows = sex_rows[sex_rows["sex"].isin(["M", "F"])].copy()
sex_id_labels = sorted(sex_rows["ID_str"].dropna().unique().tolist())

if sex_id_labels:
    exact_id_mask = df0["ID_str"].isin(sex_id_labels)
    sex_candidates = df0.loc[exact_id_mask, ["patient_id_clean", "ID_str", "value_str"]].copy()
    sex_candidates["sex"] = sex_candidates["value_str"].map(_sex_from_value)
    sex_candidates = sex_candidates[sex_candidates["sex"].isin(["M", "F"])].copy()
else:
    sex_candidates = val_based[val_based["sex"].isin(["M", "F"])].copy()

sex_by_patient = (
    sex_candidates.dropna(subset=["patient_id_clean"])
    .groupby("patient_id_clean", as_index=False)["sex"]
    .agg(lambda s: next((x for x in s if x in {"M", "F"}), None))
)

male_patient_ids = set(
    sex_by_patient.loc[sex_by_patient["sex"] == "M", "patient_id_clean"]
    .dropna()
    .astype(str)
)

# ----------------------------
# Find exam columns for WBC and fibrinogen + their normal/abnormal flags
# ----------------------------
exam = df_exam.copy()

# Patient id column detection
pid_col = None
for c in exam.columns:
    cl = str(c).strip().lower()
    if cl in {"patient_id", "patientid", "pid", "id"} or ("patient" in cl and "id" in cl):
        pid_col = c
        break
if pid_col is None:
    pid_col = exam.columns[0]  # fallback

exam["patient_id_clean"] = exam[pid_col].map(_clean_patient_id).astype(str)

# Identify WBC and fibrinogen related columns
wbc_cols = [c for c in exam.columns if re.search(r"\b(wbc|white\s*blood\s*cells?)\b", str(c).lower())]
fib_cols = [c for c in exam.columns if re.search(r"\b(fibrinogen|fib|fbg)\b", str(c).lower())]

# Prefer columns that look like interpretation/flag for normality
def _pick_flag_col(cols, keyword):
    # prioritize columns containing "judge", "flag", "status", "abnormal", "normal"
    priority = []
    for c in cols:
        cl = str(c).lower()
        score = 0
        if keyword in cl:
            score += 5
        if any(t in cl for t in ["flag", "judge", "status", "abnormal", "normal", "判定", "異常", "正常"]):
            score += 3
        if any(t in cl for t in ["value", "val", "result", "数値"]):
            score -= 1
        priority.append((score, c))
    priority.sort(reverse=True, key=lambda x: x[0])
    return priority[0][1] if priority else None

wbc_flag_col = _pick_flag_col(wbc_cols, "wbc") if wbc_cols else None
fib_flag_col = _pick_flag_col(fib_cols, "fibrinogen") if fib_cols else None
if fib_flag_col is None and fib_cols:
    fib_flag_col = _pick_flag_col(fib_cols, "fbg")

# Fallback if we only have one matched column (might still be a flag)
if wbc_flag_col is None and wbc_cols:
    wbc_flag_col = wbc_cols[0]
if fib_flag_col is None and fib_cols:
    fib_flag_col = fib_cols[0]

def _is_normal(x):
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    # common normal encodings
    if s in {"normal", "n", "0", "false", "no", "negative", "within range", "within normal limits", "w nl"}:
        return True
    if s in {"正常"}:
        return True
    # if contains "normal" but not "abnormal"
    if ("normal" in s) and ("abnormal" not in s):
        return True
    return False

def _is_abnormal(x):
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    if s in {"abnormal", "abn", "a", "1", "true", "yes", "positive", "high", "low"}:
        return True
    if s in {"異常"}:
        return True
    if "abnormal" in s:
        return True
    if any(t in s for t in ["high", "low", "elevat", "decreas"]) and "normal" not in s:
        return True
    return False

# ----------------------------
# Apply filters and compute count
# ----------------------------
# male patients
exam_male = exam[exam["patient_id_clean"].isin(male_patient_ids)].copy()

# WBC normal
if wbc_flag_col is not None:
    wbc_normal_mask = exam_male[wbc_flag_col].map(_is_normal)
else:
    wbc_normal_mask = pd.Series(False, index=exam_male.index)

exam_male_wbc_normal = exam_male.loc[wbc_normal_mask].copy()

# fibrinogen abnormal
if fib_flag_col is not None:
    fib_abn_mask = exam_male_wbc_normal[fib_flag_col].map(_is_abnormal)
else:
    fib_abn_mask = pd.Series(False, index=exam_male_wbc_normal.index)

count_abn_fib = int(fib_abn_mask.sum())

answer_df = pd.DataFrame(
    {"male_wbc_normal_and_fibrinogen_abnormal_count": [count_abn_fib]}
)

result = {"answer": answer_df}