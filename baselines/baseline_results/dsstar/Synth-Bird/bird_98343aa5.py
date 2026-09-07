import pandas as pd

# Source tables from the provided `tables` dict
links_df = tables["table_1"]
members_df = tables["table_2"]

# Split "combined_links" into "event_id" and "member_id"
split_cols = links_df["combined_links"].str.split("|", n=1, expand=True)
split_cols.columns = ["event_id", "member_id"]
member_event_df = split_cols.copy()

# Group by member_id and count distinct event_id, then filter to those with count > 7
members_over_7_events = (
    member_event_df.groupby("member_id", as_index=False)
    .agg(events_attended=("event_id", "nunique"))
    .query("events_attended > 7")
    .sort_values(["events_attended", "member_id"], ascending=[False, True])
    .reset_index(drop=True)
)

# Join to get student names
answer_df = (
    members_over_7_events.merge(
        members_df[["member_id", "first_name", "last_name"]],
        on="member_id",
        how="left",
    )
    .loc[:, ["first_name", "last_name"]]
    .drop_duplicates()
    .sort_values(["last_name", "first_name"], ascending=[True, True])
    .reset_index(drop=True)
)

# Final result mapping
result = {"students_attended_more_than_7_events": answer_df}