import pandas as pd

# Tables are preloaded in `tables`
posts_raw = tables["table_1"]
users = tables["table_2"]

# ---- Elder threshold per reference logic ----
ELDER_AGE_THRESHOLD = 60

ages = pd.to_numeric(users["Age"], errors="coerce")
elder_user_ids = set(
    users.loc[ages.notna() & (ages >= ELDER_AGE_THRESHOLD), "Id"].astype(int).tolist()
)

# ---- Reconstruct posts table (given dataset format) ----
posts_kv = posts_raw.iloc[:, 1:]  # exclude 'Id' column
colnames = posts_kv.iloc[0].astype(str).tolist()
values = posts_kv.iloc[1].tolist()
posts = pd.DataFrame([values], columns=colnames)

posts_sub = posts.loc[:, ["OwnerUserId", "Score"]].copy()
posts_sub["OwnerUserId"] = pd.to_numeric(posts_sub["OwnerUserId"], errors="coerce")
posts_sub["Score"] = pd.to_numeric(posts_sub["Score"], errors="coerce")

elder_posts = posts_sub.loc[posts_sub["OwnerUserId"].isin(elder_user_ids)]
count_posts_score_gt_19 = int((elder_posts["Score"] > 19).sum())

answer_df = pd.DataFrame(
    [{"count_posts_owned_by_elder_with_score_over_19": count_posts_score_gt_19}]
)

result = {"answer": answer_df}