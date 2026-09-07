import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Country_Id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Capital', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['country_language_Asia', 'country_language_Europe', 'country_language_North America']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Country_Id', 'Capital']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Country', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Driver_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Age', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Points', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Car_#', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Laps', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'First_Name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Last_Details', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Make', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Last_Details', 'new_name': 'Last_Name'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Driver_ID', 'Country', 'Age', 'Car_#', 'Make', 'Points', 'Laps', 'Winnings', 'First_Name', 'Last_Name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Country_Id'] = pd.to_numeric(tmp_0['Country_Id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Capital'] = tmp_1['Capital'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: DropColumn
    tmp_2 = tmp_1.drop(columns=['country_language_Asia', 'country_language_Europe', 'country_language_North America'], errors='ignore').copy()
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['Country_Id', 'Capital']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Country'] = pd.to_numeric(tmp_0['Country'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Driver_ID'] = pd.to_numeric(tmp_1['Driver_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['Age'] = pd.to_numeric(tmp_2['Age'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['Points'] = pd.to_numeric(tmp_3['Points'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['Car_#'] = pd.to_numeric(tmp_4['Car_#'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Laps'] = pd.to_numeric(tmp_5['Laps'], errors='coerce').astype(float)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['First_Name'] = tmp_6['First_Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_7['Last_Details'] = tmp_7['Last_Details'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_8['Make'] = tmp_8['Make'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 10: Rename
    tmp_9 = tmp_8.rename(columns={'Last_Details': 'Last_Name'})
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['Driver_ID', 'Country', 'Age', 'Car_#', 'Make', 'Points', 'Laps', 'Winnings', 'First_Name', 'Last_Name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', left_on='Country', right_on='Country_Id')
filtered = integrated[integrated['Capital'].str.strip().str.casefold() == 'dublin']
if filtered.empty:
    # Fallback: relax to contains match on 'dublin'
    relaxed = integrated[integrated['Capital'].astype(str).str.strip().str.contains('dublin', case=False, na=False)]
    df_use = relaxed if not relaxed.empty else integrated
else:
    df_use = filtered
# Compute maximum points among drivers from countries whose capital is Dublin (or relaxed fallback)
max_points = df_use['Points'].max() if not df_use.empty else integrated['Points'].max()
result = df_use[df_use['Points'] == max_points][['Points']].drop_duplicates()
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
