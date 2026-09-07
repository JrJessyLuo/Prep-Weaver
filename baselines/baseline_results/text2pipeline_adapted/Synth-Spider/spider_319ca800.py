import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Collection_Subset_ID', 'new_name': 'subset_id'}, {'old_name': 'Collection_Subset_Name', 'new_name': 'subset_name'}, {'old_name': 'Collecrtion_Subset_Details', 'new_name': 'subset_details'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'subset_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subset_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['subset_id', 'subset_name', 'subset_details']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Collection_ID', 'new_name': 'collection_id'}, {'old_name': 'Related_Collection_ID', 'new_name': 'related_collection_id'}, {'old_name': 'Collection_Subset_ID', 'new_name': 'subset_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'collection_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'related_collection_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'subset_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['collection_id', 'related_collection_id', 'subset_id']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Document_Object_ID', 'new_name': 'document_id'}, {'old_name': 'Collection_ID', 'new_name': 'collection_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'document_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'collection_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['document_id', 'collection_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Collection_Subset_ID': 'subset_id', 'Collection_Subset_Name': 'subset_name', 'Collecrtion_Subset_Details': 'subset_details'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['subset_id'] = pd.to_numeric(tmp_1['subset_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['subset_name'] = tmp_2['subset_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['subset_id', 'subset_name', 'subset_details']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Collection_ID': 'collection_id', 'Related_Collection_ID': 'related_collection_id', 'Collection_Subset_ID': 'subset_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['collection_id'] = pd.to_numeric(tmp_1['collection_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['related_collection_id'] = pd.to_numeric(tmp_2['related_collection_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['subset_id'] = pd.to_numeric(tmp_3['subset_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['collection_id', 'related_collection_id', 'subset_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Document_Object_ID': 'document_id', 'Collection_ID': 'collection_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['document_id'] = pd.to_numeric(tmp_1['document_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['collection_id'] = pd.to_numeric(tmp_2['collection_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['document_id', 'collection_id']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
subsets = prepared_table_1
subset_link = prepared_table_2
col_docs = prepared_table_3
# Link collections to subsets
col_to_subset = subset_link.merge(subsets, how='left', on='subset_id')
# Link documents to collections, then to subsets
docs_in_subsets = col_docs.merge(col_to_subset[['collection_id','subset_id','subset_name']], how='left', on='collection_id')
# Count distinct documents per subset_id
counts = docs_in_subsets.groupby(['subset_id','subset_name'])['document_id'].nunique().reset_index(name='num_documents')
# Ensure all subsets are represented, including those without documents
result = subsets.merge(counts, how='left', on=['subset_id','subset_name'])
result['num_documents'] = result['num_documents'].fillna(0).astype(int)
target = result[['subset_id','subset_name','num_documents']].sort_values(['subset_id','subset_name']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
