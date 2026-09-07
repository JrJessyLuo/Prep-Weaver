import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['FLOOR_KEY', 'EXT_GROSS_AREA', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA', 'FLOOR_SORT_SEQUENCE', 'LEVEL_ID', 'BUILDING_WINGS_ID', 'ACCESS_LEVEL', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['BUILDING_NUMBER', 'BUILDING_STREET_ADDRESS', 'BUILDING_MAILING_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_COUNTER', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['BUILDING_KEY'] = tmp_1['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['FLOOR'] = tmp_2['FLOOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['FLOOR_KEY', 'EXT_GROSS_AREA', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA', 'FLOOR_SORT_SEQUENCE', 'LEVEL_ID', 'BUILDING_WINGS_ID', 'ACCESS_LEVEL', 'WAREHOUSE_LOAD_DATE'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_KEY', 'FLOOR']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BUILDING_NAME'] = tmp_1['BUILDING_NAME'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['BUILDING_KEY'] = tmp_2['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['BUILDING_NAME'] = tmp_3['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: DropColumn
    tmp_4 = tmp_3.drop(columns=['BUILDING_NUMBER', 'BUILDING_STREET_ADDRESS', 'BUILDING_MAILING_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_COUNTER', 'WAREHOUSE_LOAD_DATE'], errors='ignore').copy()
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['BUILDING_KEY', 'BUILDING_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='BUILDING_KEY')
# Count distinct floors per building (use FLOOR as the floor identifier)
floor_counts = integrated.groupby(['BUILDING_KEY', 'BUILDING_NAME'], as_index=False)['FLOOR'].nunique().rename(columns={'FLOOR': 'num_floors'})
# Find the maximum number of floors
max_floors = floor_counts['num_floors'].max()
# Filter buildings that have the maximum number of floors and return their names
target = floor_counts[floor_counts['num_floors'] == max_floors][['BUILDING_NAME']].sort_values('BUILDING_NAME').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
