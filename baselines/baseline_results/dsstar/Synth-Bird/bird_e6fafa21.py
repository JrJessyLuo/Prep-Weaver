import pandas as pd

# Source table (already loaded in-scope as `tables`)
posts = tables["table_1"]

# Filter to csgillespie's questions
filtered_df = posts.loc[
    (posts["OwnerDisplayName"] == "csgillespie") & (posts["PostTypeId"] == 1),
    ["Id", "AnswerCount"]
].copy()

if filtered_df.empty:
    max_answers = None
    max_id = None
else:
    max_answers = filtered_df["AnswerCount"].fillna(0).max()
    max_id = filtered_df.loc[filtered_df["AnswerCount"].fillna(0) == max_answers, "Id"].iloc[0]

answer_df = pd.DataFrame({"max_answers": [max_answers]})

result = {"answer": answer_df}