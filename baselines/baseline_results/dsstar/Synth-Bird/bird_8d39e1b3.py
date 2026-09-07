import pandas as pd
import re

# Source tables from the provided `tables` dict
events = tables["table_1"]  # bird_8d39e1b3_input_0.pkl
links = tables["table_2"]   # bird_8d39e1b3_input_1.pkl

member_id = "recZ4PkGERzl9ziHO"  # Maya Mclean

# Match member_id inside a comma-separated list
pattern = rf"(^|,)\s*{re.escape(member_id)}\s*(,|$)"
mask = links["link_to_member"].astype(str).str.contains(pattern, regex=True, na=False)

# Extract event IDs and join to events to get event names
maya_event_ids = links.loc[mask, "link_to_event"].dropna().unique()

answer_df = (
    events.loc[events["event_id"].isin(maya_event_ids), ["event_name"]]
    .drop_duplicates()
    .sort_values(["event_name"], kind="stable")
    .reset_index(drop=True)
)

result = {"maya_mclean_attended_event_names": answer_df}