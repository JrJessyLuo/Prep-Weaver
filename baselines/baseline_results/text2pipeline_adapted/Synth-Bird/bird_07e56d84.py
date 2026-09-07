import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PostHistoryTypeId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PostId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'CreationDate', 'date_format': '%Y-%m-%d %H:%M:%S.%f'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Text', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'UserDisplayName', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['PostId', 'PostHistoryTypeId', 'Text']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PostId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'vtid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'bamt', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'cdt', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'vtid', 'new_name': 'BountyEventTypeId'}, {'old_name': 'cdt', 'new_name': 'BountyDate'}, {'old_name': 'bamt', 'new_name': 'BountyAmount'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['PostId', 'BountyAmount', 'BountyDate', 'BountyEventTypeId']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Id'] = pd.to_numeric(tmp_0['Id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['PostHistoryTypeId'] = pd.to_numeric(tmp_1['PostHistoryTypeId'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['PostId'] = pd.to_numeric(tmp_2['PostId'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['CreationDate'] = pd.to_datetime(tmp_3['CreationDate'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['Text'] = tmp_4['Text'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['UserDisplayName'] = tmp_5['UserDisplayName'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['PostId', 'PostHistoryTypeId', 'Text']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_5', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Id'] = pd.to_numeric(tmp_0['Id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['PostId'] = pd.to_numeric(tmp_1['PostId'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['vtid'] = pd.to_numeric(tmp_2['vtid'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['bamt'] = pd.to_numeric(tmp_3['bamt'], errors='coerce').astype(float)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['cdt'] = pd.to_datetime(tmp_4['cdt'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'vtid': 'BountyEventTypeId', 'cdt': 'BountyDate', 'bamt': 'BountyAmount'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['PostId', 'BountyAmount', 'BountyDate', 'BountyEventTypeId']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='PostId')
# Identify posts with titles about 'data' using broad case-insensitive matching over title-like history entries.
mask_title_like = integrated['PostHistoryTypeId'].isin([1, 2, 4, 5, 6, 7, 8, 9, 10]) if 'PostHistoryTypeId' in integrated.columns else True
mask_text_has_data = integrated['Text'].astype(str).str.contains('data', case=False, na=False)
filtered = integrated[mask_title_like & mask_text_has_data]
# If no rows matched strictly, relax to any 'data' in Text regardless of PostHistoryTypeId.
if filtered.empty:
    filtered = integrated[integrated['Text'].astype(str).str.contains('data', case=False, na=False)]
# Aggregate total bounty amount per PostId and take the total for the targeted posts.
agg = filtered.groupby('PostId', as_index=False)['BountyAmount'].sum(min_count=1).rename(columns={'BountyAmount': 'TotalBountyAmount'})
# If multiple PostId match 'data', sum across them to provide an overall total; prefer providing a single scalar answer.
overall_total = agg['TotalBountyAmount'].sum(min_count=1)
# Produce a one-row DataFrame as target
target = agg.copy()
target['OverallTotalBountyAmount'] = overall_total
# Keep a concise final projection
target = target[['PostId', 'TotalBountyAmount', 'OverallTotalBountyAmount']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
