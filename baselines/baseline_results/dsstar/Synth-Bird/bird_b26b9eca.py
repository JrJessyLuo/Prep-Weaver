import pandas as pd

# Source tables from the provided `tables` dict
df0 = tables["table_1"]  # SAT distribution-like table (has NumGE1500, cds, etc.)
df1 = tables["table_2"]  # School info table (has CDSCode, School, AdmEmail1/2/3, etc.)

# 1) Recompute target school(s): row(s) with maximum NumGE1500
num_col = "NumGE1500"
df0_num = df0.copy()
df0_num[num_col] = pd.to_numeric(df0_num[num_col], errors="coerce")

max_numge1500 = df0_num[num_col].max(skipna=True)
top0 = df0_num.loc[df0_num[num_col] == max_numge1500].copy()

# 2) Normalize join keys (cast to string and zero-pad to 14 digits)
def norm14(x):
    if pd.isna(x):
        return pd.NA
    xi = int(float(x))
    return str(xi).zfill(14)

top0["cds_norm"] = top0["cds"].apply(norm14)
df1 = df1.copy()
df1["CDSCode_norm"] = df1["CDSCode"].apply(norm14)

# 3) Left join and extract School + admin email (fallback to AdmEmail2/3)
merged = top0.merge(
    df1[["CDSCode", "CDSCode_norm", "School", "AdmEmail1", "AdmEmail2", "AdmEmail3"]],
    left_on="cds_norm",
    right_on="CDSCode_norm",
    how="left",
    suffixes=("_sat", "_schoolinfo"),
)

merged["AdminEmail"] = (
    merged["AdmEmail1"]
    .combine_first(merged["AdmEmail2"])
    .combine_first(merged["AdmEmail3"])
)

answer_df = merged[["School", "AdminEmail"]].copy()

# Final answer as required
result = {"school_with_max_sat_ge1500_test_takers_admin_email": answer_df}