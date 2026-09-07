import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'PlanetID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['Coordinates']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['PlanetID', 'Name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ShipmentID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Planet', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Planet', 'new_name': 'PlanetID'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ShipmentID', 'PlanetID']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Shipment', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Weight', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Shipment', 'Weight']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['PlanetID'] = pd.to_numeric(tmp_0['PlanetID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Name'] = tmp_1['Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: DropColumn
    tmp_2 = tmp_1.drop(columns=['Coordinates'], errors='ignore').copy()
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['PlanetID', 'Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ShipmentID'] = pd.to_numeric(tmp_0['ShipmentID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Planet'] = pd.to_numeric(tmp_1['Planet'], errors='coerce').fillna(0).astype(int)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'Planet': 'PlanetID'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ShipmentID', 'PlanetID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Shipment'] = pd.to_numeric(tmp_0['Shipment'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Weight'] = pd.to_numeric(tmp_1['Weight'], errors='coerce').astype(float)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Shipment', 'Weight']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_3.merge(prepared_table_2, left_on='Shipment', right_on='ShipmentID', how='inner').merge(prepared_table_1, left_on='PlanetID', right_on='PlanetID', how='inner')
weights_by_planet = integrated.groupby(['PlanetID', 'Name'], as_index=False)['Weight'].sum()
weights_by_planet = weights_by_planet.rename(columns={'Weight': 'TotalWeight'})
target = weights_by_planet[['Name', 'TotalWeight']].sort_values('Name').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
