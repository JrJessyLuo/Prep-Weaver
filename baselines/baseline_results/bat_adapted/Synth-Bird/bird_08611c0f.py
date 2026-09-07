import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['Id','Age']].copy()
    prepared['Age'] = pd.to_numeric(prepared['Age'], errors='coerce')
    prepared = prepared.dropna(subset=['Age'])
    target = prepared[['Id','Age']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import pandas as pd
    import numpy as np
    df = table_1.copy()
    id_col = 'Id'
    data_cols = [c for c in df.columns if c != id_col]
    long = df.reset_index(drop=True).melt(id_vars=[id_col], value_vars=data_cols, var_name='PostId', value_name='cell', ignore_index=False)
    long = long.reset_index().rename(columns={'index':'row_idx'})
    long['col_idx'] = long.groupby(['row_idx']).cumcount()
    names = long[long[id_col].astype(str).eq('shuxing')][['col_idx','PostId','cell']].rename(columns={'cell':'Attribute'})
    vals = long[~long[id_col].astype(str).eq('shuxing')][['col_idx','cell']].rename(columns={'cell':'Value'})
    pairs = pd.merge(names, vals, on=['col_idx'])
    pairs = pairs[pairs['Attribute'].isin(['OwnerUserId','Score'])].copy()
    wide = pairs.pivot_table(index='PostId', columns='Attribute', values='Value', aggfunc='first').reset_index()
    wide['OwnerUserId'] = pd.to_numeric(wide.get('OwnerUserId'), errors='coerce')
    wide['Score'] = pd.to_numeric(wide.get('Score'), errors='coerce')
    target = wide[['OwnerUserId','Score']].dropna(subset=['OwnerUserId','Score']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_users = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_posts = prepared_table_2

# Assume prepared tables are dataframes: prepared_users, prepared_posts
# Ensure numeric types for join and filters
prepared_users = prepared_users.copy()
prepared_posts = prepared_posts.copy()

# Coerce Id/OwnerUserId to numeric where possible (drop rows where conversion fails)
for col in ["Id"]:
    prepared_users[col] = pd.to_numeric(prepared_users[col], errors="coerce")
prepared_users = prepared_users.dropna(subset=["Id"]) 
prepared_users["Id"] = prepared_users["Id"].astype("int64")

for col in ["OwnerUserId", "Score"]:
    prepared_posts[col] = pd.to_numeric(prepared_posts[col], errors="coerce")
prepared_posts = prepared_posts.dropna(subset=["OwnerUserId", "Score"]) 
prepared_posts["OwnerUserId"] = prepared_posts["OwnerUserId"].astype("int64")

# Define elder users: Age >= 65 (common interpretation of elder)
prepared_users["Age"] = pd.to_numeric(prepared_users["Age"], errors="coerce")
elder_users = prepared_users[prepared_users["Age"] >= 65][["Id"]]

# Join posts to elder users
posts_elder = prepared_posts.merge(elder_users, left_on="OwnerUserId", right_on="Id", how="inner")

# Count posts with score > 19
answer = int((posts_elder["Score"] > 19).sum())

target = pd.DataFrame({"count": [answer]})

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
