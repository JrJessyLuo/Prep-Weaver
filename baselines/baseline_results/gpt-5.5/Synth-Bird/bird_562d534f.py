import pandas as pd

events = tables["table_1"].copy()
links = tables["table_2"].copy()
members = tables["table_3"].copy()

# Get event_id(s) for "Laugh Out Loud"
lol_event_ids = events.loc[events["event_name"].eq("Laugh Out Loud"), "event_id"].dropna().unique()

# Split combined_link into event_id and member_id
parts = links["combined_link"].astype(str).str.split(r"\|", n=1, expand=True)
links_norm = pd.DataFrame({"event_id": parts[0], "member_id": parts[1]})

# Filter attendees for the target event(s)
attendees = links_norm[links_norm["event_id"].isin(lol_event_ids)].dropna(subset=["member_id"])

# Join to members and build full name
out = attendees.merge(members[["member_id", "first_name", "last_name"]], on="member_id", how="inner")
out["full_name"] = out["first_name"].astype(str).str.strip() + " " + out["last_name"].astype(str).str.strip()

result = {
    "student_club_members_attended_laugh_out_loud": out[["full_name"]].drop_duplicates().sort_values("full_name").reset_index(drop=True)
}
