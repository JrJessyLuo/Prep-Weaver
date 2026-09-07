import pandas as pd

# Tables are already loaded in scope as `tables`
income_df = tables["table_1"]
member_raw_df = tables["table_2"]

# Filter to dues payments (exclude rows with missing member link, e.g., "School Appropration")
dues_df = income_df[income_df["link_to_member"].notna()].copy()

# Parse and sort by date_received ascending to find earliest dues payment
dues_df["date_received_parsed"] = pd.to_datetime(dues_df["date_received"], errors="coerce")
dues_sorted = dues_df.sort_values(["date_received_parsed", "income_id"], ascending=[True, True])

earliest_dues_entry = dues_sorted.iloc[0]
earliest_member_id = earliest_dues_entry["link_to_member"]

# Member table is stored as key-value rows; reshape to have one row per member_id
member_long = (
    member_raw_df
    .set_index("member_id")
    .T
    .rename_axis("member_record_id")
    .reset_index()
)

# Join to get first_name and last_name for the earliest dues payer
member_match = member_long.loc[
    member_long["member_record_id"] == earliest_member_id,
    ["member_record_id", "first_name", "last_name"]
].copy()

# Final answer table
answer_df = member_match.assign(
    full_name=(member_match["first_name"].fillna("").astype(str).str.strip() + " " +
               member_match["last_name"].fillna("").astype(str).str.strip()).str.strip()
)[["full_name"]]

result = {"first_dues_payer": answer_df}