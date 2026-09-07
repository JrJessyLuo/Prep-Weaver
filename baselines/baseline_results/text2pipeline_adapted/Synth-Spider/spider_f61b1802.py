import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Institution_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Team', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['City', 'Province', 'Founded', 'Affiliation', 'Metric', 'Value']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Institution_ID', 'Name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Institution_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Nickname', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['Joined_Championships']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Institution_ID', 'Nickname']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Institution_ID'] = pd.to_numeric(tmp_0['Institution_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Name'] = tmp_1['Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Team'] = tmp_2['Team'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['City', 'Province', 'Founded', 'Affiliation', 'Metric', 'Value'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Institution_ID', 'Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Institution_ID'] = pd.to_numeric(tmp_0['Institution_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Nickname'] = tmp_1['Nickname'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: DropColumn
    tmp_2 = tmp_1.drop(columns=['Joined_Championships'], errors='ignore').copy()
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['Institution_ID', 'Nickname']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='Institution_ID')
integrated = integrated.drop_duplicates(subset=['Institution_ID', 'Name', 'Nickname'])
target = integrated[['Name', 'Nickname']].reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
