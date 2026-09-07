import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ORGANIZATION_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPT_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ROOM', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR', 'ORGANIZATION_NAME', 'DEPT_CODE', 'ROOM']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['BUILDING_KEY', 'BUILDING_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_5', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FLOOR'] = tmp_1['FLOOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['ORGANIZATION_NAME'] = tmp_2['ORGANIZATION_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['DEPT_CODE'] = tmp_3['DEPT_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['ROOM'] = tmp_4['ROOM'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['BUILDING_KEY', 'FLOOR', 'ORGANIZATION_NAME', 'DEPT_CODE', 'ROOM']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='BUILDING_KEY', how='left')
# Compute min and max FLOOR per building based on string ordering, preserving mixed labels
floor_agg = integrated.groupby('BUILDING_KEY', as_index=False).agg(lowest_floor=('FLOOR', 'min'), highest_floor=('FLOOR', 'max'))
# Total number of rooms per building (count distinct ROOM entries within a building)
rooms_per_bldg = integrated.groupby('BUILDING_KEY', as_index=False).agg(total_rooms=('ROOM', 'nunique'))
# Aggregate organizations and departments per building (unique, concatenated)
orgs = integrated.groupby('BUILDING_KEY', as_index=False)['ORGANIZATION_NAME'].apply(lambda s: ', '.join(sorted({str(x) for x in s.dropna() if str(x).strip()!=''}))).rename(columns={'ORGANIZATION_NAME':'organizations'})
depts = integrated.groupby('BUILDING_KEY', as_index=False)['DEPT_CODE'].apply(lambda s: ', '.join(sorted({str(x) for x in s.dropna() if str(x).strip()!=''}))).rename(columns={'DEPT_CODE':'department_names'})
# Attach building names
bldg_names = prepared_table_1[['BUILDING_KEY','BUILDING_NAME']].drop_duplicates()
# Merge all pieces
res = bldg_names.merge(floor_agg, on='BUILDING_KEY', how='left').merge(rooms_per_bldg, on='BUILDING_KEY', how='left').merge(orgs, on='BUILDING_KEY', how='left').merge(depts, on='BUILDING_KEY', how='left')
# Final select and order
target = res[['BUILDING_KEY','BUILDING_NAME','department_names','organizations','highest_floor','lowest_floor','total_rooms']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
