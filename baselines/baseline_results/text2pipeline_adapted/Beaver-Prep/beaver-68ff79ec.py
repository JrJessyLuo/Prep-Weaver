import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'FIRST_NAME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MIDDLE_NAME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LAST_NAME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'EMAIL_ADDRESS', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OFFICE_PHONE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DEPARTMENT', 'new_name': 'DEPARTMENT_CODE'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL_ADDRESS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    # trim and collapse internal whitespace, preserve original casing otherwise\n    return " ".join(s.strip().split())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'department_full_name', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FIRST_NAME'] = tmp_0['FIRST_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MIDDLE_NAME'] = tmp_1['MIDDLE_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['LAST_NAME'] = tmp_2['LAST_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['FULL_NAME'] = tmp_3['FULL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['EMAIL_ADDRESS'] = tmp_4['EMAIL_ADDRESS'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['DEPARTMENT'] = tmp_5['DEPARTMENT'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['DEPARTMENT_NAME'] = tmp_6['DEPARTMENT_NAME'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['OFFICE_PHONE'] = tmp_7['OFFICE_PHONE'].astype(str)
    # Step 9: Rename
    tmp_8 = tmp_7.rename(columns={'DEPARTMENT': 'DEPARTMENT_CODE'})
    # Step 10: SelectCol
    result = tmp_8.loc[:, ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL_ADDRESS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    # trim and collapse internal whitespace, preserve original casing otherwise\n    return " ".join(s.strip().split())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['DEPARTMENT_CODE'] = tmp_0['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['department_full_name'] = tmp_2['department_full_name'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['SCHOOL_CODE'] = tmp_3['SCHOOL_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return " ".join(s.strip().split())', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['SCHOOL_NAME'] = tmp_4['SCHOOL_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge student records with department-school mapping on DEPARTMENT_CODE (and DEPARTMENT_NAME to preserve exact dept identity)
integrated = prepared_table_1.merge(prepared_table_2, how='left', on=['DEPARTMENT_CODE', 'DEPARTMENT_NAME'])

# Filter for first name 'Kevin' with robust case-insensitive match on FIRST_NAME; fallback to contains if exact yields none
kevin_rows = integrated[integrated['FIRST_NAME'].astype(str).str.strip().str.casefold() == 'kevin']
if kevin_rows.empty:
    kevin_rows = integrated[integrated['FIRST_NAME'].astype(str).str.contains('kevin', case=False, na=False)]

# Compute total student count per department and school across the full integrated data
counts = (
    integrated.groupby(['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], dropna=False)
    .size()
    .reset_index(name='TOTAL_STUDENTS_IN_DEPT_SCHOOL')
)

# Join counts back to Kevin rows to get totals per department-school
kevin_with_counts = kevin_rows.merge(
    counts,
    how='left',
    on=['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME']
)

# Prepare final projection
target = kevin_with_counts[[
    'FULL_NAME',
    'EMAIL_ADDRESS',
    'DEPARTMENT_NAME',
    'DEPARTMENT_CODE',
    'SCHOOL_NAME',
    'TOTAL_STUDENTS_IN_DEPT_SCHOOL'
]].copy()

# If FULL_NAME is missing or blank, construct from parts as fallback
mask_missing_full = target['FULL_NAME'].isna() | (target['FULL_NAME'].astype(str).str.strip() == '')
if mask_missing_full.any():
    fn = kevin_with_counts['FIRST_NAME'].fillna('').astype(str).str.strip()
    mn = kevin_with_counts['MIDDLE_NAME'].fillna('').astype(str).str.strip()
    ln = kevin_with_counts['LAST_NAME'].fillna('').astype(str).str.strip()
    constructed = (
        ln.where(ln == '', ln + ', ') + fn +
        mn.where(mn == '', ' ' + mn + '.')
    ).str.strip(', ').str.replace('  ', ' ', regex=False)
    target.loc[mask_missing_full, 'FULL_NAME'] = constructed[mask_missing_full]

# Deduplicate identical associations
target = target.drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
