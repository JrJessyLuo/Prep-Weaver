import pandas as pd
import numpy as np

posts = tables["table_1"].copy()
users = tables["table_2"].copy()

# Posts with score > 5 and a known owner
posts = posts[posts["Score"] > 5].copy()
posts = posts[posts["ouid"].notna()].copy()
posts["ouid"] = posts["ouid"].astype("int64")

# Join to users to get owner age
u = users[["Id", "Age"]].copy()
joined = posts.merge(u, left_on="ouid", right_on="Id", how="left")

# Define "elder" as Age >= 65; missing ages count as not elder
is_elder = joined["Age"].ge(65).fillna(False)

total = len(joined)
pct = (is_elder.sum() / total * 100) if total else 0.0

result = {
    "percentage_posts_score_over_5_owned_by_elder_user": pd.DataFrame(
        {"percentage": [pct]}
    )
}
