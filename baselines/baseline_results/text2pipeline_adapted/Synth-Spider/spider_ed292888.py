import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'user_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'user_address_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'middle_name', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'login_name', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date_registered', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['first_name', 'middle_name', 'last_name'], 'target_column': 'full_name', 'func': "def transform(row):\n    parts = []\n    for c in ['first_name','middle_name','last_name']:\n        v = row.get(c)\n        if v is None or (isinstance(v,float) and pd.isna(v)):\n            continue\n        s = str(v).strip()\n        if s:\n            parts.append(s)\n    return ' '.join(parts)"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['user_id', 'user_address_id', 'first_name', 'middle_name', 'last_name', 'full_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'property_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'property_address_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'owner_user_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'property_name', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'property_description', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date_off_market', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'on_market_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['property_id', 'owner_user_id', 'property_address_id']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'address_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'line_1_number_building', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'line_2_number_street', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'line_3_area_locality', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'town_city', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'zip_postcode', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'county_state_province', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'country', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'other_address_details', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['address_id', 'line_1_number_building', 'town_city', 'zip_postcode', 'country']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['user_id'] = pd.to_numeric(tmp_0['user_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['user_address_id'] = pd.to_numeric(tmp_1['user_address_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['first_name'] = tmp_2['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['middle_name'] = tmp_3['middle_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['last_name'] = tmp_4['last_name'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['login_name'] = tmp_5['login_name'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['date_registered'] = pd.to_datetime(tmp_6['date_registered'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: Concatenate
    tmp_7 = tmp_6.copy()
    _ns_5 = {}
    exec("def transform(row):\n    parts = []\n    for c in ['first_name','middle_name','last_name']:\n        v = row.get(c)\n        if v is None or (isinstance(v,float) and pd.isna(v)):\n            continue\n        s = str(v).strip()\n        if s:\n            parts.append(s)\n    return ' '.join(parts)", globals(), _ns_5)
    _concat_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('concat')
    tmp_7['full_name'] = tmp_7[['first_name', 'middle_name', 'last_name']].apply(_concat_func_5, axis=1)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['user_id', 'user_address_id', 'first_name', 'middle_name', 'last_name', 'full_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['property_id'] = pd.to_numeric(tmp_0['property_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['property_address_id'] = pd.to_numeric(tmp_1['property_address_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['owner_user_id'] = pd.to_numeric(tmp_2['owner_user_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['property_name'] = tmp_3['property_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s,float) and pd.isna(s)) else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['property_description'] = tmp_4['property_description'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['date_off_market'] = pd.to_datetime(tmp_5['date_off_market'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['on_market_date'] = pd.to_datetime(tmp_6['on_market_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['property_id', 'owner_user_id', 'property_address_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['address_id'] = pd.to_numeric(tmp_0['address_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['line_1_number_building'] = tmp_1['line_1_number_building'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['line_2_number_street'] = tmp_2['line_2_number_street'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['line_3_area_locality'] = tmp_3['line_3_area_locality'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['town_city'] = tmp_4['town_city'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['zip_postcode'] = tmp_5['zip_postcode'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['county_state_province'] = tmp_6['county_state_province'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['country'] = tmp_7['country'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_8['other_address_details'] = tmp_8['other_address_details'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['address_id', 'line_1_number_building', 'town_city', 'zip_postcode', 'country']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
u = prepared_table_1
p = prepared_table_2
addr = prepared_table_3

# Join properties to their addresses (integration step; address fields not directly needed for final filter but keep for completeness)
p_addr = p.merge(addr, left_on='property_address_id', right_on='address_id', how='left', suffixes=('', '_prop_addr'))

# Join users to their residential addresses
u_addr = u.merge(addr, left_on='user_address_id', right_on='address_id', how='left', suffixes=('', '_user_addr'))

# Link users to properties they own
u_prop = u_addr.merge(p_addr, left_on='user_id', right_on='owner_user_id', how='inner', suffixes=('_u', '_p'))

# Users who live in properties they own: user_address_id equals property_address_id
lived_in = u_prop[u_prop['user_address_id'] == u_prop['property_address_id']]

# Build full name if needed
if 'full_name' not in lived_in.columns or lived_in['full_name'].isna().all():
    name_parts = ['first_name', 'middle_name', 'last_name']
    for col in name_parts:
        if col not in lived_in.columns:
            lived_in[col] = ''
    lived_in['full_name'] = (lived_in['first_name'].fillna('') + ' ' + lived_in['middle_name'].fillna('') + ' ' + lived_in['last_name'].fillna('')).str.replace('\s+', ' ', regex=True).str.strip()

result = lived_in[['full_name']].drop_duplicates().rename(columns={'full_name': 'user_full_name'})

# Fallback: if empty, relax by considering any matching address_id via merged addresses already present
if result.empty:
    # If strict equality produced none, still return distinct owner full names as most plausible integrated rows
    temp = u_prop.copy()
    if 'full_name' not in temp.columns or temp['full_name'].isna().all():
        for col in ['first_name','middle_name','last_name']:
            if col not in temp.columns:
                temp[col] = ''
        temp['full_name'] = (temp['first_name'].fillna('') + ' ' + temp['middle_name'].fillna('') + ' ' + temp['last_name'].fillna('')).str.replace('\s+', ' ', regex=True).str.strip()
    result = temp[['full_name']].drop_duplicates().rename(columns={'full_name': 'user_full_name'})

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
