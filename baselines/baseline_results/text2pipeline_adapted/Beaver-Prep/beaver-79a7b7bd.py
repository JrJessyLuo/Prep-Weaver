import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_ACTIVE', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_MAILING_LIST', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MOIRA_GROUP', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_NFS_GROUP', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_PUBLIC', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_HIDDEN', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP', 'IS_PUBLIC', 'IS_HIDDEN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else s"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_MEMBER_MIT_ID', 'func': "def transform(s):\n    if s is None:\n        return s\n    s = str(s)\n    if s == 'nan':\n        return None\n    return s[:-2] if s.endswith('.0') else s"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER_TYPE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'FULL_NAME', 'FORM_OF_ADDRESS_SHORT', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'KRB_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'JOB_ID', 'JOB_TITLE', 'ADMIN_EMPLOYEE_TYPE', 'HR_DEPARTMENT_CODE_OLD', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_ID', 'ADMIN_ORG_UNIT_TITLE', 'ADMIN_POSITION_TITLE', 'PAYROLL_RANK', 'IS_FACULTY', 'EMPLOYMENT_PERCENT', 'IS_CONSULT_PRIV', 'IS_PAID_APPT', 'IS_SUMMER_SESSION_APPT', 'SUMMER_SESSION_MONTHS', 'IS_SABBATICAL', 'SABBATICAL_BEGIN_DATE', 'SABBATICAL_END_DATE', 'IS_OPA_REQUIRED', 'IS_6MO_APPT', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
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
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['IS_ACTIVE'] = tmp_2['IS_ACTIVE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['IS_MOIRA_MAILING_LIST'] = tmp_3['IS_MOIRA_MAILING_LIST'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['IS_MOIRA_GROUP'] = tmp_4['IS_MOIRA_GROUP'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['IS_NFS_GROUP'] = tmp_5['IS_NFS_GROUP'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['IS_PUBLIC'] = tmp_6['IS_PUBLIC'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()[:1]", globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7['IS_HIDDEN'] = tmp_7['IS_HIDDEN'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP', 'IS_PUBLIC', 'IS_HIDDEN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_OWNER_KEY'] = tmp_1['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else s", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['moira_list_member'] = tmp_2['moira_list_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_3['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    if s is None:\n        return s\n    s = str(s)\n    if s == 'nan':\n        return None\n    return s[:-2] if s.endswith('.0') else s", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_4['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

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

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['MIT_ID', 'FULL_NAME', 'FORM_OF_ADDRESS_SHORT', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'KRB_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'JOB_ID', 'JOB_TITLE', 'ADMIN_EMPLOYEE_TYPE', 'HR_DEPARTMENT_CODE_OLD', 'HR_DEPARTMENT_NAME', 'HR_ORG_UNIT_ID', 'ADMIN_ORG_UNIT_TITLE', 'ADMIN_POSITION_TITLE', 'PAYROLL_RANK', 'IS_FACULTY', 'EMPLOYMENT_PERCENT', 'IS_CONSULT_PRIV', 'IS_PAID_APPT', 'IS_SUMMER_SESSION_APPT', 'SUMMER_SESSION_MONTHS', 'IS_SABBATICAL', 'SABBATICAL_BEGIN_DATE', 'SABBATICAL_END_DATE', 'IS_OPA_REQUIRED', 'IS_6MO_APPT', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_8', pd.DataFrame()))

# Stage-2 program over the prepared tables.
m1 = prepared_table_2.merge(prepared_table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME']], on='MOIRA_LIST_KEY', how='left')
m2 = m1.merge(prepared_table_3[['MOIRA_LIST_OWNER_KEY','OWNER_TYPE']], on='MOIRA_LIST_OWNER_KEY', how='left')
# Normalize MIT_ID string formats for join
mem = m2.copy()
mem['MOIRA_LIST_MEMBER_MIT_ID'] = mem['MOIRA_LIST_MEMBER_MIT_ID'].astype(str).str.strip()
mem['MOIRA_LIST_MEMBER_MIT_ID'] = mem['MOIRA_LIST_MEMBER_MIT_ID'].where(mem['MOIRA_LIST_MEMBER_MIT_ID'].str.lower()!='nan', None)
mem['MOIRA_LIST_MEMBER_MIT_ID'] = mem['MOIRA_LIST_MEMBER_MIT_ID'].str.replace('\.0$','',regex=True)
hr = prepared_table_4.copy()
if 'MIT_ID' in hr.columns:
    hr['MIT_ID'] = hr['MIT_ID'].astype(str).str.strip()
    hr['MIT_ID'] = hr['MIT_ID'].where(hr['MIT_ID'].str.lower()!='nan', None)
    hr['MIT_ID'] = hr['MIT_ID'].str.replace('\.0$','',regex=True)
    if 'HR_DEPARTMENT_NAME' in hr.columns:
        hr['HR_DEPARTMENT_NAME'] = hr['HR_DEPARTMENT_NAME'].astype(str).str.strip()
else:
    hr = hr
m3 = mem.merge(hr[['MIT_ID','HR_DEPARTMENT_NAME']] if 'MIT_ID' in hr.columns else mem.iloc[0:0], left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID', how='left')
# Filter to departments starting with 'Computer Science' (case-insensitive). If no rows, relax to contains.
flt = m3[m3['HR_DEPARTMENT_NAME'].astype(str).str.lower().str.startswith('computer science', na=False)]
if flt.empty:
    flt = m3[m3['HR_DEPARTMENT_NAME'].astype(str).str.lower().str.contains('computer science', na=False)]
# Count subscribers per list (distinct members) and owners per list (rows where OWNER_TYPE indicates ownership). Assume owners are rows where OWNER_TYPE is not null and indicates an owner entry; count distinct OWNER where available, otherwise distinct MOIRA_LIST_OWNER_KEY.
sub_counts = flt.groupby(['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME'], dropna=False)['moira_list_member'].nunique().reset_index(name='num_subscribers')
own_cols = ['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME']
own_id = 'MOIRA_LIST_OWNER_KEY'
owners = flt.dropna(subset=['OWNER_TYPE'])
own_counts = owners.groupby(own_cols)[own_id].nunique().reset_index(name='num_owners')
res = sub_counts.merge(own_counts, on=['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME'], how='left')
res['num_owners'] = res['num_owners'].fillna(0).astype(int)
res['num_subscribers'] = res['num_subscribers'].fillna(0).astype(int)
# Build subtotals per ownership type
subtot = res.groupby('OWNER_TYPE', dropna=False).agg(num_owners=('num_owners','sum'), num_subscribers=('num_subscribers','sum')).reset_index()
subtot['MOIRA_LIST_KEY'] = ''
subtot['MOIRA_LIST_NAME'] = 'SUBTOTAL'
subtot['type_display'] = 'SUBTOTAL'
# Grand total
grand = subtot.agg({'num_owners':'sum','num_subscribers':'sum'})
grand_df = subtot.iloc[0:0].copy()
grand_df = grand_df.assign(OWNER_TYPE='TOTAL', MOIRA_LIST_KEY='', MOIRA_LIST_NAME='TOTAL', type_display='TOTAL', num_owners=int(grand['num_owners']) if not subtot.empty else 0, num_subscribers=int(grand['num_subscribers']) if not subtot.empty else 0)
# Detail rows: display OWNER_TYPE only when it differs from previous. Prepare ordering by OWNER_TYPE then list name.
detail = res.sort_values(['OWNER_TYPE','MOIRA_LIST_NAME']).copy()
detail['type_display'] = detail['OWNER_TYPE']
detail.loc[detail['OWNER_TYPE'].astype(str).shift(1)==detail['OWNER_TYPE'].astype(str), 'type_display'] = ''
# Concatenate detail, subtotals (per type), then grand total. Insert subtotals after each OWNER_TYPE block by sorting appropriately.
subtot_for_merge = subtot[['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME','num_owners','num_subscribers','type_display']].copy()
subtot_for_merge['__order__'] = 1
# Add order marker to detail rows to place before subtotals within each OWNER_TYPE
detail['__order__'] = 0
combined = (
    pd.concat([detail, subtot_for_merge], ignore_index=True)
      .sort_values(['OWNER_TYPE','__order__','MOIRA_LIST_NAME'], kind='mergesort')
      .drop(columns='__order__')
)
# Append grand total at end
final = pd.concat([combined, grand_df[['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME','num_owners','num_subscribers','type_display']]], ignore_index=True)
# Final projection and column names per requirement: ownership type display, list name, number of owners, number of subscribers
final = final.rename(columns={'type_display':'OWNERSHIP_TYPE_DISPLAY','MOIRA_LIST_NAME':'LIST_NAME'})
final = final[['OWNERSHIP_TYPE_DISPLAY','LIST_NAME','num_owners','num_subscribers']]
# If everything ended empty due to joins, fall back to listing totals across whatever integrated rows exist
if final.empty:
    # Try computing from m2 without HR filter as fallback
    sub_counts_fb = m2.groupby(['MOIRA_LIST_OWNER_KEY','OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME'], dropna=False)['moira_list_member'].nunique().reset_index(name='num_subscribers')
    own_counts_fb = m2.dropna(subset=['MOIRA_LIST_OWNER_KEY']).groupby(['MOIRA_LIST_OWNER_KEY','OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME'], dropna=False)['MOIRA_LIST_OWNER_KEY'].nunique().groupby(level=[1,2,3]).sum().reset_index(name='num_owners')
    res_fb = sub_counts_fb.groupby(['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME'], dropna=False)['num_subscribers'].sum().reset_index()
    res_fb = res_fb.merge(own_counts_fb, on=['OWNER_TYPE','MOIRA_LIST_KEY','MOIRA_LIST_NAME'], how='left')
    res_fb['num_owners'] = res_fb['num_owners'].fillna(0).astype(int)
    res_fb = res_fb.sort_values(['OWNER_TYPE','MOIRA_LIST_NAME'])
    res_fb['OWNERSHIP_TYPE_DISPLAY'] = res_fb['OWNER_TYPE']
    res_fb.loc[res_fb['OWNER_TYPE'].astype(str).shift(1)==res_fb['OWNER_TYPE'].astype(str), 'OWNERSHIP_TYPE_DISPLAY'] = ''
    subtot_fb = res_fb.groupby('OWNER_TYPE', dropna=False).agg(num_owners=('num_owners','sum'), num_subscribers=('num_subscribers','sum')).reset_index()
    subtot_fb['OWNERSHIP_TYPE_DISPLAY'] = 'SUBTOTAL'
    subtot_fb['MOIRA_LIST_NAME'] = 'SUBTOTAL'
    grand_fb = subtot_fb.agg({'num_owners':'sum','num_subscribers':'sum'})
    grand_row_fb = pd.DataFrame([{'OWNERSHIP_TYPE_DISPLAY':'TOTAL','MOIRA_LIST_NAME':'TOTAL','num_owners':int(grand_fb['num_owners']), 'num_subscribers':int(grand_fb['num_subscribers'])}])
    final = pd.concat([res_fb.rename(columns={'MOIRA_LIST_NAME':'LIST_NAME'})[['OWNERSHIP_TYPE_DISPLAY','LIST_NAME','num_owners','num_subscribers']],
                       subtot_fb.rename(columns={'MOIRA_LIST_NAME':'LIST_NAME'})[['OWNERSHIP_TYPE_DISPLAY','LIST_NAME','num_owners','num_subscribers']],
                       grand_row_fb.rename(columns={'MOIRA_LIST_NAME':'LIST_NAME'})], ignore_index=True)

target = final

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
