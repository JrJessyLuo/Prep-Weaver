import pandas as pd

# Tables are preloaded in a dict named `tables`
posts = tables["table_1"]     # bird_07e56d84_input_0.pkl (posts-like table with Id, Title)
bounties = tables["table_2"]  # bird_07e56d84_input_1.pkl (bounty table with PostId, bamt)

# Filter posts to titles containing "data" (case-insensitive) to get matching post Ids
matching_post_ids = posts.loc[
    posts["Title"].astype(str).str.contains("data", case=False, na=False),
    "Id",
]

# Inner-join on PostId (bounties) == Id (posts) and compute total bounty amount (nulls as 0)
joined = bounties.merge(
    matching_post_ids.drop_duplicates().to_frame(name="Id"),
    left_on="PostId",
    right_on="Id",
    how="inner",
)

total_bounty_amount = joined["bamt"].fillna(0).sum()

# Final answer as a DataFrame in `result` dict
answer_df = pd.DataFrame({"total_bounty_amount": [total_bounty_amount]})
result = {"total_bounty_amount_for_titles_containing_data": answer_df}