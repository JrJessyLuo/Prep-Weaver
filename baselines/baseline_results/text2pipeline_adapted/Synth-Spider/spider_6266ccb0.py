import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'StuID', 'new_name': 'attribute_name'}, {'old_name': 'student_id', 'new_name': 'student_id_raw'}, {'old_name': 'attribute_value', 'new_name': 'attribute_value'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute_name', 'func': 'def transform(s):\n    # Trim whitespace but preserve original casing\n    return "" if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'student_id_raw', 'func': 'def transform(s):\n    # Remove surrounding double quotes if present and trim whitespace\n    if s is None:\n        return ""\n    s = str(s).strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'student_id_raw', 'target_columns': ['student_id_str', 'student_id'], 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    sval = s\n    ival = None\n    try:\n        # treat empty string or non-numeric as None for integer\n        s_stripped = s.strip()\n        if s_stripped != "":\n            ival = int(float(s_stripped)) if s_stripped.replace(\'.\', \'\', 1).isdigit() else None\n    except Exception:\n        ival = None\n    return [sval, ival]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'student_id_str', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'student_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['student_id_str', 'student_id', 'attribute_name', 'attribute_value']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'city_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'state_country', 'target_columns': ['state_region', 'country_raw'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('~', 1)\n    left = parts[0].strip() if len(parts) > 0 else ''\n    right = parts[1].strip() if len(parts) > 1 else ''\n    return [left, right]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'country_raw', 'func': "def transform(s):\n    val = str(s).strip()\n    mapping = {\n        'U.S.A.': 'USA'\n    }\n    return mapping.get(val, val)"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'country_raw', 'new_name': 'country'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['city_code', 'city_name', 'latitude', 'longitude', 'state_region', 'country']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'StuID': 'attribute_name', 'student_id': 'student_id_raw', 'attribute_value': 'attribute_value'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace but preserve original casing\n    return "" if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['attribute_name'] = tmp_1['attribute_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Remove surrounding double quotes if present and trim whitespace\n    if s is None:\n        return ""\n    s = str(s).strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['student_id_raw'] = tmp_2['student_id_raw'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    sval = s\n    ival = None\n    try:\n        # treat empty string or non-numeric as None for integer\n        s_stripped = s.strip()\n        if s_stripped != "":\n            ival = int(float(s_stripped)) if s_stripped.replace(\'.\', \'\', 1).isdigit() else None\n    except Exception:\n        ival = None\n    return [sval, ival]', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['student_id_raw'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['student_id_str'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['student_id'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['student_id_str'] = tmp_4['student_id_str'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['student_id'] = pd.to_numeric(tmp_5['student_id'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['student_id_str', 'student_id', 'attribute_name', 'attribute_value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['city_name'] = tmp_0['city_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('~', 1)\n    left = parts[0].strip() if len(parts) > 0 else ''\n    right = parts[1].strip() if len(parts) > 1 else ''\n    return [left, right]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['state_country'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['state_region'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['country_raw'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    val = str(s).strip()\n    mapping = {\n        'U.S.A.': 'USA'\n    }\n    return mapping.get(val, val)", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['country_raw'] = tmp_2['country_raw'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'country_raw': 'country'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['city_code', 'city_name', 'latitude', 'longitude', 'state_region', 'country']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()

# Prepare lowercase helpers
t1['attr_lower'] = t1['attribute_name'].astype(str).str.strip().str.lower()
t1['val_lower'] = t1['attribute_value'].astype(str).str.strip().str.lower()

# 1) Direct country attribution to China
mask_country_attr = t1['attr_lower'].str.contains('country|nation|residence|location', na=False)
mask_china_val = t1['val_lower'].str.contains('china|prc|people\'s republic of china|cn', na=False)
direct_china = t1[mask_country_attr & mask_china_val][['student_id_str']].drop_duplicates()

# 2) City-based inference via prepared_table_2 mapping to country
city_ref = prepared_table_2.copy()
city_ref['city_name_l'] = city_ref['city_name'].astype(str).str.strip().str.lower()
city_ref['country_l'] = city_ref['country'].astype(str).str.strip().str.lower()

mask_city_attr = t1['attr_lower'].str.contains('city|hometown|home town|current city', na=False)
city_attr_rows = t1[mask_city_attr].copy()
city_attr_rows['city_name_l'] = city_attr_rows['attribute_value'].astype(str).str.strip().str.lower()

city_join = city_attr_rows.merge(city_ref[['city_name_l','country_l']], on='city_name_l', how='left')
city_china = city_join[city_join['country_l'].str.lower() == 'china'][['student_id_str']].drop_duplicates()

# Union via concat to avoid deprecated append
all_students_china = (
    pd.concat([direct_china, city_china], ignore_index=True)
    .drop_duplicates()
)

# If still empty, attempt broader heuristic: any attribute_value mentioning China
if all_students_china.empty:
    broad = t1[t1['val_lower'].str.contains('china', na=False)][['student_id_str']].drop_duplicates()
    all_students_china = pd.concat([all_students_china, broad], ignore_index=True).drop_duplicates()

# Build final single-row DataFrame with the count
count_val = int(all_students_china['student_id_str'].nunique()) if 'student_id_str' in all_students_china.columns and not all_students_china.empty else 0

target = pd.DataFrame({'answer': [count_val]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
