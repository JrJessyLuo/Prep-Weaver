import pandas as pd

# Source tables (already loaded in scope as `tables`)
events = tables["table_1"]      # bird_5bbabded_input_0.pkl (events info)
link_wide = tables["table_2"]   # bird_5bbabded_input_1.pkl (event–member attendance wide table)

# Reproduce reference logic: wide -> long attendance table
member_col = link_wide.columns[0]          # assumed member id column
event_cols = list(link_wide.columns[1:])   # remaining columns are event ids

attendance_long = (
    link_wide
    .melt(
        id_vars=[member_col],
        value_vars=event_cols,
        var_name="event_id",
        value_name="present"
    )
    .rename(columns={member_col: "member_id"})
)

attendance_long = (
    attendance_long[attendance_long["present"].notna()][["event_id", "member_id"]]
    .dropna(subset=["event_id", "member_id"])
    .drop_duplicates()
    .reset_index(drop=True)
)

# Count attendees per event
attendee_counts = (
    attendance_long
    .groupby("event_id")
    .size()
    .reset_index(name="attendee_count")
)

# Events attended by > 10 members
events_over_10 = attendee_counts[attendee_counts["attendee_count"] > 10].copy()

# Join to event metadata and count how many are meetings
events_over_10 = events_over_10.merge(events, on="event_id", how="left")

# Identify the event type column (common variants)
type_col_candidates = [
    "event_type", "type", "event_kind", "kind", "category", "event_category", "event_name"
]
type_col = next((c for c in type_col_candidates if c in events_over_10.columns), None)

meeting_count = 0
if type_col is not None:
    meeting_count = int(
        events_over_10[type_col]
        .astype(str)
        .str.strip()
        .str.lower()
        .eq("meeting")
        .sum()
    )

answer_df = pd.DataFrame({"meeting_event_count": [meeting_count]})

# Final result per required convention
result = {"answer": answer_df}