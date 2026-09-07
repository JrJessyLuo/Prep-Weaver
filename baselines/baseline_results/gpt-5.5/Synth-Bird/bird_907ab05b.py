import pandas as pd
import numpy as np

df1 = tables["table_1"].copy()
df3 = tables["table_3"].copy()

# --- Clean/standardize IDs and thrombosis flag in table_1 ---
df1["ID_int"] = pd.to_numeric(df1["ID"], errors="coerce").round().astype("Int64")

df1["Thrombosis_clean"] = (
    df1["Thrombosis"].astype(str)
    .str.replace('"', "", regex=False)
    .str.strip()
    .replace({"nan": np.nan, "None": np.nan, "": np.nan})
)
df1["Thrombosis_flag"] = pd.to_numeric(df1["Thrombosis_clean"], errors="coerce")

# --- Identify patients with abnormal APTT in table_3 ---
df3["ID_int"] = pd.to_numeric(df3["ID"], errors="coerce").astype("Int64")
df3["APTT_num"] = pd.to_numeric(df3["APTT"], errors="coerce")

# Define "abnormal" APTT as outside a typical reference range
abnormal_mask = df3["APTT_num"].notna() & ((df3["APTT_num"] < 25) | (df3["APTT_num"] > 35))

abnormal_ids = df3.loc[abnormal_mask, "ID_int"].dropna().unique()

# --- Count abnormal-APTT patients who do NOT have thrombosis ---
no_thrombosis_count = (
    df1.loc[df1["ID_int"].isin(abnormal_ids) & (df1["Thrombosis_flag"] == 0), "ID_int"]
    .nunique()
)

result = {
    "abnormal_aptt_no_thrombosis_count": pd.DataFrame(
        {"number_of_patients_without_thrombosis": [no_thrombosis_count]}
    )
}
