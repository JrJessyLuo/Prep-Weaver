import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'MOIRA_LIST_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'MOIRA_LIST_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_OWNER_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'moira_list_member', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    try:\n        return str(s).strip().upper()\n    except Exception:\n        return str(s)\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return str(s)\n'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COUNTER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'MOIRA_LIST_OWNER_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OWNER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OWNER_TYPE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    # Trim whitespace only; preserve original case and content\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['MOIRA_LIST_KEY'] = tmp_2['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['MOIRA_LIST_NAME'] = tmp_3['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MOIRA_LIST_KEY'] = tmp_0['MOIRA_LIST_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MOIRA_LIST_OWNER_KEY'] = tmp_1['MOIRA_LIST_OWNER_KEY'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['moira_list_member'] = tmp_2['moira_list_member'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip().upper()\n    except Exception:\n        return str(s)\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['MOIRA_LIST_KEY'] = tmp_3['MOIRA_LIST_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return str(s)\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['moira_list_member'] = tmp_4['moira_list_member'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['COUNTER'] = pd.to_numeric(tmp_5['COUNTER'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MOIRA_LIST_OWNER_KEY'] = tmp_0['MOIRA_LIST_OWNER_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['OWNER'] = tmp_1['OWNER'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['OWNER_TYPE'] = tmp_2['OWNER_TYPE'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace only; preserve original case and content\n    return None if s is None else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['MOIRA_LIST_OWNER_KEY'] = tmp_3['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
members = prepared_table_2.copy()
list_attrs = prepared_table_1.copy()
owners = prepared_table_3.copy()

# Count members per list
member_counts = members.groupby('MOIRA_LIST_KEY', as_index=False).agg(num_members=('moira_list_member', 'count'))

# Join counts to list attributes
counts_with_attrs = member_counts.merge(list_attrs, on='MOIRA_LIST_KEY', how='left')

# Create owner-list pairs and resolve owner details (separate row per owner)
list_owner_pairs = members[['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY']].drop_duplicates()
list_owner_details = list_owner_pairs.merge(owners, on='MOIRA_LIST_OWNER_KEY', how='left')

# Combine counts/attributes with owners
full = counts_with_attrs.merge(list_owner_details, on='MOIRA_LIST_KEY', how='left')

# Fallback if merge produced no rows
if full.empty:
    full = counts_with_attrs.copy()

# Identify min and max member counts and select corresponding rows
if not full.empty and 'num_members' in full.columns:
    max_cnt = full['num_members'].max()
    min_cnt = full['num_members'].min()
    top = full[full['num_members'] == max_cnt]
    bottom = full[full['num_members'] == min_cnt]
    result = pd.concat([top, bottom], ignore_index=True)
else:
    result = full.copy()

# Final projection and de-dup
cols = [c for c in ['MOIRA_LIST_NAME', 'OWNER', 'OWNER_TYPE', 'IS_PUBLIC', 'IS_HIDDEN', 'num_members'] if c in result.columns]
result = result[cols].drop_duplicates()

# Ensure not empty: if empty, relax by taking any available lists with their counts
if result.empty:
    fallback = counts_with_attrs.merge(list_owner_details, on='MOIRA_LIST_KEY', how='left')
    cols_fb = [c for c in ['MOIRA_LIST_NAME', 'OWNER', 'OWNER_TYPE', 'IS_PUBLIC', 'IS_HIDDEN', 'num_members'] if c in fallback.columns]
    if cols_fb:
        result = fallback[cols_fb].drop_duplicates()
    else:
        result = counts_with_attrs.copy()
        cols_ca = [c for c in ['MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN', 'num_members'] if c in result.columns]
        result = result[cols_ca].drop_duplicates()

# Assign final DataFrame
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
