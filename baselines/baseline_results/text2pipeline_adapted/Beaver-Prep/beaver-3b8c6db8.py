import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'FCLT_BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME_LONG', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_TYPE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_BUILT', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_OF_ROOMS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'DATE_BUILT', 'BUILDING_TYPE', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'STREET_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'STREET_SUFFIX', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CITY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'STATE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FCLT_BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'FCLT_BUILDING_ADDRESS_KEY', 'ADDRESS_PURPOSE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ROOM_COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'ROOM_COUNTER']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BUILDING_NUMBER'] = tmp_1['BUILDING_NUMBER'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['BUILDING_NAME'] = tmp_2['BUILDING_NAME'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['BUILDING_NAME_LONG'] = tmp_3['BUILDING_NAME_LONG'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['BUILDING_TYPE'] = tmp_4['BUILDING_TYPE'].astype(str)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['DATE_BUILT'] = pd.to_datetime(tmp_5['DATE_BUILT'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['EXT_GROSS_AREA'] = pd.to_numeric(tmp_6['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['NUM_OF_ROOMS'] = pd.to_numeric(tmp_7['NUM_OF_ROOMS'], errors='coerce').fillna(0).astype(int)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'DATE_BUILT', 'BUILDING_TYPE', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['STREET_NAME'] = tmp_0['STREET_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['STREET_SUFFIX'] = tmp_1['STREET_SUFFIX'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['CITY'] = tmp_2['CITY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['STATE'] = tmp_3['STATE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['FCLT_BUILDING_KEY'] = tmp_4['FCLT_BUILDING_KEY'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['BUILDING_NUMBER'] = tmp_5['BUILDING_NUMBER'].astype(str)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'FCLT_BUILDING_ADDRESS_KEY', 'ADDRESS_PURPOSE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_8', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ROOM_COUNTER'] = pd.to_numeric(tmp_1['ROOM_COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'ROOM_COUNTER']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b = prepared_table_1.copy()
addr = prepared_table_2.copy()
rooms = prepared_table_3.copy()
# Count addresses per building (distinct address key per building)
addr_counts = addr.groupby('FCLT_BUILDING_KEY', as_index=False)['FCLT_BUILDING_ADDRESS_KEY'].nunique()
addr_counts = addr_counts.rename(columns={'FCLT_BUILDING_ADDRESS_KEY': 'address_count'})
# Sum total rooms per building using ROOM_COUNTER
room_counts = rooms.groupby('BUILDING_KEY', as_index=False)['ROOM_COUNTER'].sum()
room_counts = room_counts.rename(columns={'BUILDING_KEY': 'FCLT_BUILDING_KEY', 'ROOM_COUNTER': 'total_rooms'})
# Merge buildings with address counts and room counts
integrated = b.merge(addr_counts, on='FCLT_BUILDING_KEY', how='left').merge(room_counts, on='FCLT_BUILDING_KEY', how='left')
# Compute average gross area across all buildings (scalar), then attach as a column for context
avg_gross = integrated['EXT_GROSS_AREA'].mean()
integrated['average_gross_area'] = avg_gross
# Final select and sort by building name
cols = ['BUILDING_NAME', 'BUILDING_NUMBER', 'DATE_BUILT', 'BUILDING_TYPE', 'address_count', 'average_gross_area', 'NUM_OF_ROOMS']
# If address_count or total_rooms are missing, fill with 0 for counts, but keep NUM_OF_ROOMS as provided per building
integrated['address_count'] = integrated['address_count'].fillna(0).astype(int)
# Prefer NUM_OF_ROOMS from buildings as the requested "total number of rooms in each building"; if missing, fallback to aggregated total_rooms
integrated['total_rooms_final'] = integrated['NUM_OF_ROOMS']
mask_missing = integrated['total_rooms_final'].isna() & integrated['total_rooms'].notna()
integrated.loc[mask_missing, 'total_rooms_final'] = integrated.loc[mask_missing, 'total_rooms']
# Prepare target with required columns and rename total rooms column
target = integrated[['BUILDING_NAME', 'BUILDING_NUMBER', 'DATE_BUILT', 'BUILDING_TYPE', 'address_count', 'average_gross_area', 'total_rooms_final']].rename(columns={'total_rooms_final': 'total_rooms'}).sort_values(by='BUILDING_NAME', kind='mergesort').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
