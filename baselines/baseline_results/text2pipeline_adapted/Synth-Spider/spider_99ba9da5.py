import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'NumberWithQuoteSuffix', 'target_columns': ['NumberWithQuoteSuffix_clean'], 'func': 'def transform(s):\n    # remove a single trailing quote if present\n    return [str(s)[:-1] if str(s).endswith(\'"\') else str(s)]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NumberWithQuoteSuffix_clean', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Capacity', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'NumberWithQuoteSuffix_clean', 'new_name': 'warehouse_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['warehouse_id', 'Capacity', 'Location']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'wh', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'wh', 'new_name': 'warehouse_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Code', 'cts', 'vl', 'warehouse_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # remove a single trailing quote if present\n    return [str(s)[:-1] if str(s).endswith(\'"\') else str(s)]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['NumberWithQuoteSuffix'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['NumberWithQuoteSuffix_clean'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['NumberWithQuoteSuffix_clean'] = pd.to_numeric(tmp_1['NumberWithQuoteSuffix_clean'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Capacity'] = pd.to_numeric(tmp_2['Capacity'], errors='coerce').fillna(0).astype(int)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'NumberWithQuoteSuffix_clean': 'warehouse_id'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['warehouse_id', 'Capacity', 'Location']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['wh'] = pd.to_numeric(tmp_0['wh'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'wh': 'warehouse_id'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Code', 'cts', 'vl', 'warehouse_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='warehouse_id')
# Compute load per warehouse as the count of item rows per warehouse
warehouse_loads = integrated.groupby(['warehouse_id', 'Capacity'], as_index=False).size().rename(columns={'size': 'load'})
# Identify warehouses where load exceeds capacity
above_capacity = warehouse_loads[warehouse_loads['load'] > warehouse_loads['Capacity']]
# Get the codes (warehouse identifiers) for those warehouses
target = above_capacity[['warehouse_id']].rename(columns={'warehouse_id': 'Code'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
