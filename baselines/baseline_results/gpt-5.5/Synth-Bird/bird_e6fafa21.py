import pandas as pd

posts = tables["table_1"].copy()
users = tables["table_2"].copy()

# Find user id(s) for csgillespie
name_col = "xm"  # display name column in users
target = "csgillespie"

users[name_col] = users[name_col].astype(str)
uid = users.loc[users[name_col].str.lower().eq(target), "Id"]

if uid.empty:
    uid = users.loc[users[name_col].str.lower().str.contains(r"\bcsgillespie\b", regex=True, na=False), "Id"]

if not uid.empty:
    csg_uid = uid.iloc[0]
    q = posts[(posts["PostTypeId"] == 1) & (posts["ouid"] == csg_uid)].copy()
else:
    # Fallback: try matching OwnerDisplayName in posts if user table doesn't contain the name
    posts["OwnerDisplayName"] = posts["OwnerDisplayName"].astype(str)
    q = posts[(posts["PostTypeId"] == 1) & (posts["OwnerDisplayName"].str.lower().eq(target))].copy()

q["AnswerCount"] = pd.to_numeric(q["AnswerCount"], errors="coerce").fillna(0)

max_answers = int(q["AnswerCount"].max()) if not q.empty else 0

result = {
    "most_answered_post_answer_count": pd.DataFrame({"answer_count": [max_answers]})
}
