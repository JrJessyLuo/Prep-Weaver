import pandas as pd

# Tables already loaded in `tables`
expenses = tables["table_1"]
members = tables["table_2"]

# Merge: expenses.link_to_member -> members.member_id
merged_df = expenses.merge(
    members[["member_id", "position"]],
    left_on="link_to_member",
    right_on="member_id",
    how="left",
)

# Compute average amount paid by students in a position other than "Member"
avg_paid = merged_df.loc[
    merged_df["position"].notna() & (merged_df["position"] != "Member"),
    "cost",
].mean()

final_df = pd.DataFrame({"average_amount_paid": [avg_paid]})

result = {"average_amount_paid_non_member_positions": final_df}