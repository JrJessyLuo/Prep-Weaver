import pandas as pd

events = tables["table_1"].copy()
budget = tables["table_2"].copy()

# Unpivot the "matrix" budget table into long form, then pivot to get semantic columns
long = budget.melt(id_vars=["budget_id"], var_name="event_id", value_name="value")
wide = (
    long.pivot_table(index="event_id", columns="budget_id", values="value", aggfunc="first")
    .reset_index()
)
wide.columns.name = None

# Ensure numeric spent
wide["spent"] = pd.to_numeric(wide.get("spent"), errors="coerce")

# Find event with max advertisement spent
ad = wide[wide.get("category").eq("Advertisement")].dropna(subset=["spent"])
top_event_id = ad.loc[ad["spent"].idxmax(), "event_id"] if not ad.empty else None

out = (
    events.loc[events["event_id"].eq(top_event_id), ["event_name"]]
    .rename(columns={"event_name": "event_name_with_highest_ad_spend"})
    .reset_index(drop=True)
)

result = {"highest_advertisement_spend_event": out}
