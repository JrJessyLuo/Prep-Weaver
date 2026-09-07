import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'product_id', 'target_columns': ['product_id'], 'func': 'def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [val]\n    return [[val]]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'parent_product_id', 'target_columns': ['parent_product_id'], 'func': 'def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [val]\n    return [[val]]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'product_name', 'target_columns': ['product_name'], 'func': 'def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [list(map(str, val))]\n    return [[str(val)]]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'product_price', 'target_columns': ['product_price'], 'func': 'def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [val]\n    return [[val]]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'product_size', 'target_columns': ['product_size'], 'func': 'def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [list(map(str, val))]\n    return [[str(val)]]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'product_description', 'target_columns': ['product_description'], 'func': 'def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [list(map(str, val))]\n    return [[str(val)]]'}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'product_id', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'parent_product_id', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'product_name', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'product_price', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'product_size', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'product_description', 'split_comma': False}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'product_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'parent_product_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'product_price', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'product_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'product_color', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['product_id', 'product_name', 'product_price', 'product_color']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'order_item_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'product_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['status_part1', 'status_part2', 'status_part3'], 'target_column': 'status', 'func': 'def transform(row):\n    parts = []\n    for c in ["status_part1", "status_part2", "status_part3"]:\n        v = row.get(c)\n        if v is None:\n            continue\n        s = str(v)\n        if s.strip().lower() == \'none\' or s.strip() == \'\':\n            continue\n        parts.append(s)\n    return \' \'.join(parts)'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['status_part1', 'status_part2', 'status_part3']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['order_item_id', 'product_id', 'order_id', 'status']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'customer_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['date', 'time'], 'target_column': 'order_datetime', 'func': 'def transform(row):\n    d = str(row[\'date\']).strip() if \'date\' in row else \'\'\n    t = str(row[\'time\']).strip() if \'time\' in row else \'\'\n    if d and t:\n        return f"{d} {t}"\n    return d or t'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['order_id', 'order_status_code', 'order_datetime']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [val]\n    return [[val]]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['product_id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['product_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [val]\n    return [[val]]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['parent_product_id'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['parent_product_id'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [list(map(str, val))]\n    return [[str(val)]]', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_2['product_name'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['product_name'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [val]\n    return [[val]]', globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_3['product_price'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['product_price'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [list(map(str, val))]\n    return [[str(val)]]', globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_4['product_size'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['product_size'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 6: SplitColumn
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    import ast\n    txt = str(s)\n    try:\n        val = ast.literal_eval(txt)\n    except Exception:\n        val = []\n    if isinstance(val, (list, tuple)):\n        return [list(map(str, val))]\n    return [[str(val)]]', globals(), _ns_6)
    _split_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('split')
    _split_values_6 = tmp_5['product_description'].apply(_split_func_6)
    _split_values_6 = _split_values_6.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_5['product_description'] = _split_values_6.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 7: Explode
    tmp_6 = tmp_5.explode('product_id')
    # Step 8: Explode
    tmp_7 = tmp_6.explode('parent_product_id')
    # Step 9: Explode
    tmp_8 = tmp_7.explode('product_name')
    # Step 10: Explode
    tmp_9 = tmp_8.explode('product_price')
    # Step 11: Explode
    tmp_10 = tmp_9.explode('product_size')
    # Step 12: Explode
    tmp_11 = tmp_10.explode('product_description')
    # Step 13: CastType
    tmp_12 = tmp_11.copy()
    tmp_12['product_id'] = pd.to_numeric(tmp_12['product_id'], errors='coerce').fillna(0).astype(int)
    # Step 14: CastType
    tmp_13 = tmp_12.copy()
    tmp_13['parent_product_id'] = pd.to_numeric(tmp_13['parent_product_id'], errors='coerce').fillna(0).astype(int)
    # Step 15: CastType
    tmp_14 = tmp_13.copy()
    tmp_14['product_price'] = pd.to_numeric(tmp_14['product_price'], errors='coerce').astype(float)
    # Step 16: StandardizeString
    tmp_15 = tmp_14.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_15['product_name'] = tmp_15['product_name'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 17: StandardizeString
    tmp_16 = tmp_15.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_16['product_color'] = tmp_16['product_color'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 18: SelectCol
    result = tmp_16.loc[:, ['product_id', 'product_name', 'product_price', 'product_color']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['order_item_id'] = pd.to_numeric(tmp_0['order_item_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['product_id'] = pd.to_numeric(tmp_1['product_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['order_id'] = pd.to_numeric(tmp_2['order_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(row):\n    parts = []\n    for c in ["status_part1", "status_part2", "status_part3"]:\n        v = row.get(c)\n        if v is None:\n            continue\n        s = str(v)\n        if s.strip().lower() == \'none\' or s.strip() == \'\':\n            continue\n        parts.append(s)\n    return \' \'.join(parts)', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_3['status'] = tmp_3[['status_part1', 'status_part2', 'status_part3']].apply(_concat_func_1, axis=1)
    # Step 5: DropColumn
    tmp_4 = tmp_3.drop(columns=['status_part1', 'status_part2', 'status_part3'], errors='ignore').copy()
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['order_item_id', 'product_id', 'order_id', 'status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['order_id'] = pd.to_numeric(tmp_0['order_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['customer_id'] = pd.to_numeric(tmp_1['customer_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(row):\n    d = str(row[\'date\']).strip() if \'date\' in row else \'\'\n    t = str(row[\'time\']).strip() if \'time\' in row else \'\'\n    if d and t:\n        return f"{d} {t}"\n    return d or t', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_2['order_datetime'] = tmp_2[['date', 'time']].apply(_concat_func_1, axis=1)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['order_id', 'order_status_code', 'order_datetime']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
prod = prepared_table_1
items = prepared_table_2
# Count distinct orders per product_id
order_counts = items.groupby('product_id', as_index=False)['order_id'].nunique().rename(columns={'order_id':'order_count'})
# Left join products to counts so products with zero appearances are included with NaN -> 0
prod_with_counts = prod.merge(order_counts, on='product_id', how='left')
prod_with_counts['order_count'] = prod_with_counts['order_count'].fillna(0)
# Filter products listed in less than two orders (i.e., order_count < 2)
result = prod_with_counts[prod_with_counts['order_count'] < 2]
# Final projection: ids, names, prices, colors
target = result[['product_id', 'product_name', 'product_price', 'product_color']].copy()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
