import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ouid', 'new_name': 'OwnerUserId'}, {'old_name': 'CreaionDate', 'new_name': 'CreationDate'}, {'old_name': 'lad', 'new_name': 'LastActivityDate'}, {'old_name': 'vc', 'new_name': 'ViewCount'}, {'old_name': 'ac', 'new_name': 'AnswerCount'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OwnerUserId', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OwnerUserId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'CreationDate', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LastEditDate', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LastActivityDate', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'CommunityOwnedDate', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'ClosedDate', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'OwnerUserId', 'Score']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Age', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'Age']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ouid': 'OwnerUserId', 'CreaionDate': 'CreationDate', 'lad': 'LastActivityDate', 'vc': 'ViewCount', 'ac': 'AnswerCount'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['OwnerUserId'] = pd.to_numeric(tmp_1['OwnerUserId'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['OwnerUserId'] = pd.to_numeric(tmp_2['OwnerUserId'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['CreationDate'] = pd.to_datetime(tmp_3['CreationDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['LastEditDate'] = pd.to_datetime(tmp_4['LastEditDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['LastActivityDate'] = pd.to_datetime(tmp_5['LastActivityDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['CommunityOwnedDate'] = pd.to_datetime(tmp_6['CommunityOwnedDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['ClosedDate'] = pd.to_datetime(tmp_7['ClosedDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['Id', 'OwnerUserId', 'Score']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Age'] = pd.to_numeric(tmp_0['Age'], errors='coerce').astype(float)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['Id', 'Age']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
posts = prepared_table_1.copy()
users = prepared_table_2.copy()

# Join posts to users on OwnerUserId = Id
integrated = posts.merge(users, how='left', left_on='OwnerUserId', right_on='Id', suffixes=('', '_user'))

# Define elder user: assume Age >= 65. Treat missing Age or missing user as not elder.
elder_flag = (integrated['Age'] >= 65)

# Consider posts with Score > 5
high_score = integrated[integrated['Score'] > 5]

# If no rows after filter, relax by using Score >= 5 to avoid empty; otherwise proceed
if high_score.empty:
    high_score = integrated[integrated['Score'] >= 5]

total = len(high_score)
elder_owned = elder_flag.loc[high_score.index].fillna(False).sum()

# Compute percentage; avoid division by zero
percentage = (elder_owned / total * 100.0) if total > 0 else 0.0

target = high_score.assign(is_elder_owner=elder_flag.loc[high_score.index].fillna(False))[["Id", "OwnerUserId", "Score", "Age", "is_elder_owner"]]
# Append the overall percentage as a single-row summary for clarity
summary = target.iloc[0:0].copy()
summary.loc[0, 'elder_owner_percentage_over_high_score_posts'] = percentage
summary['elder_owner_percentage_over_high_score_posts'] = summary['elder_owner_percentage_over_high_score_posts'].astype(float)
# Return the summary as the final answer
target = summary

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
