import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'discount_id'}, {'old_name': 'nm', 'new_name': 'discount_name'}, {'old_name': 'mc', 'new_name': 'min_charge'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'discount_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'min_charge', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'discount_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['discount_id', 'discount_name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'rental_id'}, {'old_name': 'customer_id', 'new_name': 'customer_id'}, {'old_name': 'discount_id', 'new_name': 'discount_id'}, {'old_name': 'vehicles_id', 'new_name': 'vehicle_id'}, {'old_name': 'total_hours', 'new_name': 'total_hours'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rental_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'discount_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'vehicle_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'total_hours', 'func': 'def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        return s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'total_hours', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['rental_id', 'customer_id', 'discount_id', 'vehicle_id', 'total_hours']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'discount_id', 'nm': 'discount_name', 'mc': 'min_charge'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['discount_id'] = pd.to_numeric(tmp_1['discount_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['min_charge'] = pd.to_numeric(tmp_2['min_charge'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['discount_name'] = tmp_3['discount_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['discount_id', 'discount_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'rental_id', 'customer_id': 'customer_id', 'discount_id': 'discount_id', 'vehicles_id': 'vehicle_id', 'total_hours': 'total_hours'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['rental_id'] = pd.to_numeric(tmp_1['rental_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['customer_id'] = pd.to_numeric(tmp_2['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['discount_id'] = pd.to_numeric(tmp_3['discount_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['vehicle_id'] = pd.to_numeric(tmp_4['vehicle_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        return s[1:-1]\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['total_hours'] = tmp_5['total_hours'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['total_hours'] = pd.to_numeric(tmp_6['total_hours'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['rental_id', 'customer_id', 'discount_id', 'vehicle_id', 'total_hours']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', on='discount_id')
counts = integrated.groupby(['discount_id', 'discount_name'], dropna=False).size().reset_index(name='rental_count')
counts_sorted = counts.sort_values(['rental_count', 'discount_name'], ascending=[False, True])
target = counts_sorted[['discount_name']].head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
