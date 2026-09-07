import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t4 = tables["table_4"].copy()

# Normalize events table (table_1 is transposed: attributes in rows, event record ids in columns)
events = (
    t1.set_index("event_id")
      .T
      .reset_index()
      .rename(columns={"index": "event_record_id"})
)

# Get the event_record_id for "September Meeting"
sept_event_id = events.loc[events["event_name"].eq("September Meeting"), "event_record_id"].iloc[0]

# Sum approved food expenses linked to budgets for the September Meeting
t4["approved"] = t4["approved"].astype(str).str.lower()
food_spent = (
    t4.merge(t2, left_on="link_to_budget", right_on="budget_id", how="inner")
      .loc[
          lambda d: d["approved"].eq("true")
                    & d["category"].eq("Food")
                    & d["lte"].eq(sept_event_id),
          "cost"
      ]
      .sum()
)

result = {
    "september_meeting_food_spent": pd.DataFrame({"food_spent": [food_spent]})
}
