import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['customer_id', 'customer_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'order_date_only', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['order_id', 'customer_id', 'order_status_code', 'order_date_only', 'order_time_only']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['customer_id'] = pd.to_numeric(tmp_0['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['customer_id', 'customer_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['order_id'] = pd.to_numeric(tmp_0['order_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['customer_id'] = pd.to_numeric(tmp_1['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['order_date_only'] = pd.to_datetime(tmp_2['order_date_only'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['order_id', 'customer_id', 'order_status_code', 'order_date_only', 'order_time_only']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='customer_id')
mask = integrated['customer_name'].astype(str).str.strip().str.casefold() == 'jeromy'
filtered = integrated[mask]
if filtered.empty:
    # fallback to partial match on plausible name columns
    mask2 = integrated['customer_name'].astype(str).str.contains('jeromy', case=False, na=False)
    filtered = integrated[mask2]
result = filtered[['order_id', 'order_date_only', 'order_status_code']].copy()
result = result.rename(columns={'order_id': 'id', 'order_date_only': 'date', 'order_status_code': 'status_code'})
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
