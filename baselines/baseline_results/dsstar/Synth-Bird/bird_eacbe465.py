import pandas as pd

# Source tables from the provided `tables` dict
attendance = tables["table_1"]  # bird_eacbe465_input_0.pkl
members = tables["table_2"]     # bird_eacbe465_input_1.pkl

# 1) Get the member_id for the given phone number
member_ids = (
    members.loc[members["phone"] == "954-555-6240", "member_id"]
    .dropna()
    .unique()
    .tolist()
)

if not member_ids:
    answer_df = pd.DataFrame({"member_id": [None], "attendance_count": [0]})
else:
    member_id = member_ids[0]

    # 2) Select the row(s) with that link_to_member
    member_rows = attendance.loc[attendance["link_to_member"] == member_id]

    # 3) Count non-null/true-ish values across all event columns (exclude link_to_member)
    event_cols = [c for c in attendance.columns if c != "link_to_member"]

    if member_rows.empty:
        attendance_count = 0
    else:
        s = member_rows[event_cols]
        attended_mask = (
            s.notna()
            & s.astype(str).str.strip().ne("")
            & s.astype(str).str.lower().ne("false")
        )
        attendance_count = int(attended_mask.to_numpy().sum())

    answer_df = pd.DataFrame({"member_id": [member_id], "attendance_count": [attendance_count]})

# Final output per guideline
result = {"events_attended_by_phone_954_555_6240": answer_df}
print(answer_df["attendance_count"].iloc[0])