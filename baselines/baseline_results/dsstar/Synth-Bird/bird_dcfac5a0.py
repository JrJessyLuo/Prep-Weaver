import re
import pandas as pd

# Tables (already loaded in scope as `tables`)
drivers = tables["table_1"]   # formula_1_drivers.pkl
status_map = tables["table_2"]  # bird_dcfac5a0_input_1.pkl
results = tables["table_3"]   # bird_dcfac5a0_input_2.pkl

# -----------------------------
# Identify American drivers
# -----------------------------
nat_col = "nationality" if "nationality" in drivers.columns else None
if nat_col is None:
    nat_candidates = [c for c in drivers.columns if "nation" in str(c).lower()]
    nat_col = nat_candidates[0]

american_driver_ids = set(
    drivers.loc[
        drivers[nat_col].astype("string").str.casefold().eq("american"),
        "driverId",
    ].astype("int64")
)

# -----------------------------
# Normalize status mapping to have explicit statusId (match reference logic)
# -----------------------------
if "statusId" not in status_map.columns:
    if status_map.index.name == "statusId":
        status_map_norm = status_map.reset_index()
    else:
        status_map_norm = status_map.reset_index(drop=False).rename(columns={"index": "statusId"})
        status_map_norm["statusId"] = status_map_norm["statusId"] + 1
else:
    status_map_norm = status_map.copy()

# -----------------------------
# Match puncture/tyre/tire statuses (same as reference code)
# -----------------------------
pattern = re.compile(r"(puncture|tyre|tire)", flags=re.IGNORECASE)
status_map_norm["_status_str"] = status_map_norm["status_combined"].astype("string")

status_hits = status_map_norm.loc[
    status_map_norm["_status_str"].str.contains(pattern, na=False),
    ["statusId", "status_combined"],
].drop_duplicates()

matched_status_ids = sorted(status_hits["statusId"].astype("int64").unique().tolist())

# -----------------------------
# Filter results: American drivers AND matched status
# -----------------------------
results_norm = results.copy()
results_norm["driverId"] = results_norm["driverId"].astype("int64")
results_norm["statusId"] = results_norm["statusId"].astype("int64")

refiltered = results_norm.loc[
    results_norm["driverId"].isin(american_driver_ids) & results_norm["statusId"].isin(matched_status_ids),
    ["driverId"],
]

answer = pd.DataFrame(
    {"american_drivers_with_puncture_status": [int(refiltered["driverId"].nunique())]}
)

result = {"answer": answer}
print(answer.iloc[0, 0])