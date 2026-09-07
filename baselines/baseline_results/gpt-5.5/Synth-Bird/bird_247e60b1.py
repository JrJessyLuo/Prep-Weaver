import pandas as pd
import numpy as np

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# --- SLE cohort from table_1 ---
t1["Diagnosis"] = t1["Diagnosis"].astype(str)
sle = t1[t1["Diagnosis"].str.contains(r"\bSLE\b", case=False, na=False)].copy()

# Infer DOB as first date in combined_dates (YYYY-MM-DD|...)
sle["birth_date"] = pd.to_datetime(
    sle["combined_dates"].astype(str).str.split("|", n=1, expand=True)[0].replace({"NA": np.nan}),
    errors="coerce",
)

# --- Hemoglobin normality (sex-specific) from table_2 ---
labs = t2[["ID", "HGB"]].copy()
labs["HGB"] = pd.to_numeric(labs["HGB"], errors="coerce")

sle_labs = sle[["ID", "SEX", "birth_date"]].merge(labs, on="ID", how="inner")

# Typical adult reference ranges
sle_labs["hgb_normal"] = np.where(
    sle_labs["SEX"].astype(str).str.upper().eq("M"),
    sle_labs["HGB"].between(13.5, 17.5, inclusive="both"),
    sle_labs["HGB"].between(12.0, 16.0, inclusive="both"),
)

# Keep patients with at least one normal HGB
eligible_ids = (
    sle_labs.groupby(["ID", "SEX", "birth_date"], as_index=False)["hgb_normal"]
    .any()
)
eligible_ids = eligible_ids[eligible_ids["hgb_normal"]].copy()

# Oldest = earliest birth_date
out = (
    eligible_ids.dropna(subset=["birth_date"])
    .sort_values(["birth_date", "ID"], ascending=[True, True])
    .head(1)[["ID", "SEX"]]
    .reset_index(drop=True)
)

result = {"oldest_sle_normal_hemoglobin": out}
