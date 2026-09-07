import pandas as pd

# Source table: bird_eed91fbb_input_1.pkl
posts = tables["table_2"]

# 1) Filter for the two specified OwnerDisplayName values and keep ViewCount for later use
target_names = ["Mornington", "Amos"]
filtered_posts = posts.loc[
    posts["OwnerDisplayName"].isin(target_names),
    ["Id", "OwnerDisplayName", "ViewCount"],
].copy()

# Ensure ViewCount is numeric for aggregation/comparison later
filtered_posts["ViewCount"] = pd.to_numeric(filtered_posts["ViewCount"], errors="coerce")

# 2) Group by OwnerDisplayName, sum ViewCount, then compute difference (Mornington - Amos)
viewcount_sums = filtered_posts.groupby("OwnerDisplayName", dropna=False)["ViewCount"].sum(min_count=1)

mornington_sum = viewcount_sums.get("Mornington", 0.0)
amos_sum = viewcount_sums.get("Amos", 0.0)
difference = mornington_sum - amos_sum

# Final answer table
answer_df = pd.DataFrame(
    {
        "Mornington_ViewCount_Sum": [mornington_sum],
        "Amos_ViewCount_Sum": [amos_sum],
        "Difference_Mornington_minus_Amos": [difference],
    }
)

result = {"viewcount_difference": answer_df}