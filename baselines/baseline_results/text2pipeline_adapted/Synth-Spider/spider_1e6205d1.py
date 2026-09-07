import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'University_ID', 'new_name': 'field'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['field'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], 'var_name': 'uni_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'uni_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'uni_id', 'columns': 'field', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'University_Name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['uni_id', 'University_Name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'uni_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Rank', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Reputation_point', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Research_point', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'cit_p', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Total', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['uni_id', 'Rank', 'Reputation_point', 'cit_p']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'University_ID': 'field'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['field'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], var_name='uni_id', value_name='value')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['uni_id'] = pd.to_numeric(tmp_2['uni_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='uni_id', columns='field', values='value', aggfunc='first').reset_index()
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['University_Name'] = tmp_4['University_Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['uni_id', 'University_Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['uni_id'] = pd.to_numeric(tmp_0['uni_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Rank'] = pd.to_numeric(tmp_1['Rank'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Reputation_point'] = pd.to_numeric(tmp_2['Reputation_point'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Research_point'] = pd.to_numeric(tmp_3['Research_point'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['cit_p'] = pd.to_numeric(tmp_4['cit_p'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Total'] = pd.to_numeric(tmp_5['Total'], errors='coerce').fillna(0).astype(int)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['uni_id', 'Rank', 'Reputation_point', 'cit_p']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='uni_id', how='inner')
# Get top 3 by Reputation_point; if ties expand naturally then take top 3 rows after sorting by Reputation_point desc, then by uni_id asc for determinism
integrated_sorted = integrated.sort_values(['Reputation_point','uni_id'], ascending=[False, True])
result = integrated_sorted[['University_Name','cit_p','Reputation_point']].head(3)
# Final projection: name and citation point as requested
target = result[['University_Name','cit_p']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
