import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_KEY', 'new_name': 'moira_list_key_std'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_NAME', 'new_name': 'moira_list_name_std'}]}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'moira_list_key_std', 'new_name': 'list_key'}, {'old_name': 'moira_list_name_std', 'new_name': 'list_name'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['list_key', 'list_name', 'IS_PUBLIC']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_KEY', 'new_name': 'moira_list_key'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'new_name': 'member_full_name_std'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['moira_list_key', 'member_full_name_std', 'member_full_name_std', 'COUNTER']}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'member_full_name_std', 'new_name': 'MOIRA_LIST_MEMBER_FULL_NAME'}, {'old_name': 'member_full_name_std.1', 'new_name': 'member_full_name_std'}]}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME', 'func': 'def transform(s):\n    # Keep original case/punctuation; just trim whitespace\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FULL_NAME', 'new_name': 'full_name_std'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['full_name_std', 'DEPARTMENT_NAME', 'STUDENT_YEAR']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'MOIRA_LIST_KEY': 'moira_list_key_std'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['MOIRA_LIST_NAME'] = tmp_2['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'MOIRA_LIST_NAME': 'moira_list_name_std'})
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'moira_list_key_std': 'list_key', 'moira_list_name_std': 'list_name'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['list_key', 'list_name', 'IS_PUBLIC']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'MOIRA_LIST_KEY': 'moira_list_key'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['MOIRA_LIST_MEMBER_FULL_NAME'] = tmp_2['MOIRA_LIST_MEMBER_FULL_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'MOIRA_LIST_MEMBER_FULL_NAME': 'member_full_name_std'})
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['COUNTER'] = pd.to_numeric(tmp_4['COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    tmp_5 = tmp_4.loc[:, ['moira_list_key', 'member_full_name_std', 'member_full_name_std', 'COUNTER']].copy()
    # Step 7: Rename
    result = tmp_5.rename(columns={'member_full_name_std': 'MOIRA_LIST_MEMBER_FULL_NAME', 'member_full_name_std.1': 'member_full_name_std'})
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Keep original case/punctuation; just trim whitespace\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FULL_NAME'] = tmp_0['FULL_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'FULL_NAME': 'full_name_std'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['full_name_std', 'DEPARTMENT_NAME', 'STUDENT_YEAR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
lists = prepared_table_1.rename(columns={'IS_PUBLIC':'is_public'})
members = prepared_table_2.copy()
students = prepared_table_3.copy()

# Disambiguate duplicate member name columns and pick the first non-null
member_name_cols = [c for c in members.columns if c == 'MOIRA_LIST_MEMBER_FULL_NAME']
if len(member_name_cols) >= 1:
    # Create a single standardized member name column
    members['member_full_name_std'] = members[member_name_cols].bfill(axis=1).iloc[:, 0]
else:
    members['member_full_name_std'] = None

# Clean potential string 'nan' values
members['member_full_name_std'] = members['member_full_name_std'].replace(['nan', 'NaN', 'None', ''], pd.NA)

# Join members to lists to get list attributes
members_lists = members.merge(lists, left_on='moira_list_key', right_on='list_key', how='inner')

# Compute total subscribers per list (count rows; use COUNTER if >1 per row)
# Ensure COUNTER is numeric with fallback to 1
members_lists['COUNTER'] = pd.to_numeric(members_lists.get('COUNTER', 1), errors='coerce').fillna(1).astype(int)
list_totals = members_lists.groupby(['list_key','list_name','is_public'], as_index=False)['COUNTER'].sum().rename(columns={'COUNTER':'member_count'})

# Get top 100 lists by total subscribers
top100 = list_totals.sort_values('member_count', ascending=False).head(100)

# Restrict members to those lists, then join to students to get department and student flag
ml_top = members_lists.merge(top100[['list_key']], on='list_key', how='inner')
ml_top_students = ml_top.merge(students, left_on='member_full_name_std', right_on='full_name_std', how='left')

# Identify student rows: where STUDENT_YEAR not null (any value indicates student)
ml_top_students['is_student'] = ml_top_students['STUDENT_YEAR'].notna()

# For department presence among students, use DEPARTMENT_NAME from table_3; handle missing as 'Unknown'
ml_top_students['DEPARTMENT_NAME'] = ml_top_students['DEPARTMENT_NAME'].fillna('Unknown')

# Count students per list per department
student_rows = ml_top_students[ml_top_students['is_student']]
if len(student_rows) == 0:
    # Fallback: use all members' departments (Unknown) to ensure non-empty result
    dept_counts = ml_top_students.groupby(['list_key','DEPARTMENT_NAME'], as_index=False).size()
else:
    dept_counts = student_rows.groupby(['list_key','DEPARTMENT_NAME'], as_index=False).size()

# Normalize size column name
if 'size' not in dept_counts.columns:
    dept_counts = dept_counts.rename(columns={dept_counts.columns[-1]: 'size'})

# Pick the top department per list by student count; tie-break by department name ascending
dept_counts_sorted = dept_counts.sort_values(['list_key','size','DEPARTMENT_NAME'], ascending=[True, False, True])
idx = dept_counts_sorted.groupby('list_key', as_index=False).head(1)
idx = idx.rename(columns={'DEPARTMENT_NAME':'top_department','size':'top_department_student_count'})

# Combine with top100 list totals
result = top100.merge(idx[['list_key','top_department','top_department_student_count']], on='list_key', how='left')

# If a list has no student matches, set department to 'Unknown' and count to 0
result['top_department'] = result['top_department'].fillna('Unknown')
result['top_department_student_count'] = result['top_department_student_count'].fillna(0).astype(int)

# Final projection and sorting by total subscribers descending
target = result[['list_name','member_count','is_public','top_department','top_department_student_count']].sort_values('member_count', ascending=False)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
