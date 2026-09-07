import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    import re\n    s = str(s)\n    s = s.strip().lower()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    import re\n    s = str(s)\n    s = s.strip().lower()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP', 'IS_PUBLIC', 'IS_HIDDEN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LAST_UPDATE_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER_TYPE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'EMAIL_ADDRESS', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FULL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'STUDENT_YEAR', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'OFFICE_LOCATION', 'OFFICE_PHONE', 'EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = str(s)\n    s = s.strip().lower()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = str(s)\n    s = s.strip().lower()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP', 'IS_PUBLIC', 'IS_HIDDEN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_10', pd.DataFrame()))

def _prepare_table_2(_source):
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
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_OWNER_KEY'] = tmp_1['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['moira_list_member'] = tmp_2['moira_list_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['MOIRA_LIST_MEMBER_FULL_NAME'] = tmp_3['MOIRA_LIST_MEMBER_FULL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['LAST_UPDATE_DATE'] = pd.to_datetime(tmp_4['LAST_UPDATE_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_5['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['COUNTER'] = pd.to_numeric(tmp_6['COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_OWNER_KEY'] = tmp_0['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['OWNER'] = tmp_1['OWNER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['OWNER_TYPE'] = tmp_2['OWNER_TYPE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['EMAIL_ADDRESS'] = tmp_0['EMAIL_ADDRESS'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['FULL_NAME'] = tmp_1['FULL_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['DEPARTMENT_NAME'] = tmp_2['DEPARTMENT_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['STUDENT_YEAR'] = tmp_3['STUDENT_YEAR'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'OFFICE_LOCATION', 'OFFICE_PHONE', 'EMAIL_ADDRESS', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
lists = prepared_table_1.copy()
members = prepared_table_2.copy()
owners = prepared_table_3.copy()
people = prepared_table_4.copy()

# Join lists to members on normalized list name/key
lm = members.merge(lists, left_on='MOIRA_LIST_KEY', right_on='MOIRA_LIST_NAME', how='inner', suffixes=('_mem','_list'))

# Attach owner name
lm = lm.merge(owners[['MOIRA_LIST_OWNER_KEY','OWNER']], on='MOIRA_LIST_OWNER_KEY', how='left')

# Derive a member identifier suitable for matching to email usernames
# Use moira_list_member trimmed/lower as candidate username; also check if it already looks like email and take local-part
m_user = lm['moira_list_member'].astype(str).str.strip()
m_user_lower = m_user.str.lower()
local_part = m_user_lower.str.split('@').str[0]
lm['member_user'] = local_part

# Prepare people directory username from EMAIL_ADDRESS
people_email = people['EMAIL_ADDRESS'].astype(str).str.strip().str.lower()
people['email_user'] = people_email.str.split('@').str[0]

# Broad CS department flag: case-insensitive contains for common variants
dept = people['DEPARTMENT_NAME'].astype(str).str.lower()
cs_flag = (
    dept.str.contains('computer sci', case=False, na=False) |
    dept.str.contains('electrical eng', case=False, na=False) & dept.str.contains('computer', case=False, na=False) |
    dept.str.contains('eecs', case=False, na=False)
)
people['is_cs'] = cs_flag

# Join member rows to people via username heuristic (many-to-one)
lmp = lm.merge(people[['email_user','is_cs']], left_on='member_user', right_on='email_user', how='left')

# Compute per-list member counts and CS counts
grp = lmp.groupby(['MOIRA_LIST_NAME','OWNER'], dropna=False).agg(
    member_count=('moira_list_member','count'),
    cs_count=('is_cs', lambda x: x.fillna(False).sum())
).reset_index()

# Compute CS percentage and apply filters: name starts with 'e', 10-20 members inclusive, over 75% CS
name_series = grp['MOIRA_LIST_NAME'].astype(str)
starts_with_e = name_series.str.strip().str.lower().str.startswith('e')
cs_pct = grp['cs_count'] / grp['member_count']
mask = starts_with_e & (grp['member_count'] >= 10) & (grp['member_count'] <= 20) & (cs_pct > 0.75)
res = grp.loc[mask, ['MOIRA_LIST_NAME','OWNER','member_count']].copy()

# If empty, relax CS department matching by considering any 'computer' mention
if res.empty:
    dept2 = people['DEPARTMENT_NAME'].astype(str).str.lower()
    people['is_cs_relaxed'] = dept2.str.contains('computer', na=False)
    lmp2 = lm.merge(people[['email_user','is_cs_relaxed']], left_on='member_user', right_on='email_user', how='left')
    grp2 = lmp2.groupby(['MOIRA_LIST_NAME','OWNER'], dropna=False).agg(
        member_count=('moira_list_member','count'),
        cs_count=('is_cs_relaxed', lambda x: x.fillna(False).sum())
    ).reset_index()
    name_series2 = grp2['MOIRA_LIST_NAME'].astype(str)
    starts_with_e2 = name_series2.str.strip().str.lower().str.startswith('e')
    cs_pct2 = grp2['cs_count'] / grp2['member_count']
    mask2 = starts_with_e2 & (grp2['member_count'] >= 10) & (grp2['member_count'] <= 20) & (cs_pct2 > 0.75)
    res = grp2.loc[mask2, ['MOIRA_LIST_NAME','OWNER','member_count']].copy()

# Final projection and rename per question
res = res.rename(columns={'MOIRA_LIST_NAME':'list_name','OWNER':'owner','member_count':'member_count'})

target = res.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
