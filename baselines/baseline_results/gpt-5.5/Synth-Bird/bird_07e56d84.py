import pandas as pd

ph = tables["table_5"].copy()
votes = tables["table_2"].copy()

# Get latest title per PostId from post history (PostHistoryTypeId == 1)
ph = ph[ph["PostHistoryTypeId"] == 1].copy()
ph["CreationDate"] = pd.to_datetime(ph["CreationDate"], errors="coerce")
ph = ph.sort_values(["PostId", "CreationDate"])
latest_titles = ph.drop_duplicates(subset=["PostId"], keep="last")[["PostId", "Text"]].rename(columns={"Text": "Title"})

# Posts whose latest title contains 'data' (case-insensitive)
data_posts = latest_titles[latest_titles["Title"].astype(str).str.contains(r"\bdata\b", case=False, na=False)][["PostId"]].drop_duplicates()

# Sum bounty amounts for those posts
votes["bamt"] = pd.to_numeric(votes["bamt"], errors="coerce")
total_bounty = votes.merge(data_posts, on="PostId", how="inner")["bamt"].fillna(0).sum()

result = {
    "total_bounty_amount": pd.DataFrame({"total_bounty_amount": [total_bounty]})
}
