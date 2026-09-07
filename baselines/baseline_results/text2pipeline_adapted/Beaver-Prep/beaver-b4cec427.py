import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_DESCRIPTION', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_PUBLIC', 'IS_HIDDEN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'MOIRA_LIST_MEMBER_MIT_ID', 'target_columns': ['MOIRA_LIST_MEMBER_MIT_ID'], 'func': 'def transform(s):\n    import math\n    v = None if s is None or (isinstance(s, float) and math.isnan(s)) or str(s).strip().lower()==\'nan\' else s\n    if v is None:\n        return [None]\n    try:\n        f = float(str(v))\n        if f.is_integer():\n            return [str(int(f))]\n        else:\n            txt = ("%f" % f).rstrip(\'0\').rstrip(\'.\')\n            return [txt]\n    except Exception:\n        return [str(v)]'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s)'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER_TYPE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'IS_FACULTY', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MOIRA_LIST_DESCRIPTION'] = tmp_1['MOIRA_LIST_DESCRIPTION'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST', 'IS_PUBLIC', 'IS_HIDDEN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

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
    tmp_1['moira_list_member'] = tmp_1['moira_list_member'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import math\n    v = None if s is None or (isinstance(s, float) and math.isnan(s)) or str(s).strip().lower()==\'nan\' else s\n    if v is None:\n        return [None]\n    try:\n        f = float(str(v))\n        if f.is_integer():\n            return [str(int(f))]\n        else:\n            txt = ("%f" % f).rstrip(\'0\').rstrip(\'.\')\n            return [txt]\n    except Exception:\n        return [str(v)]', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_2['MOIRA_LIST_MEMBER_MIT_ID'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['MOIRA_LIST_MEMBER_MIT_ID'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s)', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['MOIRA_LIST_OWNER_KEY'] = tmp_3['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID']].copy()
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
    result = tmp_2.loc[:, ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['MIT_ID', 'IS_FACULTY', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='MOIRA_LIST_KEY').merge(prepared_table_3, how='left', on='MOIRA_LIST_OWNER_KEY')
# Identify Professor Ayden Hopkins memberships by robust name matching over member full name and login
name_mask = False
if 'MOIRA_LIST_MEMBER_FULL_NAME' in integrated.columns:
    name_mask = name_mask | integrated['MOIRA_LIST_MEMBER_FULL_NAME'].fillna('').str.contains('ayden', case=False) & integrated['MOIRA_LIST_MEMBER_FULL_NAME'].fillna('').str.contains('hopkins', case=False)
if 'moira_list_member' in integrated.columns:
    name_mask = name_mask | integrated['moira_list_member'].fillna('').str.contains('ayden', case=False) | integrated['moira_list_member'].fillna('').str.contains('hopkins', case=False)
subs = integrated[name_mask].copy()
# Filter lists whose names begin with R (case-insensitive)
subs = subs[subs['MOIRA_LIST_NAME'].fillna('').str.match(r'^[rR]')]
# Bring in faculty attributes for counting tenured faculty
with_fac = subs.merge(prepared_table_4, how='left', left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID')
# Derive tenure flag heuristically: consider tenured faculty as IS_FACULTY == 'Y' and personnel subarea codes/names suggesting tenure
is_faculty = with_fac['IS_FACULTY'].fillna('').str.upper().eq('Y')
psa = with_fac['PERSONNEL_SUBAREA'].fillna('') + ' ' + with_fac['PERSONNEL_SUBAREA_CODE'].fillna('')
# Broad match for tenure indicators
tenure_mask = is_faculty & psa.str.contains('tenure|tenured|professor|faculty', case=False)
with_fac['TENURED_FACULTY_FLAG'] = tenure_mask.astype(int)
# Aggregate per list
agg = with_fac.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'OWNER'], dropna=False).agg(
    number_of_people_in_list=('MOIRA_LIST_MEMBER_MIT_ID', 'count'),
    number_of_tenured_faculty_in_list=('TENURED_FACULTY_FLAG', 'sum')
).reset_index()
# Final projection as requested
target = agg[['MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'OWNER', 'number_of_people_in_list', 'number_of_tenured_faculty_in_list']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
