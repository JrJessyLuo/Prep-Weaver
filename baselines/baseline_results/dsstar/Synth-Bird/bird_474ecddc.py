import pandas as pd

# Source tables from the provided `tables` dict
events = tables["table_1"]
budgets = tables["table_2"]

# Clean/normalize budget numeric fields
budgets = budgets.copy()
budgets["amount_num"] = pd.to_numeric(
    budgets["amount"].astype(str).str.replace('"', "", regex=False).str.strip(),
    errors="coerce",
)
budgets["spent"] = pd.to_numeric(budgets["spent"], errors="coerce")

# Join: events.event_id = budgets.link_to_event
joined = events.merge(
    budgets,
    left_on="event_id",
    right_on="link_to_event",
    how="inner",
    suffixes=("_event", "_budget"),
)

# Identify underspend: spent < amount
underspend = joined.loc[
    joined["spent"].notna()
    & joined["amount_num"].notna()
    & (joined["spent"] < joined["amount_num"])
].copy()

# Recompute location as TRIM(CONCAT(COALESCE(building,''),' ',COALESCE(room,'')))
def recompute_location(df: pd.DataFrame) -> pd.Series:
    building = df["building"].fillna("").astype(str)
    room = df["room"].fillna("").astype(str)
    return (building + " " + room).str.replace(r"\s+", " ", regex=True).str.strip()

underspend = underspend.assign(location=recompute_location(underspend))

final_event_locations = (
    underspend.loc[:, ["event_name", "location"]]
    .drop_duplicates()
    .sort_values(["event_name", "location"], na_position="last")
    .reset_index(drop=True)
)

# Final output in required variable
result = {"underspent_events": final_event_locations}