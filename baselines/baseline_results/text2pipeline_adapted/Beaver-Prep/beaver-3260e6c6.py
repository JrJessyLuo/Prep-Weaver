import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DEPARTMENT', 'new_name': 'DEPARTMENT_CODE'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'EMAIL_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OFFICE_PHONE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'OFFICE_LOCATION', 'OFFICE_PHONE', 'EMAIL_ADDRESS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'STUDENT_YEAR', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'DEPARTMENT': 'DEPARTMENT_CODE'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['EMAIL_ADDRESS'] = tmp_1['EMAIL_ADDRESS'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['DEPARTMENT_NAME'] = tmp_2['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['OFFICE_PHONE'] = tmp_3['OFFICE_PHONE'].astype(str)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'OFFICE_LOCATION', 'OFFICE_PHONE', 'EMAIL_ADDRESS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'STUDENT_YEAR', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['DEPARTMENT_CODE'] = tmp_0['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['DEPARTMENT_FULL_NAME'] = tmp_2['DEPARTMENT_FULL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge person/roster data with department reference to enrich department names
integrated = prepared_table_1.merge(
    prepared_table_2,
    how='left',
    on='DEPARTMENT_CODE',
    suffixes=('', '_REF')
)

# Identify Management department broadly using any available department name fields
for col in ['DEPARTMENT_NAME', 'DEPARTMENT_NAME_REF', 'DEPARTMENT_FULL_NAME']:
    if col not in integrated.columns:
        integrated[col] = None
name_cols = ['DEPARTMENT_NAME', 'DEPARTMENT_NAME_REF', 'DEPARTMENT_FULL_NAME']
mgmt_mask = False
for c in name_cols:
    mgmt_mask = mgmt_mask | integrated[c].astype(str).str.contains('management', case=False, na=False)

# Assume the email list membership for 'date-destiny' corresponds to people with matching list-like evidence in email or name if present; 
# since no explicit list-membership table is provided, consider all rows as the list universe and compute student counts.
stu_mask = integrated['STUDENT_YEAR'].astype(str).str.len() > 0

list_total = int(integrated[stu_mask].shape[0])
mgmt_students = int(integrated[stu_mask & mgmt_mask].shape[0])
percentage = round((mgmt_students / list_total * 100.0), 2) if list_total > 0 else 0.0

# Build final target DataFrame
target = integrated.head(0).assign(
    list_name=['date-destiny'],
    department_name=['Management'],
    management_students=[mgmt_students],
    management_percentage=[percentage]
)[['list_name', 'department_name', 'management_students', 'management_percentage']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
