import pandas as pd
import numpy as np

# --- Table 1: extract Birthday per patient ID (table is in Attribute/Value rows, patient IDs are columns) ---
t1 = tables["table_1"].copy()
t1 = t1.loc[:, ~t1.columns.duplicated()]  # guard against duplicate column names

attr_row = t1.loc[t1["ID"].astype(str).str.lower().eq("attribute")].iloc[0].drop("ID")
val_row = t1.loc[t1["ID"].astype(str).str.lower().eq("value")].iloc[0].drop("ID")

meta_long = pd.DataFrame({
    "patient_id": attr_row.index.astype(str),
    "attribute": attr_row.values,
    "value": val_row.values
})

bday = meta_long.loc[meta_long["attribute"].eq("Birthday"), ["patient_id", "value"]].copy()
bday["patient_id"] = pd.to_numeric(bday["patient_id"], errors="coerce")
bday = bday.dropna(subset=["patient_id", "value"])
bday["patient_id"] = bday["patient_id"].astype("int64")
bday["Birthday"] = (
    bday["value"].astype(str)
    .str.split("|", n=1, expand=True)[0]
    .str.strip()
)
bday["Birthday"] = pd.to_datetime(bday["Birthday"], errors="coerce")
bday = bday.dropna(subset=["Birthday"])[["patient_id", "Birthday"]].drop_duplicates("patient_id")

# --- Table 2: abnormal creatinine + compute age at that lab date ---
t2 = tables["table_2"].copy()
t2["Date"] = pd.to_datetime(t2["Date"], errors="coerce")

abn = t2.loc[
    t2["CRE"].notna() & ((t2["CRE"] < 0.6) | (t2["CRE"] > 1.2)),
    ["ID", "Date", "CRE"]
].copy()

abn = abn.merge(bday, left_on="ID", right_on="patient_id", how="inner")
abn["age_years"] = (abn["Date"] - abn["Birthday"]).dt.days / 365.25

count_under_70 = abn.loc[abn["age_years"] < 70, "ID"].nunique()

result = {
    "patients_abnormal_creatinine_under_70_count": pd.DataFrame(
        {"number_of_patients": [int(count_under_70)]}
    )
}
