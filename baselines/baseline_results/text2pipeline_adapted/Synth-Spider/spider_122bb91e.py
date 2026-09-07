import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'PlanetID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Name_Part1', 'Name_Part2', 'Name_Part3'], 'target_column': 'Name', 'func': "def transform(row):\n    parts = []\n    for k in ['Name_Part1','Name_Part2','Name_Part3']:\n        v = row.get(k)\n        if v is None:\n            continue\n        s = str(v)\n        if s.strip().lower() in ('', 'none', 'null', 'nan'):\n            continue\n        parts.append(s)\n    return ' '.join(parts)"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': "def transform(s):\n    import re\n    if s is None:\n        return ''\n    text = str(s)\n    text = text.strip()\n    text = re.sub(r'\\s+', ' ', text)\n    return text"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['PlanetID', 'Name', 'Coordinates']}, 'table_indices': [0]}], [{'op': 'Concatenate', 'params': {'concatenate_columns': ['Contents1', 'Contents2', 'Contents3', 'Contents4'], 'target_column': 'Contents', 'func': "def transform(row):\n    parts = []\n    for c in [row.get('Contents1'), row.get('Contents2'), row.get('Contents3'), row.get('Contents4')]:\n        if c is None:\n            continue\n        s = str(c)\n        if s.strip().lower() == 'none':\n            continue\n        if s.strip() == '':\n            continue\n        parts.append(s)\n    return ' '.join(parts)"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Contents', 'func': "def transform(s):\n    import re\n    return re.sub(r'\\s+', ' ', str(s).strip())"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Shipment', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PackageNumber', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Sender', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Recipient', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Weight', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Shipment', 'PackageNumber', 'Weight', 'Sender', 'Recipient', 'Contents']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'EmployeeID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Salary', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Name', 'target_columns': ['Name', 'Name_lc'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return [s, s.lower()]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['EmployeeID', 'Name', 'Name_lc', 'Position', 'Salary', 'Remarks']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Employee', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Planet', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Level', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Employee', 'Planet', 'Level']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['PlanetID'] = pd.to_numeric(tmp_0['PlanetID'], errors='coerce').fillna(0).astype(int)
    # Step 2: Concatenate
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(row):\n    parts = []\n    for k in ['Name_Part1','Name_Part2','Name_Part3']:\n        v = row.get(k)\n        if v is None:\n            continue\n        s = str(v)\n        if s.strip().lower() in ('', 'none', 'null', 'nan'):\n            continue\n        parts.append(s)\n    return ' '.join(parts)", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_1['Name'] = tmp_1[['Name_Part1', 'Name_Part2', 'Name_Part3']].apply(_concat_func_1, axis=1)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    if s is None:\n        return ''\n    text = str(s)\n    text = text.strip()\n    text = re.sub(r'\\s+', ' ', text)\n    return text", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Name'] = tmp_2['Name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['PlanetID', 'Name', 'Coordinates']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    parts = []\n    for c in [row.get('Contents1'), row.get('Contents2'), row.get('Contents3'), row.get('Contents4')]:\n        if c is None:\n            continue\n        s = str(c)\n        if s.strip().lower() == 'none':\n            continue\n        if s.strip() == '':\n            continue\n        parts.append(s)\n    return ' '.join(parts)", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['Contents'] = tmp_0[['Contents1', 'Contents2', 'Contents3', 'Contents4']].apply(_concat_func_1, axis=1)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    return re.sub(r'\\s+', ' ', str(s).strip())", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['Contents'] = tmp_1['Contents'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Shipment'] = pd.to_numeric(tmp_2['Shipment'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['PackageNumber'] = pd.to_numeric(tmp_3['PackageNumber'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Sender'] = pd.to_numeric(tmp_4['Sender'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Recipient'] = pd.to_numeric(tmp_5['Recipient'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['Weight'] = pd.to_numeric(tmp_6['Weight'], errors='coerce').astype(float)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['Shipment', 'PackageNumber', 'Weight', 'Sender', 'Recipient', 'Contents']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['EmployeeID'] = pd.to_numeric(tmp_0['EmployeeID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Salary'] = pd.to_numeric(tmp_1['Salary'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['Name'] = tmp_2['Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return [s, s.lower()]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_3['Name'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['Name'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['Name_lc'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['EmployeeID', 'Name', 'Name_lc', 'Position', 'Salary', 'Remarks']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Employee'] = pd.to_numeric(tmp_0['Employee'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Planet'] = pd.to_numeric(tmp_1['Planet'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Level'] = pd.to_numeric(tmp_2['Level'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['Employee', 'Planet', 'Level']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge employee-planet with planet names
integrated = prepared_table_4.merge(prepared_table_1, how='left', left_on='Planet', right_on='PlanetID')
# Employees linked to Omicron Persei 8
mask_ope8 = integrated['Name'].fillna('').str.strip().str.casefold().eq('omicron persei 8')
employees_on_planet = integrated.loc[mask_ope8, ['Employee']].drop_duplicates()
# Link shipments where either Sender or Recipient is an employee on that planet
ship_link_sender = prepared_table_2.merge(employees_on_planet, how='inner', left_on='Sender', right_on='Employee')
ship_link_recipient = prepared_table_2.merge(employees_on_planet, how='inner', left_on='Recipient', right_on='Employee')
ship_on_planet = __import__('pandas').concat([
    ship_link_sender[['Shipment','PackageNumber']].drop_duplicates(),
    ship_link_recipient[['Shipment','PackageNumber']].drop_duplicates()
], ignore_index=True).drop_duplicates()
# Identify Zapp Brannigan by name (case-insensitive contains) and link to shipments sent by him
employees_named = prepared_table_3.copy()
employees_named['Name_lc'] = employees_named['Name'].fillna('').str.strip().str.casefold()
mask_zapp = employees_named['Name_lc'].str.contains('zapp') & employees_named['Name_lc'].str.contains('brannigan')
zapp_ids = employees_named.loc[mask_zapp, ['EmployeeID']].drop_duplicates()
ship_by_zapp = prepared_table_2.merge(zapp_ids, how='inner', left_on='Sender', right_on='EmployeeID')
ship_by_zapp_keys = ship_by_zapp[['Shipment','PackageNumber']].drop_duplicates()
# Union of package keys to avoid double counting
union_keys = __import__('pandas').concat([
    ship_on_planet[['Shipment','PackageNumber']].drop_duplicates(),
    ship_by_zapp_keys
], ignore_index=True).drop_duplicates()
# If union empty, relax planet match to partial contains
if union_keys.shape[0] == 0:
    mask_relaxed = integrated['Name'].fillna('').str.casefold().str.contains('omicron') & integrated['Name'].fillna('').str.casefold().str.contains('persei')
    employees_relaxed = integrated.loc[mask_relaxed, ['Employee']].drop_duplicates()
    ship_link_sender_r = prepared_table_2.merge(employees_relaxed, how='inner', left_on='Sender', right_on='Employee')
    ship_link_recipient_r = prepared_table_2.merge(employees_relaxed, how='inner', left_on='Recipient', right_on='Employee')
    ship_on_planet_r = __import__('pandas').concat([
        ship_link_sender_r[['Shipment','PackageNumber']].drop_duplicates(),
        ship_link_recipient_r[['Shipment','PackageNumber']].drop_duplicates()
    ], ignore_index=True).drop_duplicates()
    union_keys = __import__('pandas').concat([ship_on_planet_r, ship_by_zapp_keys], ignore_index=True).drop_duplicates()
# Final count
if union_keys.shape[0] == 0:
    target = __import__('pandas').DataFrame({'number_of_packages': [0]})
else:
    target = __import__('pandas').DataFrame({'number_of_packages': [union_keys.shape[0]]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
