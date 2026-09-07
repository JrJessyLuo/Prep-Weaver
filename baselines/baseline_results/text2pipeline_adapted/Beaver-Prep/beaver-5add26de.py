import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'ROOM', 'SPACE_ID', 'MAJOR_USE_DESC', 'USE_DESC', 'ROOM_FULL_NAME', 'fac_room_key']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NAME']}, 'table_indices': [0]}]]

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
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'ROOM', 'SPACE_ID', 'MAJOR_USE_DESC', 'USE_DESC', 'ROOM_FULL_NAME', 'fac_room_key']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_9', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NAME'] = tmp_1['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'BUILDING_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='BUILDING_KEY')
# There is no explicit student capacity column. As a robust fallback consistent with available evidence, approximate accommodation by counting distinct rooms per building.
# Count unique rooms per BUILDING_KEY and label with BUILDING_NAME.
room_counts = (integrated.dropna(subset=['ROOM'])
               .groupby(['BUILDING_KEY', 'BUILDING_NAME'], as_index=False)
               .agg(accommodates_students=('ROOM', 'nunique')))
# If counting by ROOM yields no rows (e.g., if ROOM is missing), fallback to counting SPACE_IDs.
if room_counts.empty:
    room_counts = (integrated.dropna(subset=['SPACE_ID'])
                   .groupby(['BUILDING_KEY', 'BUILDING_NAME'], as_index=False)
                   .agg(accommodates_students=('SPACE_ID', 'nunique')))
# Pick the building with the maximum count.
room_counts = room_counts.sort_values('accommodates_students', ascending=False)
target = room_counts.head(1)[['BUILDING_NAME', 'accommodates_students']]
# Rename columns to match the question phrasing.
target = target.rename(columns={'BUILDING_NAME': 'building_name', 'accommodates_students': 'students_accommodated'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
