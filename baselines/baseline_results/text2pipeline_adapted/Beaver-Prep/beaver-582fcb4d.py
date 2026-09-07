import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME_LONG', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SITE', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_TYPE', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNERSHIP_TYPE', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_OCCUPIED', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILDING_TYPE', 'OWNERSHIP_TYPE', 'DATE_OCCUPIED', 'SITE', 'PARENT_BUILDING_NUMBER']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    # Trim outer whitespace but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_STREET_ADDRESS', 'func': 'def transform(s):\n    # Normalize internal spacing: collapse multiple spaces to single, trim ends; preserve case/content\n    import re\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'BUILDING_STREET_ADDRESS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_NUMBER'] = tmp_0['BUILDING_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NAME_LONG'] = tmp_1['BUILDING_NAME_LONG'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SITE'] = tmp_2['SITE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['BUILDING_TYPE'] = tmp_3['BUILDING_TYPE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s).lower() != 'nan' else None", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['OWNERSHIP_TYPE'] = tmp_4['OWNERSHIP_TYPE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['DATE_OCCUPIED'] = pd.to_datetime(tmp_5['DATE_OCCUPIED'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILDING_TYPE', 'OWNERSHIP_TYPE', 'DATE_OCCUPIED', 'SITE', 'PARENT_BUILDING_NUMBER']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim outer whitespace but preserve original case\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_NUMBER'] = tmp_0['BUILDING_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Normalize internal spacing: collapse multiple spaces to single, trim ends; preserve case/content\n    import re\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s)\n    return s.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_STREET_ADDRESS'] = tmp_1['BUILDING_STREET_ADDRESS'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_NUMBER', 'BUILDING_STREET_ADDRESS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='BUILDING_NUMBER')
# Identify non-subdivisions: rows where PARENT_BUILDING_NUMBER is null/blank or '-' like values
non_sub_mask = integrated['PARENT_BUILDING_NUMBER'].isna() | (integrated['PARENT_BUILDING_NUMBER'].astype(str).str.strip().str.len() == 0) | (integrated['PARENT_BUILDING_NUMBER'].astype(str).str.strip().str.upper().isin(['-', 'NAN', 'NONE']))
non_sub = integrated[non_sub_mask].copy()
# Project required columns and rename for clarity per question
non_sub['BUILDING_NUMBER'] = non_sub['BUILDING_NUMBER']
non_sub['FULL_NAME'] = non_sub['BUILDING_NAME_LONG']
non_sub['STREET_ADDRESS'] = non_sub['BUILDING_STREET_ADDRESS']
non_sub['BUILDING_TYPE'] = non_sub['BUILDING_TYPE']
non_sub['OCCUPANCY_DATE'] = non_sub['DATE_OCCUPIED']
non_sub['OWNERSHIP_TYPE'] = non_sub['OWNERSHIP_TYPE']
non_sub['SITE'] = non_sub['SITE']
result_cols = ['BUILDING_NUMBER', 'FULL_NAME', 'STREET_ADDRESS', 'BUILDING_TYPE', 'OCCUPANCY_DATE', 'OWNERSHIP_TYPE', 'SITE']
main_rows = non_sub[result_cols].copy()
# Counts for owned, leased, all (within non-subdivision set)
owned_count = int((non_sub['OWNERSHIP_TYPE'].astype(str).str.strip().str.upper() == 'OWNED').sum())
leased_count = int((non_sub['OWNERSHIP_TYPE'].astype(str).str.strip().str.upper() == 'LEASED').sum())
all_count = int(len(non_sub))
summary_rows = [
    {'BUILDING_NUMBER': None, 'FULL_NAME': f"{owned_count} Buildings", 'STREET_ADDRESS': None, 'BUILDING_TYPE': None, 'OCCUPANCY_DATE': None, 'OWNERSHIP_TYPE': None, 'SITE': None},
    {'BUILDING_NUMBER': None, 'FULL_NAME': f"{leased_count} Buildings", 'STREET_ADDRESS': None, 'BUILDING_TYPE': None, 'OCCUPANCY_DATE': None, 'OWNERSHIP_TYPE': None, 'SITE': None},
    {'BUILDING_NUMBER': None, 'FULL_NAME': f"{all_count} Buildings", 'STREET_ADDRESS': None, 'BUILDING_TYPE': None, 'OCCUPANCY_DATE': None, 'OWNERSHIP_TYPE': None, 'SITE': None}
]
summary_df = pd.DataFrame(summary_rows, columns=result_cols)
target = pd.concat([main_rows, summary_df], ignore_index=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
