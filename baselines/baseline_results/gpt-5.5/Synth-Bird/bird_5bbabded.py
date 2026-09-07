import pandas as pd

events = tables["table_1"].copy()
att_wide = tables["table_2"].copy()

# Unpivot attendance: columns (event_id) -> rows (event_id, member_id)
value_cols = [c for c in att_wide.columns if c != "link_to_event"]
att_long = att_wide.melt(value_vars=value_cols, var_name="event_id", value_name="member_id")

# Keep only plausible member record ids and non-nulls
att_long = att_long.dropna(subset=["member_id"])
att_long = att_long[att_long["member_id"].astype(str).str.match(r"^rec")]

# Count attendees per event
att_counts = att_long.groupby("event_id")["member_id"].nunique()

events_over_10 = att_counts[att_counts > 10].index

meetings_count = events[
    events["event_id"].isin(events_over_10)
    & events["lx"].fillna("").astype(str).str.lower().eq("meeting")
].shape[0]

result = {
    "meetings_among_events_attended_by_more_than_10": pd.DataFrame(
        {"number_of_meetings": [meetings_count]}
    )
}
