import pandas as pd

# tables dict is assumed to be already loaded and in scope:
# tables['table_1'] = bird_82d1fd8f_input_0.pkl
# tables['table_2'] = bird_82d1fd8f_input_1.pkl

df0 = tables["table_1"]
df1 = tables["table_2"]

# Extract outpatient-clinic patient IDs (Admission == '-')
outpatient_df = df0[df0["Admission"].astype(str).str.strip().eq("-")].copy()
outpatient_ids = (
    outpatient_df["ID"]
    .dropna()
    .astype("int64")
    .unique()
    .tolist()
)

# Typical adult RBC normal range (million/µL): 4.2–5.9
RBC_LOW, RBC_HIGH = 4.2, 5.9

# Find abnormal RBC IDs (outside normal range)
abnormal_rbc_ids = (
    df1.loc[df1["RBC"].notna() & ((df1["RBC"] < RBC_LOW) | (df1["RBC"] > RBC_HIGH)), "ID"]
    .dropna()
    .astype("int64")
    .unique()
    .tolist()
)

# Intersect abnormal-RBC IDs with outpatient-clinic IDs
result_ids = sorted(set(outpatient_ids).intersection(abnormal_rbc_ids))

# Final answer dataframe
answer_df = pd.DataFrame({"ID": result_ids})

# Required result object
result = {"abnormal_rbc_outpatient_ids": answer_df}