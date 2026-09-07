import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Receipt', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Ordinal', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Attribute', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Value', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Value', 'target_columns': ['item_p1', 'item_p2', 'item_p3', 'item_p4', 'item_p5'], 'func': "def transform(s):\n    try:\n        parts = str(s).split('-') if s is not None else []\n    except Exception:\n        parts = []\n    parts = parts[:5]\n    while len(parts) < 5:\n        parts.append(None)\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'item_p1', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'item_p2', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'item_p3', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'item_p4', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'item_p5', 'func': 'def transform(s):\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'item_p1', 'new_name': 'Id_Part1'}, {'old_name': 'item_p2', 'new_name': 'Id_Part2'}, {'old_name': 'item_p3', 'new_name': 'Id_Part3'}, {'old_name': 'item_p4', 'new_name': 'Id_Part4'}, {'old_name': 'item_p5', 'new_name': 'Id_Part5'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Receipt', 'Ordinal', 'Attribute', 'Value', 'Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Price', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Id_Part1', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Id_Part2', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Id_Part3', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Id_Part4', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Id_Part5', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Flavor', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Food', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Flavor', 'Food', 'Price', 'Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Receipt'] = tmp_0['Receipt'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Ordinal'] = tmp_1['Ordinal'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Attribute'] = tmp_2['Attribute'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Value'] = tmp_3['Value'].astype(str)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec("def transform(s):\n    try:\n        parts = str(s).split('-') if s is not None else []\n    except Exception:\n        parts = []\n    parts = parts[:5]\n    while len(parts) < 5:\n        parts.append(None)\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_4['Value'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['item_p1'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['item_p2'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_4['item_p3'] = _split_values_1.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    tmp_4['item_p4'] = _split_values_1.apply(lambda x: x[3] if len(x) > 3 else pd.NA)
    tmp_4['item_p5'] = _split_values_1.apply(lambda x: x[4] if len(x) > 4 else pd.NA)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['item_p1'] = tmp_5['item_p1'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['item_p2'] = tmp_6['item_p2'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_7['item_p3'] = tmp_7['item_p3'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_8['item_p4'] = tmp_8['item_p4'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return None if s is None else str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_9['item_p5'] = tmp_9['item_p5'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 11: Rename
    tmp_10 = tmp_9.rename(columns={'item_p1': 'Id_Part1', 'item_p2': 'Id_Part2', 'item_p3': 'Id_Part3', 'item_p4': 'Id_Part4', 'item_p5': 'Id_Part5'})
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['Receipt', 'Ordinal', 'Attribute', 'Value', 'Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Price'] = pd.to_numeric(tmp_0['Price'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Id_Part1'] = tmp_1['Id_Part1'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Id_Part2'] = tmp_2['Id_Part2'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['Id_Part3'] = tmp_3['Id_Part3'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['Id_Part4'] = tmp_4['Id_Part4'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    return None if s == '' or s.lower() == 'none' else s", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['Id_Part5'] = tmp_5['Id_Part5'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['Flavor'] = tmp_6['Flavor'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['Food'] = tmp_7['Food'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['Flavor', 'Food', 'Price', 'Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()
# Keep only item attribute rows for joining
items = t1[t1['Attribute'].str.lower() == 'item']
# Ensure join keys are strings and handle null-like 'None'
for c in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    if c in items.columns:
        items[c] = items[c].astype(object).where(~items[c].isin(['None', 'none', 'NULL', 'null', 'NaN', 'nan', '']), None)

menu = prepared_table_2.copy()
for c in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    if c in menu.columns:
        menu[c] = menu[c].astype(object).where(~menu[c].isin(['None', 'none', 'NULL', 'null', 'NaN', 'nan', '']), None)

# Join on all ID parts
merged = items.merge(
    menu,
    how='inner',
    on=['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']
)
# Filter to goods costing more than 13 dollars
merged = merged[pd.to_numeric(merged['Price'], errors='coerce') > 13]
# Distinct receipt numbers
target = merged[['Receipt']].drop_duplicates().sort_values('Receipt').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
