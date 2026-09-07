import pandas as pd
import re

members = tables["table_2"].copy()
attendance = tables["table_1"].copy()

def norm_phone(x):
    if pd.isna(x):
        return None
    return re.sub(r"\D+", "", str(x))

target_phone_norm = norm_phone("954-555-6240")
members["_phone_norm"] = members["phone"].map(norm_phone)

target_member_ids = members.loc[members["_phone_norm"] == target_phone_norm, "member_id"].dropna().unique().tolist()

events_attended = 0

def attended_flag(v):
    if isinstance(v, (list, tuple, set)):
        return len(v) > 0
    if pd.isna(v):
        return False
    s = str(v).strip()
    return s != "" and s.lower() not in {"nan", "none", "null"}

if target_member_ids:
    mid = target_member_ids[0]

    if mid in attendance.columns:
        events_attended = int(attendance[mid].map(attended_flag).sum())
    elif "link_to_member" in attendance.columns:
        # Fallback: if table_1 is in long form with link_to_member as member_id
        events_attended = int((attendance["link_to_member"] == mid).sum())

result = {
    "events_attended": pd.DataFrame(
        {"phone": ["954-555-6240"], "events_attended": [events_attended]}
    )
}
