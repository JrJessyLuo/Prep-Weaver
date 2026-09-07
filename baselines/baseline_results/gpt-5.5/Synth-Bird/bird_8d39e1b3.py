import pandas as pd

events = tables["table_1"].copy()
attendance = tables["table_2"].copy()
members_kv = tables["table_3"].copy()

# table_3 is transposed (attributes in rows, member record ids in columns) -> make it member-wise
members = (
    members_kv.set_index("member_id")
    .T.reset_index()
    .rename(columns={"index": "member_record_id"})
)

maya_id = members.loc[
    (members["first_name"].astype(str).str.strip() == "Maya")
    & (members["last_name"].astype(str).str.strip() == "Mclean"),
    "member_record_id"
].iloc[0]

# Normalize attendance: split comma-separated member ids and explode
att_long = attendance.assign(
    member_id=attendance["link_to_member"].fillna("").astype(str).str.split(",")
).explode("member_id")

att_long["member_id"] = att_long["member_id"].astype(str).str.strip()
maya_event_ids = att_long.loc[att_long["member_id"] == maya_id, "link_to_event"].dropna().unique()

out = (
    events.loc[events["event_id"].isin(maya_event_ids), ["event_name"]]
    .drop_duplicates()
    .sort_values("event_name")
    .reset_index(drop=True)
)

result = {"events_attended_by_maya_mclean": out}
