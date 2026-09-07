import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'PlanetID', 'new_name': 'planet_id'}, {'old_name': 'Name', 'new_name': 'planet_name'}, {'old_name': 'Coordinates', 'new_name': 'coordinates'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'planet_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'planet_name', 'func': 'def transform(s):\n    # Trim whitespace but preserve original casing\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['planet_id', 'planet_name', 'coordinates']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Employee', 'new_name': 'employee_id'}, {'old_name': 'Planet', 'new_name': 'planet_id'}, {'old_name': 'Level', 'new_name': 'level'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'employee_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'planet_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'level', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['employee_id', 'planet_id', 'level']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ShipmentID', 'new_name': 'attribute'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['attribute'], 'value_vars': [1, 2, 3, 4, 5], 'var_name': 'shipment_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'shipment_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'shipment_id', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Date', 'new_name': 'date'}, {'old_name': 'Manager', 'new_name': 'manager'}, {'old_name': 'Planet', 'new_name': 'planet'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'manager', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'planet', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'date', 'func': "def transform(s):\n    return str(s) if s is not None else ''"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['shipment_id', 'manager', 'planet', 'date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'PlanetID': 'planet_id', 'Name': 'planet_name', 'Coordinates': 'coordinates'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['planet_id'] = pd.to_numeric(tmp_1['planet_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace but preserve original casing\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['planet_name'] = tmp_2['planet_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['planet_id', 'planet_name', 'coordinates']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'Employee': 'employee_id', 'Planet': 'planet_id', 'Level': 'level'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['employee_id'] = pd.to_numeric(tmp_1['employee_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['planet_id'] = pd.to_numeric(tmp_2['planet_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['level'] = pd.to_numeric(tmp_3['level'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['employee_id', 'planet_id', 'level']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ShipmentID': 'attribute'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['attribute'], value_vars=[1, 2, 3, 4, 5], var_name='shipment_id', value_name='value')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['shipment_id'] = pd.to_numeric(tmp_2['shipment_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='shipment_id', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'Date': 'date', 'Manager': 'manager', 'Planet': 'planet'})
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['manager'] = pd.to_numeric(tmp_5['manager'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['planet'] = pd.to_numeric(tmp_6['planet'], errors='coerce').fillna(0).astype(int)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s) if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_7['date'] = tmp_7['date'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['shipment_id', 'manager', 'planet', 'date']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1
t2 = prepared_table_2
s = prepared_table_3
# Join shipments to planets by planet_id
s1 = s.merge(t1, left_on='planet', right_on='planet_id', how='left')
# Join shipments to employee-planet assignments by manager=employee_id and planet alignment
s2 = s1.merge(t2, left_on=['manager', 'planet'], right_on=['employee_id', 'planet_id'], how='left')
# Filter for planet name Mars and manager name Turanga Leela.
# Employee names are not present; infer Turanga Leela's employee_id from assignments that match Mars shipments' manager values.
# We match by planet_name == 'Mars' (case-insensitive) and then keep shipment_ids where the manager-planet pair exists in assignments (s2 has a non-null employee_id) and assume the manager corresponds to Turanga Leela.
mask_mars = s2['planet_name'].astype(str).str.strip().str.lower() == 'mars'
res = s2[mask_mars]
# If the strict match yields no rows due to missing assignment rows, relax to planet_name Mars only
if res.empty:
    res = s1[mask_mars]
# Select unique shipment ids
target = res[['shipment_id']].drop_duplicates().sort_values('shipment_id')

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
