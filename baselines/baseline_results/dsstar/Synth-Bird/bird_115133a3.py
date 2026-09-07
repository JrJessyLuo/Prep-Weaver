import pandas as pd

# Inputs are already loaded in `tables`
df_scores = tables["table_1"]
df_schools = tables["table_2"]

# --- Reproduce reference logic ---

df_scores = df_scores.copy()
df_schools = df_schools.copy()

def to_cds_str(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    n = int(float(s))
    return str(n)

df_scores["cds_raw_str"] = df_scores["cds"].map(to_cds_str)
df_schools["CDSCode_raw_str"] = df_schools["CDSCode"].map(to_cds_str)

df_scores["cds14"] = df_scores["cds_raw_str"].astype("string").str.zfill(14)
df_schools["cds14"] = df_schools["CDSCode_raw_str"].astype("string").str.zfill(14)

df_scores["cds_last7"] = df_scores["cds14"].str[-7:]
df_schools["cds_last7"] = df_schools["cds14"].str[-7:]

df_scores["cds_last12"] = df_scores["cds14"].str[-12:]
df_schools["cds_last12"] = df_schools["cds14"].str[-12:]

scores_cols = ["cds", "AvgScrWrite", "cds14", "cds_last12", "cds_last7"]
schools_cols = ["School", "District", "County", "Phone", "OpenDate", "ClosedDate", "cds14", "cds_last12", "cds_last7"]

scores = df_scores[scores_cols].copy()
schools = df_schools[schools_cols].copy()

schools14 = schools.drop_duplicates(subset=["cds14"])
schools12 = schools.drop_duplicates(subset=["cds_last12"])
schools7 = schools.drop_duplicates(subset=["cds_last7"])

merged14 = scores.merge(
    schools14[["cds14", "School", "District", "County", "Phone", "OpenDate", "ClosedDate"]],
    on="cds14",
    how="left",
    validate="m:1",
)

unmatched_mask = merged14["School"].isna()
if unmatched_mask.any():
    add12 = (
        scores.loc[unmatched_mask, ["cds_last12"]]
        .merge(
            schools12[["cds_last12", "School", "District", "County", "Phone", "OpenDate", "ClosedDate"]],
            on="cds_last12",
            how="left",
            validate="m:1",
        )
        .set_index(scores.index[unmatched_mask])
    )
    for col in ["School", "District", "County", "Phone", "OpenDate", "ClosedDate"]:
        merged14.loc[unmatched_mask, col] = add12[col].values

unmatched_mask2 = merged14["School"].isna()
if unmatched_mask2.any():
    add7 = (
        scores.loc[unmatched_mask2, ["cds_last7"]]
        .merge(
            schools7[["cds_last7", "School", "District", "County", "Phone", "OpenDate", "ClosedDate"]],
            on="cds_last7",
            how="left",
            validate="m:1",
        )
        .set_index(scores.index[unmatched_mask2])
    )
    for col in ["School", "District", "County", "Phone", "OpenDate", "ClosedDate"]:
        merged14.loc[unmatched_mask2, col] = add7[col].values

merged14["OpenDate_dt"] = pd.to_datetime(merged14["OpenDate"], errors="coerce", infer_datetime_format=True)
merged14["ClosedDate_dt"] = pd.to_datetime(merged14["ClosedDate"], errors="coerce", infer_datetime_format=True)

cut_open = pd.Timestamp("1991-12-31")
cut_closed = pd.Timestamp("2000-01-01")

matched = merged14.loc[merged14["School"].notna()].copy()
filtered = matched.loc[
    (matched["OpenDate_dt"] > cut_open) |
    (matched["ClosedDate_dt"].notna() & (matched["ClosedDate_dt"] < cut_closed))
].copy()

overall_avg = filtered["AvgScrWrite"].mean()

answer_df = filtered[["School", "AvgScrWrite", "Phone"]].copy()

# Final result (per guidelines)
result = {
    "schools_opened_after_1991_or_closed_before_2000": answer_df
}