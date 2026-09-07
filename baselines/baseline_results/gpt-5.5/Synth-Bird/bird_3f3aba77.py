import pandas as pd

members = tables["table_2"].copy()
income = tables["table_6"].copy()

# Join income to members to get position
df = income.merge(
    members[["member_id", "position"]],
    left_on="link_to_member",
    right_on="member_id",
    how="left"
)

# Filter to positions other than "Member" (case-insensitive), then average amount paid
pos = df["position"].astype(str).str.strip().str.lower()
filtered = df[pos.ne("member") & df["position"].notna()]

avg_amount_paid = filtered["amount"].mean()

result = {
    "average_amount_paid_non_members": pd.DataFrame(
        {"average_amount_paid": [avg_amount_paid]}
    )
}
