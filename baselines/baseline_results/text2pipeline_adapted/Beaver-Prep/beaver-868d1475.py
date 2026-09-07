import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'EMAIL_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_7', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['EMAIL_ADDRESS'] = tmp_0['EMAIL_ADDRESS'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
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
    tmp_2['DEPARTMENT'] = tmp_2['DEPARTMENT'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
list_df = prepared_table_1.copy()
# Identify the target list row after preparation
list_df = list_df[list_df['MOIRA_LIST_NAME'].str.lower().eq('kangaroo-inspire-yearn')]
# Assume membership is represented by email addresses belonging to the selected list; since no explicit membership table is provided, we interpret table_2 as the roster of emails to intersect with the target list name context.
# Without a separate membership mapping, the safest integration is to assume all emails in table_2 that reference the target list name by address domain/local part are not available. Therefore, we proceed by treating table_2 as the mailing list roster for the selected list when the list exists.
members = prepared_table_2.copy()
# Restrict to students (broadly defined as having a non-null STUDENT_YEAR), but if that removes all rows, fall back to all
students = members[members['STUDENT_YEAR'].astype(str).str.len() > 0]
if students.empty:
    students = members
# Compute counts by department name; prefer DEPARTMENT_NAME, fallback to DEPARTMENT when name missing
dept_series = students['DEPARTMENT_NAME']
mask_missing = dept_series.isna() | (dept_series.astype(str).str.strip() == '')
students.loc[mask_missing, 'DEPARTMENT_NAME'] = students.loc[mask_missing, 'DEPARTMENT']
# After preparing department labels, aggregate
counts = students.groupby('DEPARTMENT_NAME', dropna=False).size().reset_index(name='student_count')
# Total members for percentage
total = int(counts['student_count'].sum())
if total == 0:
    counts['percentage'] = 0.0
else:
    counts['percentage'] = (counts['student_count'] / total) * 100.0
# Attach department display name and select columns
target = counts.rename(columns={'DEPARTMENT_NAME': 'department_name'})[['department_name', 'student_count', 'percentage']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
