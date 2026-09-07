import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# --- Prepare IDs for joining ---
t1["ID_int"] = pd.to_numeric(t1["ID"], errors="coerce").round().astype("Int64")
t2["ID_int"] = pd.to_numeric(t2["ID"], errors="coerce").round().astype("Int64")

# --- Determine "normal anti-SM" patients from table_2 ---
sm = t2[["ID_int", "SM"]].copy()
sm["SM_norm"] = (
    sm["SM"]
    .astype("string")
    .str.strip()
    .str.strip('"')
    .str.upper()
)

normal_set = {"-", "0", "0.0", "NEG", "NEGATIVE", "N", "NORMAL"}

sm["is_normal"] = sm["SM_norm"].isin(normal_set)
sm["is_abnormal"] = sm["SM_norm"].notna() & (sm["SM_norm"] != "") & (~sm["SM_norm"].isin(normal_set))

sm_status = (
    sm.groupby("ID_int", as_index=False)
      .agg(any_normal=("is_normal", "any"),
           any_abnormal=("is_abnormal", "any"))
)
normal_ids = sm_status.loc[sm_status["any_normal"] & (~sm_status["any_abnormal"]), ["ID_int"]]

# --- Determine thrombosis status per patient from table_1 ---
th = t1[["ID_int", "Thrombosis"]].copy()
th["Thrombosis"] = pd.to_numeric(th["Thrombosis"], errors="coerce")
th_per_patient = th.groupby("ID_int", as_index=False).agg(thrombosis=("Thrombosis", "max"))

# --- Count normal anti-SM patients without thrombosis ---
merged = normal_ids.merge(th_per_patient, on="ID_int", how="inner")
count_no_thrombosis = (merged["thrombosis"] == 0).sum()

result = {
    "normal_antiSM_without_thrombosis_count": pd.DataFrame(
        {"count": [int(count_no_thrombosis)]}
    )
}
