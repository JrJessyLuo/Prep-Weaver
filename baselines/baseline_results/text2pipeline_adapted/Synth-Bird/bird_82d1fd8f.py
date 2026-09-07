import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SEX', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Admission', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Diagnosis', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'First Date', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'First Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Birthday_Description', 'target_columns': ['Birthdate', 'DescriptionDate'], 'func': "def transform(s):\n    try:\n        if s is None:\n            return [None, None]\n        s_str = str(s)\n        if s_str.lower() == 'nan':\n            return [None, None]\n        parts = s_str.split('|')\n        if len(parts) == 1:\n            return [parts[0].strip() if parts[0] != '' else None, None]\n        left = parts[0].strip() if parts[0].strip() != '' and parts[0].strip().lower() != 'nan' else None\n        right = parts[1].strip() if parts[1].strip() != '' and parts[1].strip().lower() != 'nan' else None\n        return [left, right]\n    except Exception:\n        return [None, None]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'SEX', 'First Date', 'Admission', 'Diagnosis', 'Birthday_Description', 'Birthdate', 'DescriptionDate']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RBC', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'U-PRO', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CRP', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RA', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RF', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RNP', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SM', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SC170', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SSA', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'GOT', 'GPT', 'LDH', 'ALP', 'TP', 'ALB', 'UA', 'UN', 'CRE', 'T-BIL', 'T-CHO', 'TG', 'CPK', 'GLU', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PT', 'APTT', 'FG', 'PIC', 'TAT', 'TAT2', 'U-PRO', 'IGG', 'IGA', 'IGM', 'CRP', 'RA', 'RF', 'C3', 'C4', 'RNP', 'SM', 'SC170', 'SSA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SEX'] = tmp_1['SEX'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Admission'] = tmp_2['Admission'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['Diagnosis'] = tmp_3['Diagnosis'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['First Date'] = tmp_4['First Date'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['First Date'] = pd.to_datetime(tmp_5['First Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: SplitColumn
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec("def transform(s):\n    try:\n        if s is None:\n            return [None, None]\n        s_str = str(s)\n        if s_str.lower() == 'nan':\n            return [None, None]\n        parts = s_str.split('|')\n        if len(parts) == 1:\n            return [parts[0].strip() if parts[0] != '' else None, None]\n        left = parts[0].strip() if parts[0].strip() != '' and parts[0].strip().lower() != 'nan' else None\n        right = parts[1].strip() if parts[1].strip() != '' and parts[1].strip().lower() != 'nan' else None\n        return [left, right]\n    except Exception:\n        return [None, None]", globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_6['Birthday_Description'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_6['Birthdate'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_6['DescriptionDate'] = _split_values_5.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['ID', 'SEX', 'First Date', 'Admission', 'Diagnosis', 'Birthday_Description', 'Birthdate', 'DescriptionDate']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['RBC'] = pd.to_numeric(tmp_2['RBC'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['U-PRO'] = tmp_3['U-PRO'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['CRP'] = tmp_4['CRP'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['RA'] = tmp_5['RA'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_6['RF'] = tmp_6['RF'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_7['RNP'] = tmp_7['RNP'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_8['SM'] = tmp_8['SM'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_9['SC170'] = tmp_9['SC170'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_10['SSA'] = tmp_10['SSA'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['ID', 'Date', 'GOT', 'GPT', 'LDH', 'ALP', 'TP', 'ALB', 'UA', 'UN', 'CRE', 'T-BIL', 'T-CHO', 'TG', 'CPK', 'GLU', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PT', 'APTT', 'FG', 'PIC', 'TAT', 'TAT2', 'U-PRO', 'IGG', 'IGA', 'IGM', 'CRP', 'RA', 'RF', 'C3', 'C4', 'RNP', 'SM', 'SC170', 'SSA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='ID')
# Determine outpatient follow-up: treat '-' or case-insensitive 'outpatient' indications as outpatient; if ambiguous, keep row to avoid empty results
adm = integrated['Admission'].astype(str).str.strip().str.lower()
is_outpatient = adm.eq('-') | adm.str.contains('outpatient', na=False)
# Define RBC abnormality using sex-specific adult reference ranges (plausible lab units x10^6/µL):
# Female normal ~ 3.8-5.2, Male normal ~ 4.2-5.8. If sex missing/other, use 3.8-5.8.
sex = integrated['SEX'].astype(str).str.strip().str.upper()
rbc = integrated['RBC']
low_f, high_f = 3.8, 5.2
low_m, high_m = 4.2, 5.8
low_u, high_u = 3.8, 5.8
is_f = sex.eq('F')
is_m = sex.eq('M')
low_bound = (is_f * low_f) + (is_m * low_m) + (~is_f & ~is_m) * low_u
high_bound = (is_f * high_f) + (is_m * high_m) + (~is_f & ~is_m) * high_u
abnormal_rbc = (rbc < low_bound) | (rbc > high_bound)
filtered = integrated[is_outpatient & abnormal_rbc]
# Return unique patient IDs who meet criteria
result_ids = filtered[['ID']].drop_duplicates().sort_values('ID')
target = result_ids

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
