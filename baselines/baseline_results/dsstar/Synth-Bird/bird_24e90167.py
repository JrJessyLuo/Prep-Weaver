import pandas as pd
import numpy as np

# --- Load labs table from preloaded tables dict ---
df1 = tables["table_2"].copy()

# Ensure consistent ID dtype for joining with id_to_age
df1["ID"] = pd.to_numeric(df1["ID"], errors="coerce")

# Parse CRE as numeric
df1["CRE_num"] = pd.to_numeric(df1["CRE"], errors="coerce")

# --- Define abnormal creatinine criterion ---
CRE_LOW_CUTOFF = 0.6
CRE_HIGH_CUTOFF = 1.3

df1["CRE_abnormal"] = (df1["CRE_num"] < CRE_LOW_CUTOFF) | (df1["CRE_num"] > CRE_HIGH_CUTOFF)

# Filter to abnormal CRE
abn_cre = df1.loc[df1["CRE_abnormal"] & df1["ID"].notna(), ["ID", "Date", "CRE_num"]].copy()

# --- Join with extracted ID -> age mapping (id_to_age from base code; assumed in scope) ---
age_map = id_to_age.copy()
age_map.index = pd.to_numeric(age_map.index, errors="coerce")

abn_with_age = abn_cre.merge(
    age_map.rename("age").reset_index().rename(columns={"index": "ID"}),
    on="ID",
    how="inner"
)

# Count unique patients with abnormal creatinine and age < 70
count_unique_ids_age_lt_70 = int(abn_with_age.loc[abn_with_age["age"] < 70, "ID"].nunique())

# Final answer table
answer_df = pd.DataFrame({"patients_under_70_with_abnormal_creatinine": [count_unique_ids_age_lt_70]})

result = {"answer": answer_df}