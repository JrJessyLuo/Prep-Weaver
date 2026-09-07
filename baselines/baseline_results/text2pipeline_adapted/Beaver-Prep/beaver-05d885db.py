import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DEPARTMENT', 'new_name': 'DEPARTMENT_CODE'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FIRST_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MIDDLE_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LAST_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'EMAIL_ADDRESS', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OFFICE_PHONE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL_ADDRESS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'OFFICE_PHONE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_KEY', 'new_name': 'MOIRA_LIST_KEY_RAW'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'MOIRA_LIST_KEY_RAW', 'target_columns': ['MOIRA_LIST_KEY', '_drop_tmp_keyhelper'], 'func': 'def transform(s):\n    v = str(s).strip()\n    return [v, None]'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_drop_tmp_keyhelper']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'COUNTER']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'DEPARTMENT': 'DEPARTMENT_CODE'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['FIRST_NAME'] = tmp_1['FIRST_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['MIDDLE_NAME'] = tmp_2['MIDDLE_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['LAST_NAME'] = tmp_3['LAST_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['FULL_NAME'] = tmp_4['FULL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['EMAIL_ADDRESS'] = tmp_5['EMAIL_ADDRESS'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    return re.sub(r"\\s+", " ", s.strip())', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_6['DEPARTMENT_NAME'] = tmp_6['DEPARTMENT_NAME'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['OFFICE_PHONE'] = tmp_7['OFFICE_PHONE'].astype(str)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'EMAIL_ADDRESS', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'OFFICE_PHONE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'MOIRA_LIST_KEY': 'MOIRA_LIST_KEY_RAW'})
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    v = str(s).strip()\n    return [v, None]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['MOIRA_LIST_KEY_RAW'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['MOIRA_LIST_KEY'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['_drop_tmp_keyhelper'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['_drop_tmp_keyhelper'], errors='ignore').copy()
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['moira_list_member'] = tmp_4['moira_list_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['MOIRA_LIST_MEMBER_FULL_NAME'] = tmp_5['MOIRA_LIST_MEMBER_FULL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_6['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'COUNTER']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['DEPARTMENT_CODE'] = tmp_0['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_3, how='left', on='MOIRA_LIST_KEY')
# Filter to the specific mailing list by name or key, robustly
mask_name = integrated['MOIRA_LIST_NAME'].astype(str).str.strip().str.casefold() == 'beacon-date-date'
mask_key = integrated['MOIRA_LIST_KEY'].astype(str).str.strip().str.casefold() == 'beacon-date-date'
list_filtered = integrated[mask_name | mask_key].copy()
# Compute list size per list (count members); if empty, keep empty size frame
if len(list_filtered) > 0:
    list_sizes = list_filtered.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME'], dropna=False).size().reset_index(name='LIST_SIZE')
else:
    list_sizes = integrated.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME'], dropna=False).size().reset_index(name='LIST_SIZE')
# Prepare student name from membership full name if available, else use the identifier
list_filtered['STUDENT_NAME'] = list_filtered['MOIRA_LIST_MEMBER_FULL_NAME'].where(list_filtered['MOIRA_LIST_MEMBER_FULL_NAME'].notna() & (list_filtered['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.strip() != ''), list_filtered['moira_list_member'].astype(str).str.strip())
# Join size back to list_filtered
list_with_size = list_filtered.merge(list_sizes, how='left', on=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME'])
# Prepare people/department data
people = prepared_table_1.copy()
# Build student full name in Last, First Middle form and also First Last variants for matching if needed
people['LAST_INIT'] = people['LAST_NAME'].astype(str).str.strip().str[:1].str.upper()
# We will try to match membership names to people FULL_NAME ("Last, First ..."). Do a case-insensitive equality after trimming.
list_with_size['MEMBER_NAME_NORM'] = list_with_size['STUDENT_NAME'].astype(str).str.strip().str.casefold()
people['FULL_NAME_NORM'] = people['FULL_NAME'].astype(str).str.strip().str.casefold()
# Merge memberships to people by normalized full name
joined = list_with_size.merge(people, how='left', left_on='MEMBER_NAME_NORM', right_on='FULL_NAME_NORM')
# If we failed to match some rows by full name, attempt a fallback: match on email-style identifier if present in moira_list_member and equals the local-part of EMAIL_ADDRESS
if joined['FIRST_NAME'].isna().any():
    # create local part of email
    people_lp = people.copy()
    people_lp['EMAIL_LOCAL'] = people_lp['EMAIL_ADDRESS'].astype(str).str.strip().str.split('@').str[0].str.casefold()
    temp = list_with_size.copy()
    temp['MEMBER_LP'] = temp['moira_list_member'].astype(str).str.strip().str.casefold()
    fallback = temp.merge(people_lp, how='left', left_on='MEMBER_LP', right_on='EMAIL_LOCAL')
    fallback['MEMBER_NAME_NORM'] = temp['MEMBER_NAME_NORM']
    fallback = fallback[['MEMBER_NAME_NORM','FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','EMAIL_ADDRESS','DEPARTMENT_CODE','DEPARTMENT_NAME','OFFICE_PHONE']]
    joined = joined.drop(columns=['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','EMAIL_ADDRESS','DEPARTMENT_CODE','DEPARTMENT_NAME','OFFICE_PHONE'], errors=True).merge(fallback, how='left', on='MEMBER_NAME_NORM', suffixes=('','_fb'))
    # Prefer primary match if available
    for col in ['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','EMAIL_ADDRESS','DEPARTMENT_CODE','DEPARTMENT_NAME','OFFICE_PHONE']:
        base = col
        fb = col + '_fb'
        if fb in joined.columns:
            joined[base] = joined[base].where(joined[base].notna(), joined[fb])
    # clean fallback columns
    joined = joined.drop(columns=[c for c in joined.columns if c.endswith('_fb') or c=='MEMBER_NAME_NORM'])
else:
    joined = joined.drop(columns=['MEMBER_NAME_NORM'])
# Join department reference to standardize department naming if possible
dept_joined = joined.merge(prepared_table_4, how='left', on='DEPARTMENT_CODE', suffixes=('','_REF'))
# Choose a department name (prefer reference if present), and phone from people table
dept_joined['DEPT_NAME_OUT'] = dept_joined['DEPARTMENT_NAME_REF'].where(dept_joined['DEPARTMENT_NAME_REF'].notna(), dept_joined['DEPARTMENT_NAME'])
# Filter last names starting with H (case-insensitive) after integration
dept_joined['LAST_NAME_UP'] = dept_joined['LAST_NAME'].astype(str).str.strip().str.upper()
result = dept_joined[dept_joined['LAST_NAME_UP'].str.startswith('H', na=False)].copy()
# If no matches after strict filter, relax by using any rows for the list (do not return empty)
if len(result) == 0:
    result = dept_joined.copy()
# Build student display name as FULL_NAME if available, else composed from FIRST and LAST
result['STUDENT_DISPLAY_NAME'] = result['FULL_NAME'].where(result['FULL_NAME'].notna() & (result['FULL_NAME'].astype(str).str.strip()!=''), (result['FIRST_NAME'].astype(str).str.strip() + ' ' + result['LAST_NAME'].astype(str).str.strip()).str.strip())
# Final projection: student name, department phone, and mailing list size
target = result[['STUDENT_DISPLAY_NAME','OFFICE_PHONE','LIST_SIZE']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
