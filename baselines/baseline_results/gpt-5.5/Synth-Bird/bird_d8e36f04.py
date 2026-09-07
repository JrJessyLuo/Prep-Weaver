import pandas as pd

# Load tables
t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Pivot event key-value table to wide
events = (
    t1.pivot_table(index="rid", columns="sjid", values="value", aggfunc="first")
      .reset_index()
      .rename(columns={"rid": "event_id"})
)

# Pick the best available event name column
name_candidates = ["event_name", "name", "event", "event_title", "title"]
event_name_col = next((c for c in name_candidates if c in events.columns), None)
if event_name_col is None:
    # If no obvious name field exists, still return event_id as the "name" placeholder
    events["event_name"] = events["event_id"]
else:
    events = events.rename(columns={event_name_col: "event_name"})

# Standardize event_date if present
if "event_date" in events.columns:
    events["event_date"] = pd.to_datetime(events["event_date"], errors="coerce")

# Build budget_id to connect expenses -> budgets -> events
t2["budget_id"] = t2["budget_id_prefix"].astype(str) + t2["budget_id_suffix"].astype(str)

# Filter pizza expenses with cost > 50 and < 100
pizza_exp = t3[
    t3["items"].fillna("").str.contains(r"\bpizza\b", case=False, regex=True)
    & (t3["cost"] > 50)
    & (t3["cost"] < 100)
].copy()

# Link pizza expenses to events via budgets
pizza_exp = pizza_exp.merge(
    t2[["budget_id", "link_to_event"]],
    left_on="link_to_budget",
    right_on="budget_id",
    how="left"
)

# Join to event info and select requested columns
out = (
    pizza_exp.merge(
        events[["event_id", "event_name"] + (["event_date"] if "event_date" in events.columns else [])],
        left_on="link_to_event",
        right_on="event_id",
        how="left"
    )[["event_name"] + (["event_date"] if "event_date" in events.columns else [])]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"events_with_pizza_expenses_50_to_100": out}
