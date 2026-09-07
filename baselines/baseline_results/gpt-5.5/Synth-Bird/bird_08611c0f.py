import pandas as pd

# --- Reconstruct Posts from the "field-name row" + "value row" layout in table_1 ---
raw = tables["table_1"].copy()

# Identify the row that contains the semantic field names per column
hdr_mask = raw["Id"].astype(str).str.lower().eq("shuxing")
hdr = raw.loc[hdr_mask].iloc[0]

# Remaining row(s) contain values; use the first non-header row as the values row
val_df = raw.loc[~hdr_mask]
val_row = val_df.iloc[0]

# Build long (PostId, field, value) then pivot to a normal Posts-like table
fields = hdr.drop(labels=["Id"], errors="ignore")
values = val_row.drop(labels=["Id"], errors="ignore")

long = pd.DataFrame(
    {
        "PostId": fields.index.astype(str),
        "field": fields.values,
        "value": values.values,
    }
)

long["field"] = long["field"].astype(str).str.strip()
long = long[long["field"].notna() & (long["field"] != "") & (long["field"].str.lower() != "nan")]

posts = (
    long.pivot_table(index="PostId", columns="field", values="value", aggfunc="first")
    .reset_index()
)

# Coerce types needed for the query
if "OwnerUserId" in posts.columns:
    posts["OwnerUserId"] = pd.to_numeric(posts["OwnerUserId"], errors="coerce")
if "Score" in posts.columns:
    posts["Score"] = pd.to_numeric(posts["Score"], errors="coerce")

users = tables["table_2"].copy()
users["Age"] = pd.to_numeric(users["Age"], errors="coerce")

elder_user_ids = users.loc[users["Age"] >= 65, "Id"].astype(float)

count_over_19 = (
    posts.loc[
        posts.get("OwnerUserId").isin(elder_user_ids) & (posts.get("Score") > 19),
        :
    ]
    .shape[0]
)

result = {
    "elder_owned_posts_score_over_19_count": pd.DataFrame(
        {"count": [count_over_19]}
    )
}
