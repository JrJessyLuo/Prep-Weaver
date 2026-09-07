import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Get admitted/accepted patient IDs from the transposed table_1
admission_row = t1.loc[t1["ID"].astype(str).str.strip().eq("Admission")].iloc[0]
adm_series = admission_row.drop(labels=["ID"])

admitted_cols = adm_series.fillna("").astype(str).str.startswith("+")
admitted_ids = (
    pd.to_numeric(pd.Index(adm_series.index[admitted_cols]).str.replace('"', "", regex=False), errors="coerce")
    .dropna()
    .astype(int)
    .unique()
)

# Normal WBC range (typical): 4.0 to 10.0
normal_wbc = t2["WBC"].between(4.0, 10.0, inclusive="both")

num_patients = (
    t2.loc[t2["ID"].isin(admitted_ids) & normal_wbc, "ID"]
    .dropna()
    .nunique()
)

result = {
    "admitted_patients_with_normal_wbc_count": pd.DataFrame(
        {"num_patients": [int(num_patients)]}
    )
}
