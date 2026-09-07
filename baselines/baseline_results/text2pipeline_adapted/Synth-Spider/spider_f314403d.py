import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'invoice_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'invoice_date', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'invoice_status_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['invoice_number', 'invoice_status_code', 'invoice_date']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'shipment_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'invoice_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'shipment_tracking_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'shipment_date', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['shipment_id', 'order_id', 'invoice_number', 'shipment_tracking_number', 'shipment_date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['invoice_number'] = pd.to_numeric(tmp_0['invoice_number'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['invoice_date'] = pd.to_datetime(tmp_1['invoice_date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['invoice_status_code'] = tmp_2['invoice_status_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['invoice_number', 'invoice_status_code', 'invoice_date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['shipment_id'] = pd.to_numeric(tmp_0['shipment_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['order_id'] = pd.to_numeric(tmp_1['order_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['invoice_number'] = pd.to_numeric(tmp_2['invoice_number'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['shipment_tracking_number'] = pd.to_numeric(tmp_3['shipment_tracking_number'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['shipment_date'] = pd.to_datetime(tmp_4['shipment_date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['shipment_id', 'order_id', 'invoice_number', 'shipment_tracking_number', 'shipment_date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2[['invoice_number','shipment_date']], on='invoice_number', how='inner')
result = integrated[['invoice_number','invoice_status_code','invoice_date','shipment_date']]
result = result.sort_values(['invoice_number','shipment_date'], kind='mergesort')
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
