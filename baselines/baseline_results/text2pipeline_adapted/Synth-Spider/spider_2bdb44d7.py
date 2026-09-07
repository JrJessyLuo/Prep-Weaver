import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['document_id', 'document_name', 'document_description', 'other_details', 'first_name', 'last_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'document_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'process_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date_from', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date_to', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['document_id', 'process_id', 'staff_id', 'staff_role_code', 'date_from', 'date_to', 'other_details']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['document_id', 'document_name', 'document_description', 'other_details', 'first_name', 'last_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['document_id'] = pd.to_numeric(tmp_0['document_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['process_id'] = pd.to_numeric(tmp_1['process_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date_from'] = pd.to_datetime(tmp_2['date_from'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['date_to'] = pd.to_datetime(tmp_3['date_to'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['document_id', 'process_id', 'staff_id', 'staff_role_code', 'date_from', 'date_to', 'other_details']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2[['document_id','process_id']], on='document_id', how='left')
no_process = integrated[integrated['process_id'].isna()]
target = no_process[['document_id']].drop_duplicates().sort_values('document_id').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
