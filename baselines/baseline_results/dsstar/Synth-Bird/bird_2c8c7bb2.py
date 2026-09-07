import pandas as pd

# Source tables from the preloaded `tables` dict
demo = tables["table_1"]
labs = tables["table_2"]

# Filter to outpatients (Admission == '-')
outpatients = demo.loc[demo["Admission"].astype(str).eq("-"), ["ID", "xb", "Admission"]].copy()

# Join to labs on ID, keeping HGB for evaluation
outpatient_hgb = outpatients.merge(
    labs.loc[:, ["ID", "Date", "HGB"]].copy(),
    on="ID",
    how="inner"
)

# Ensure HGB is numeric
outpatient_hgb["HGB"] = pd.to_numeric(outpatient_hgb["HGB"], errors="coerce")

# Compute sex-specific low-HGB flag (F < 12, M < 13)
xb_upper = outpatient_hgb["xb"].astype(str).str.upper()
outpatient_hgb["low"] = (
    (xb_upper.eq("F") & outpatient_hgb["HGB"].lt(12)) |
    (xb_upper.eq("M") & outpatient_hgb["HGB"].lt(13))
)

# Final distinct ID, xb for low hemoglobin outpatients
final_df = (
    outpatient_hgb.loc[outpatient_hgb["low"], ["ID", "xb"]]
    .dropna(subset=["ID", "xb"])
    .drop_duplicates(["ID", "xb"])
    .reset_index(drop=True)
)

# Assign per guidelines
result = {"low_hgb_outpatients": final_df}