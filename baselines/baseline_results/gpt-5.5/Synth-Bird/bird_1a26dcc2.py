import pandas as pd

posts = tables["table_7"].copy()

# Posts posted by Community => CommunityOwnedDate is not null
community_posts = posts[posts["CommunityOwnedDate"].notna()].copy()

total = len(community_posts)

text_blob = (
    community_posts[["Tags", "Title", "Body"]]
    .fillna("")
    .astype(str)
    .agg(" ".join, axis=1)
)

uses_r = (
    community_posts["Tags"].fillna("").astype(str).str.contains(r"(?i)<r>|<r-language>", regex=True)
    | text_blob.str.contains(r"(?i)\br\b|r-project|\br language\b", regex=True)
)

pct = (uses_r.sum() / total * 100) if total else 0.0

result = {
    "community_posts_r_percentage": pd.DataFrame(
        {"percentage_posts_using_R": [pct]}
    )
}
