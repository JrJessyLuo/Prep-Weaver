import pandas as pd
import numpy as np

# Source tables (already loaded in-scope as `tables`)
posts = tables["table_1"].copy()
users = tables["table_2"].copy()

def safe_int_series(s):
    return pd.to_numeric(s, errors="coerce").astype("Int64")

ELDER_AGE_THRESHOLD = 65

# Reproduce reference logic: join posts.ouid -> users.Id, filter Score > 5, compute elder % among known Age
posts["ouid_int"] = safe_int_series(posts.get("ouid"))
users["Id_int"] = safe_int_series(users.get("Id"))
users["Age_num"] = pd.to_numeric(users.get("Age"), errors="coerce")

joined = posts.merge(
    users[["Id_int", "Age_num"]],
    left_on="ouid_int",
    right_on="Id_int",
    how="left",
)

score_filtered = joined[joined["Score"] > 5].copy()

n_known_age = int(score_filtered["Age_num"].notna().sum())
elder_pct_among_known_age = (
    100.0
    * score_filtered.loc[score_filtered["Age_num"].notna(), "Age_num"]
    .ge(ELDER_AGE_THRESHOLD)
    .mean()
) if n_known_age else np.nan

answer_df = pd.DataFrame(
    {
        "elder_pct_among_known_age_score_gt_5": [elder_pct_among_known_age]
    }
)

result = {"answer": answer_df}