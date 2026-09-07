import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip().upper()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LAST_UPDATE_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'EMAIL_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip().lower() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'EMAIL_ADDRESS', 'target_columns': ['USERNAME', '_discard_domain'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('@', 1)\n    local = parts[0].lower() if parts else ''\n    domain = parts[1] if len(parts) > 1 else ''\n    return [local, domain]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FIRST_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MIDDLE_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LAST_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME_UPPERCASE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OFFICE_PHONE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_discard_domain']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['USERNAME', 'DEPARTMENT', 'DEPARTMENT_NAME', 'OFFICE_PHONE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SIS_ADMIN_DEPARTMENT_CODE', 'func': 'def transform(s):\n    # Trim whitespace; keep original case\n    return "" if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SIS_ADMIN_DEPARTMENT_NAME', 'func': 'def transform(s):\n    # Trim whitespace; keep original case\n    return "" if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_PHONE_AREA_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'department_phone_number', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number'], 'target_column': 'DEPT_PHONE', 'func': 'def transform(row):\n    import math\n    def clean(v):\n        if v is None:\n            return ""\n        s = str(v).strip()\n        # normalize pandas float-to-str artifacts like \'nan\' and trailing .0\n        if s.lower() == \'nan\':\n            return ""\n        if s.endswith(\'.0\') and s.replace(\'.\', \'\', 1).isdigit():\n            s = s[:-2]\n        return s\n    area = clean(row.get(\'DEPARTMENT_PHONE_AREA_CODE\'))\n    num = clean(row.get(\'department_phone_number\'))\n    if area and num:\n        return f"{area}-{num}"\n    return area or num or ""'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SIS_ADMIN_DEPARTMENT_CODE', 'SIS_ADMIN_DEPARTMENT_NAME', 'DEPT_PHONE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip().upper()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['moira_list_member'] = tmp_1['moira_list_member'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['MOIRA_LIST_MEMBER_FULL_NAME'] = tmp_2['MOIRA_LIST_MEMBER_FULL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_3['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['LAST_UPDATE_DATE'] = pd.to_datetime(tmp_4['LAST_UPDATE_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['COUNTER'] = pd.to_numeric(tmp_5['COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['EMAIL_ADDRESS'] = tmp_0['EMAIL_ADDRESS'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('@', 1)\n    local = parts[0].lower() if parts else ''\n    domain = parts[1] if len(parts) > 1 else ''\n    return [local, domain]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['EMAIL_ADDRESS'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['USERNAME'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['_discard_domain'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['FIRST_NAME'] = tmp_2['FIRST_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['MIDDLE_NAME'] = tmp_3['MIDDLE_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['LAST_NAME'] = tmp_4['LAST_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['FULL_NAME'] = tmp_5['FULL_NAME'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['FULL_NAME_UPPERCASE'] = tmp_6['FULL_NAME_UPPERCASE'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7['DEPARTMENT'] = tmp_7['DEPARTMENT'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_9 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_9)
    _std_func_9 = _ns_9.get('transform') or _ns_9.get('transform')
    tmp_8['DEPARTMENT_NAME'] = tmp_8['DEPARTMENT_NAME'].apply(lambda s: _std_func_9(s) if pd.notna(s) else s)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['OFFICE_PHONE'] = tmp_9['OFFICE_PHONE'].astype(str)
    # Step 11: DropColumn
    tmp_10 = tmp_9.drop(columns=['_discard_domain'], errors='ignore').copy()
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['USERNAME', 'DEPARTMENT', 'DEPARTMENT_NAME', 'OFFICE_PHONE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace; keep original case\n    return "" if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SIS_ADMIN_DEPARTMENT_CODE'] = tmp_0['SIS_ADMIN_DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim whitespace; keep original case\n    return "" if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SIS_ADMIN_DEPARTMENT_NAME'] = tmp_1['SIS_ADMIN_DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['DEPARTMENT_PHONE_AREA_CODE'] = tmp_2['DEPARTMENT_PHONE_AREA_CODE'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['department_phone_number'] = tmp_3['department_phone_number'].astype(str)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(row):\n    import math\n    def clean(v):\n        if v is None:\n            return ""\n        s = str(v).strip()\n        # normalize pandas float-to-str artifacts like \'nan\' and trailing .0\n        if s.lower() == \'nan\':\n            return ""\n        if s.endswith(\'.0\') and s.replace(\'.\', \'\', 1).isdigit():\n            s = s[:-2]\n        return s\n    area = clean(row.get(\'DEPARTMENT_PHONE_AREA_CODE\'))\n    num = clean(row.get(\'department_phone_number\'))\n    if area and num:\n        return f"{area}-{num}"\n    return area or num or ""', globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_4['DEPT_PHONE'] = tmp_4[['DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number']].apply(_concat_func_3, axis=1)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['SIS_ADMIN_DEPARTMENT_CODE', 'SIS_ADMIN_DEPARTMENT_NAME', 'DEPT_PHONE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
members = prepared_table_1.copy()
members['MOIRA_LIST_KEY'] = members['MOIRA_LIST_KEY'].astype(str)
# Filter to the 'ocean-apple' mailing list
mlist = members[members['MOIRA_LIST_KEY'].str.strip().str.lower() == 'ocean-apple']
# Prepare username from moira_list_member (case-insensitive join)
mlist = mlist.assign(USERNAME=mlist['moira_list_member'].astype(str).str.strip().str.lower())
# Join to people directory on USERNAME
people = prepared_table_2.copy()
joined = mlist.merge(people, how='left', on='USERNAME')
# Enrich with department phone by joining department name to SIS admin department name (case-insensitive)
depdir = prepared_table_3.copy()
depdir['__dep_name_key'] = depdir['SIS_ADMIN_DEPARTMENT_NAME'].astype(str).str.strip().str.lower()
joined['__dep_name_key'] = joined['DEPARTMENT_NAME'].astype(str).str.strip().str.lower()
joined = joined.merge(depdir[['__dep_name_key','DEPT_PHONE']], how='left', on='__dep_name_key')
# Choose phone preference: use department directory phone when available, else use OFFICE_PHONE
joined['PHONE'] = joined['DEPT_PHONE'].where(joined['DEPT_PHONE'].notna() & (joined['DEPT_PHONE'].astype(str).str.len()>0), joined['OFFICE_PHONE'])
# Aggregate student counts per department name (case-insensitive grouping but preserve display name)
joined['DEPT_DISPLAY'] = joined['DEPARTMENT_NAME']
counts = joined.groupby(joined['DEPARTMENT_NAME'].astype(str).str.strip().str.lower(), dropna=False).agg(
    STUDENT_COUNT=('USERNAME','nunique'),
    DEPT_DISPLAY=('DEPT_DISPLAY','first'),
    PHONE=('PHONE','first')
).reset_index(drop=True)
# Find max count and filter
if len(counts) == 0:
    target = counts
else:
    max_count = counts['STUDENT_COUNT'].max()
    top = counts[counts['STUDENT_COUNT'] == max_count].copy()
    # Final projection
    top = top.rename(columns={'DEPT_DISPLAY':'DEPARTMENT_NAME'})
    target = top[['DEPARTMENT_NAME','PHONE','STUDENT_COUNT']].sort_values(['DEPARTMENT_NAME']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
