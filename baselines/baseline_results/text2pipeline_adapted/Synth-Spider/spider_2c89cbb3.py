import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Receipt', 'new_name': 'receipt_id'}, {'old_name': 'Ordinal', 'new_name': 'line_number'}, {'old_name': 'Item', 'new_name': 'item'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'receipt_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'line_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'item', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['receipt_id', 'line_number', 'item']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'sjb', 'new_name': 'receipt_id'}, {'old_name': 'Date', 'new_name': 'date'}, {'old_name': 'khid', 'new_name': 'customer_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'receipt_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%d-%b-%Y'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['receipt_id', 'date', 'customer_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Receipt': 'receipt_id', 'Ordinal': 'line_number', 'Item': 'item'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['receipt_id'] = pd.to_numeric(tmp_1['receipt_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['line_number'] = pd.to_numeric(tmp_2['line_number'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['item'] = tmp_3['item'].astype(str)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['receipt_id', 'line_number', 'item']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'sjb': 'receipt_id', 'Date': 'date', 'khid': 'customer_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['receipt_id'] = pd.to_numeric(tmp_1['receipt_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['customer_id'] = pd.to_numeric(tmp_2['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['date'] = pd.to_datetime(tmp_3['date'], errors='coerce').dt.strftime('%d-%b-%Y')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['receipt_id', 'date', 'customer_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='receipt_id')
filtered = integrated[integrated['customer_id'] == 15]
result = filtered[['item']].dropna()
target = result.drop_duplicates().sort_values(by='item').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
