import pandas as pd

# Tables
races_kv = tables["table_2"]
results_df = tables["table_3"]
status_df = tables["table_13"]

# Pivot races key-value to wide
races_wide = (
    races_kv.pivot_table(index="raceId", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)
races_wide.columns.name = None

# Find raceId for Bahrain Grand Prix in 2007
races_wide["year"] = pd.to_numeric(races_wide.get("year"), errors="coerce")
bahrain_2007_race_ids = races_wide.loc[
    (races_wide["year"] == 2007) & (races_wide.get("name") == "Bahrain Grand Prix"),
    "raceId",
].dropna()

# Join results with status and count DNFs (exclude Finished and classified finishes like "+1 Lap")
res = results_df.merge(status_df, on="statusId", how="left")
res_bahrain_2007 = res[res["raceId"].isin(bahrain_2007_race_ids)]

dnf_count = (
    res_bahrain_2007.loc[
        (~res_bahrain_2007["status"].eq("Finished"))
        & (~res_bahrain_2007["status"].astype(str).str.startswith("+", na=False))
    ]["driverId"]
    .nunique()
)

result = {
    "bahrain_grand_prix_2007_dnf_drivers": pd.DataFrame(
        {"dnf_drivers": [int(dnf_count)]}
    )
}
