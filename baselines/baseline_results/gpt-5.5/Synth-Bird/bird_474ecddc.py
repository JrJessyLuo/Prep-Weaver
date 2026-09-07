import pandas as pd
import numpy as np

events = tables["table_1"].copy()
budgets = tables["table_2"].copy()

# Parse budget amount (stored like '"75"') to numeric
budgets["budget_amount"] = (
    budgets["amount"]
    .astype(str)
    .str.replace(r'[^0-9.\-]', '', regex=True)
    .replace('', np.nan)
    .astype(float)
)

# Aggregate budgets/spend by event
by_event = (
    budgets.groupby("link_to_event", as_index=False)
    .agg(total_budget=("budget_amount", "sum"),
         total_spent=("spent", "sum"))
)

# Underspend: spent < budget (and budget is not null/zero)
underspent_ids = by_event.loc[
    by_event["total_budget"].notna() & (by_event["total_budget"] > 0) & (by_event["total_spent"] < by_event["total_budget"]),
    "link_to_event"
]

# Join to events and build location
out = events[events["event_id"].isin(underspent_ids)].copy()
out["location"] = (
    out[["building", "room"]]
    .fillna("")
    .astype(str)
    .agg(lambda x: " ".join([p for p in x if p.strip() != ""]).strip(), axis=1)
)
out.loc[out["location"].eq(""), "location"] = np.nan

out = out[["event_name", "location"]].drop_duplicates().reset_index(drop=True)

result = {"underspent_events": out}
