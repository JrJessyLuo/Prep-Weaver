import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'aff_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'aff_id', 'new_name': 'affiliation_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'aid', 'affiliation_id']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'affiliation_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'affiliation_id', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['affiliation_id', 'name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['aff_id'] = pd.to_numeric(tmp_0['aff_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'aff_id': 'affiliation_id'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['paper_id', 'aid', 'affiliation_id']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['affiliation_id'] = pd.to_numeric(tmp_0['affiliation_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['attribute'] = tmp_1['attribute'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['value'] = tmp_2['value'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='affiliation_id', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['affiliation_id', 'name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
affs = prepared_table_2.copy()
# Join paper-affiliation links to affiliation names
joined = prepared_table_1.merge(affs, on='affiliation_id', how='left')
# Count distinct papers per affiliation name; if name is missing, keep as missing group
paper_counts = joined.groupby('name', dropna=False)['paper_id'].nunique().reset_index(name='total_papers')
# Sort by count desc then name for readability
target = paper_counts.sort_values(['total_papers', 'name'], ascending=[False, True])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
