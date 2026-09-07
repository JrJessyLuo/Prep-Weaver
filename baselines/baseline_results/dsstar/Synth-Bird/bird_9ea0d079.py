import pandas as pd
import numpy as np

# tables['table_1'] = demographics/attributes (demo)
# tables['table_2'] = lab
demo = tables["table_1"].copy()
lab = tables["table_2"].copy()

# ----------------------------
# Reproduce reference logic to infer SEX and join to lab using best key strategy
# ----------------------------
d = demo.copy()
d["attr_norm"] = d["attr"].astype(str).str.strip().str.upper()
d["val_norm"] = d["val"].astype(str).str.strip()

def pick_mode(series: pd.Series):
    s = series.dropna().astype(str).str.strip()
    s = s[s.ne("") & s.ne("nan")]
    if s.empty:
        return np.nan
    return s.value_counts().index[0]

def canon_sex(x):
    if pd.isna(x):
        return np.nan
    t = str(x).strip().upper()
    if t in {"M", "MALE", "MAN"}:
        return "M"
    if t in {"F", "FEMALE", "WOMAN"}:
        return "F"
    if t.startswith("M"):
        return "M"
    if t.startswith("F"):
        return "F"
    return t

def clean_piece(x):
    if pd.isna(x):
        return ""
    s = str(x)
    s = s.replace('"', "").replace("'", "").strip()
    s = " ".join(s.split())
    return s

def to_int64_safe(x):
    if pd.isna(x):
        return pd.NA
    s = str(x)
    digits = "".join(ch for ch in s if ch.isdigit())
    if digits == "":
        return pd.NA
    return int(digits)

demo2 = demo.copy()
demo2["prefix_clean"] = demo2["prefix"].map(clean_piece)
demo2["id_core_clean"] = demo2["id_core"].map(clean_piece)
demo2["suffix_clean"] = demo2["suffix"].map(clean_piece)
demo2["full_id_str"] = (demo2["prefix_clean"] + demo2["id_core_clean"] + demo2["suffix_clean"]).str.strip()
demo2["ID_from_id_core"] = demo2["id_core_clean"].map(to_int64_safe).astype("Int64")
demo2["ID_from_full"] = demo2["full_id_str"].map(to_int64_safe).astype("Int64")

sex_map_full = (
    demo2.loc[
        demo2["attr"].astype(str).str.strip().str.upper().isin(["SEX", "GENDER"]),
        ["id_core", "ID_from_id_core", "ID_from_full", "val"]
    ]
    .copy()
)
sex_map_full["val_norm"] = sex_map_full["val"].astype(str).str.strip()
sex_map_full = (
    sex_map_full.groupby(["id_core", "ID_from_id_core", "ID_from_full"])["val_norm"]
    .apply(pick_mode)
    .rename("SEX_demo")
    .reset_index()
)
sex_map_full["SEX_demo"] = sex_map_full["SEX_demo"].map(canon_sex)

lab2 = lab.copy()
lab2["ID_key"] = pd.to_numeric(lab2["ID"], errors="coerce").astype("Int64")

m_idcore = (
    sex_map_full.dropna(subset=["ID_from_id_core"])
    .sort_values(["id_core"])
    .drop_duplicates(subset=["ID_from_id_core"], keep="first")
    .rename(columns={"ID_from_id_core": "ID_key"})
    [["ID_key", "SEX_demo"]]
)
lab_join_idcore = lab2.merge(m_idcore, on="ID_key", how="left")
miss_idcore = int(lab_join_idcore["SEX_demo"].isna().sum())

m_full = (
    sex_map_full.dropna(subset=["ID_from_full"])
    .sort_values(["id_core"])
    .drop_duplicates(subset=["ID_from_full"], keep="first")
    .rename(columns={"ID_from_full": "ID_key"})
    [["ID_key", "SEX_demo"]]
)
lab_join_full = lab2.merge(m_full, on="ID_key", how="left")
miss_full = int(lab_join_full["SEX_demo"].isna().sum())

lab_aug = lab_join_full if miss_full < miss_idcore else lab_join_idcore

# ----------------------------
# Abnormal uric acid (UA) and male:female ratio among those patients
# ----------------------------
# Use common clinical reference ranges:
# - Male UA abnormal if < 3.4 or > 7.0 mg/dL
# - Female UA abnormal if < 2.4 or > 6.0 mg/dL
# If sex is missing, cannot apply sex-specific thresholds -> exclude.
lab_aug["UA"] = pd.to_numeric(lab_aug.get("UA"), errors="coerce")
sex = lab_aug["SEX_demo"]

abnormal_m = (sex.eq("M")) & (lab_aug["UA"].lt(3.4) | lab_aug["UA"].gt(7.0))
abnormal_f = (sex.eq("F")) & (lab_aug["UA"].lt(2.4) | lab_aug["UA"].gt(6.0))
abnormal = abnormal_m | abnormal_f

abn = lab_aug.loc[abnormal, ["ID_key", "SEX_demo"]].dropna(subset=["ID_key", "SEX_demo"])

# Patient-level counts (unique patients with any abnormal UA)
patient_sex = abn.drop_duplicates(subset=["ID_key"])[["ID_key", "SEX_demo"]]
counts = patient_sex["SEX_demo"].value_counts()

male_patients = int(counts.get("M", 0))
female_patients = int(counts.get("F", 0))
ratio_m_to_f = np.nan if female_patients == 0 else male_patients / female_patients

answer = pd.DataFrame(
    {
        "male_patients_abnormal_UA": [male_patients],
        "female_patients_abnormal_UA": [female_patients],
        "male_to_female_ratio": [ratio_m_to_f],
    }
)

result = {"male_female_ratio_abnormal_uric_acid": answer}