import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'cds', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'rtype', 'func': "def transform(s):\n    return ('' if s is None else str(s)).strip()"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['sname_prefix', 'sname_suffix'], 'target_column': 'SchoolName', 'func': "def transform(row):\n    parts = []\n    for col in ['sname_prefix','sname_suffix']:\n        v = row.get(col, None)\n        if v is None:\n            continue\n        s = str(v).strip()\n        if s and s.lower() != 'nan':\n            parts.append(s)\n    return ' '.join(parts)"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NumTstTakr', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NumGE1500', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['cds', 'rtype', 'dname', 'cname', 'enroll12', 'NumTstTakr', 'NumGE1500', 'SchoolName']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'CDSCode', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'School', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'District', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'County', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CDSCode', 'School', 'District', 'County', 'StatusType', 'Phone', 'Website', 'AdmFName1']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['cds'] = tmp_0['cds'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return ('' if s is None else str(s)).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['rtype'] = tmp_1['rtype'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(row):\n    parts = []\n    for col in ['sname_prefix','sname_suffix']:\n        v = row.get(col, None)\n        if v is None:\n            continue\n        s = str(v).strip()\n        if s and s.lower() != 'nan':\n            parts.append(s)\n    return ' '.join(parts)", globals(), _ns_2)
    _concat_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('concat')
    tmp_2['SchoolName'] = tmp_2[['sname_prefix', 'sname_suffix']].apply(_concat_func_2, axis=1)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['NumTstTakr'] = pd.to_numeric(tmp_3['NumTstTakr'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['NumGE1500'] = pd.to_numeric(tmp_4['NumGE1500'], errors='coerce').astype(float)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['cds', 'rtype', 'dname', 'cname', 'enroll12', 'NumTstTakr', 'NumGE1500', 'SchoolName']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CDSCode'] = tmp_0['CDSCode'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['School'] = tmp_1['School'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['District'] = tmp_2['District'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['County'] = tmp_3['County'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['CDSCode', 'School', 'District', 'County', 'StatusType', 'Phone', 'Website', 'AdmFName1']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', left_on='cds', right_on='CDSCode')
# Focus on school rows and valid counts, then find the school with the highest number of test takers with SAT >=1500
integrated_schools = integrated[integrated['rtype'].str.upper()=='S'].copy()
# Coerce NumGE1500 to numeric in case of any lingering non-numeric values after preparation
integrated_schools['NumGE1500'] = integrated_schools['NumGE1500'].astype(float)
# Identify the maximum NumGE1500
max_val = integrated_schools['NumGE1500'].max()
# Get all schools achieving that max (ties allowed)
top = integrated_schools[integrated_schools['NumGE1500']==max_val].copy()
# Prefer an explicit administrator email column if present; otherwise try common email-like columns
email_cols = [c for c in top.columns if 'email' in c.lower()]
if email_cols:
    email_col = email_cols[0]
    top['AdminEmail'] = top[email_col]
else:
    # Fallback: if no email column exists, leave AdminEmail as None to preserve rows without error
    top['AdminEmail'] = None
# Choose a display school name: prefer directory 'School' when available; fallback to constructed 'SchoolName'
top['SchoolDisplay'] = top['School'].where(top['School'].notna() & (top['School'].astype(str).str.strip()!=''), top['SchoolName'])
# Final projection
target = top[['SchoolDisplay', 'AdminEmail']].rename(columns={'SchoolDisplay':'School', 'AdminEmail':'AdministratorEmail'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
