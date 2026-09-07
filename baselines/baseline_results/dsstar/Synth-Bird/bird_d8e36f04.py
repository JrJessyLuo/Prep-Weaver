import pandas as pd

# Source tables from the provided `tables` dict
events_eav = tables["table_1"]   # bird_d8e36f04_input_0.pkl
budget = tables["table_2"]       # bird_d8e36f04_input_1.pkl
expenses = tables["table_3"]     # bird_d8e36f04_input_2.pkl

# 1) Filter pizza expenses with 50 < cost < 100
filtered = expenses[
    expenses["items"].astype(str).str.contains("Pizza", case=False, na=False)
    & (expenses["cost"] > 50)
    & (expenses["cost"] < 100)
].copy()

# 2) Merge filtered pizza expenses with budget to get link_to_event
budget_for_join = budget.assign(_join_budget_id="rec" + budget["budget_id_suffix"].astype(str))

pizza_with_budget = filtered.merge(
    budget_for_join[["_join_budget_id", "link_to_event"]],
    left_on="link_to_budget",
    right_on="_join_budget_id",
    how="left",
)

# 3) Filter events EAV to only needed attributes and only relevant rids; pivot to wide; select distinct
relevant_event_ids = pizza_with_budget["link_to_event"].dropna().unique()

events_subset = events_eav.loc[
    events_eav["sjid"].isin(["event_name", "event_date"])
    & events_eav["rid"].isin(relevant_event_ids),
    ["rid", "sjid", "value"],
].dropna(subset=["rid", "sjid"])

event_info = (
    events_subset.pivot_table(
        index="rid",
        columns="sjid",
        values="value",
        aggfunc="first",
    )
    .reset_index()
    .rename(columns={"rid": "link_to_event"})
)

answer_df = (
    event_info[["event_name", "event_date"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Final answer in the required format
result = {"events_with_pizza_expenses_50_to_100": answer_df}