import pandas as pd

# Tables
att = tables["table_1"].copy()
members = tables["table_2"].copy()

# Split combined links into event_id and member_id
parts = att["combined_links"].astype(str).str.split("|", n=1, expand=True)
att["event_id"] = parts[0]
att["member_id"] = parts[1]

# Count events attended per member (unique events, in case of duplicates)
event_counts = (
    att.dropna(subset=["member_id", "event_id"])
       .drop_duplicates(subset=["member_id", "event_id"])
       .groupby("member_id", as_index=False)
       .agg(events_attended=("event_id", "nunique"))
)

# Members with > 7 events
active = event_counts[event_counts["events_attended"] > 7]

# Join to members to get names
out = active.merge(members[["member_id", "first_name", "last_name"]], on="member_id", how="left")
out["student_name"] = (out["first_name"].fillna("") + " " + out["last_name"].fillna("")).str.strip()

students_more_than_7_events = (
    out.loc[out["student_name"].ne(""), ["student_name"]]
       .drop_duplicates()
       .sort_values("student_name")
       .reset_index(drop=True)
)

result = {"students_more_than_7_events": students_more_than_7_events}
