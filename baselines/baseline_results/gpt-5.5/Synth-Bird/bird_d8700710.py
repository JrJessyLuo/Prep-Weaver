import pandas as pd

events = tables["table_1"].copy()
budgets = tables["table_2"].copy()

# Parse event year
events["event_date"] = pd.to_datetime(events["event_date"], errors="coerce")
events["year"] = events["event_date"].dt.year

# Ensure spent is numeric
budgets["spent"] = pd.to_numeric(budgets["spent"], errors="coerce").fillna(0)

# Join budgets to events, then sum spent by year
budgets_events = budgets.merge(
    events[["event_id", "year"]],
    left_on="link_to_event",
    right_on="event_id",
    how="left"
)

year_totals = budgets_events.groupby("year", dropna=False)["spent"].sum()

spent_2019 = float(year_totals.get(2019, 0.0))
spent_2020 = float(year_totals.get(2020, 0.0))
diff_2020_minus_2019 = spent_2020 - spent_2019

result = {
    "spent_difference_2019_2020": pd.DataFrame(
        {"spent_difference_2020_minus_2019": [diff_2020_minus_2019]}
    )
}
