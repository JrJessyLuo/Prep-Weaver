import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Collecrtion_Subset_Details', 'new_name': 'Collection_Subset_Details'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Collection_Subset_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Collection_Subset_ID', 'Collection_Subset_Name', 'Collection_Subset_Details']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'subset_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subset_type', 'func': 'def transform(s):\n    # Trim surrounding whitespace but preserve original letter casing\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Collection_ID', 'Related_Collection_ID', 'subset_type', 'subset_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Collecrtion_Subset_Details': 'Collection_Subset_Details'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Collection_Subset_ID'] = pd.to_numeric(tmp_1['Collection_Subset_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Collection_Subset_ID', 'Collection_Subset_Name', 'Collection_Subset_Details']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['subset_id'] = pd.to_numeric(tmp_0['subset_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but preserve original letter casing\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['subset_type'] = tmp_1['subset_type'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Collection_ID', 'Related_Collection_ID', 'subset_type', 'subset_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, left_on='subset_id', right_on='Collection_Subset_ID', how='left')
# Count number of collections per subset_id using Collection_ID (count distinct Collection_ID to avoid double-counts if duplicates exist)
counts = integrated.groupby(['subset_id', 'Collection_Subset_Name'], dropna=False)['Collection_ID'].nunique().reset_index(name='number_of_collections')
# Final projection with requested fields; prefer the canonical subset id column name
counts = counts.rename(columns={'subset_id': 'Collection_Subset_ID', 'Collection_Subset_Name': 'Collection_Subset_Name'})
target = counts[['Collection_Subset_ID', 'Collection_Subset_Name', 'number_of_collections']].sort_values(['Collection_Subset_ID'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
