import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': "def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else None"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'MOIRA_LIST_MEMBER_MIT_ID', 'target_columns': ['member_mit_id'], 'func': "def transform(s):\n    import math\n    if s is None or str(s) == 'nan':\n        return [None]\n    try:\n        x = float(s)\n        if math.isnan(x):\n            return [None]\n        return [str(int(x))]\n    except Exception:\n        return [None]"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_KEY', 'new_name': 'list_key'}, {'old_name': 'MOIRA_LIST_OWNER_KEY', 'new_name': 'list_owner_key'}, {'old_name': 'MOIRA_LIST_MEMBER_FULL_NAME', 'new_name': 'member_full_name'}, {'old_name': 'moira_list_member', 'new_name': 'member_login'}, {'old_name': 'LAST_UPDATE_DATE', 'new_name': 'last_update_date'}, {'old_name': 'COUNTER', 'new_name': 'counter'}, {'old_name': 'WAREHOUSE_LOAD_DATE', 'new_name': 'warehouse_load_date'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['list_key', 'list_owner_key', 'member_login', 'member_full_name', 'member_mit_id', 'last_update_date', 'counter', 'warehouse_load_date']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DEPARTMENT_NAME', 'new_name': 'department_name'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'department_name', 'target_columns': ['department_name', 'department_name_upper'], 'func': 'def transform(s):\n    orig = s\n    upper = str(s).upper()\n    return [orig, upper]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'department_name', 'department_name_upper', 'FULL_NAME', 'EMAIL_ADDRESS', 'krb_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None and str(s) != 'nan' else None", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['moira_list_member'] = tmp_0['moira_list_member'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_1['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import math\n    if s is None or str(s) == 'nan':\n        return [None]\n    try:\n        x = float(s)\n        if math.isnan(x):\n            return [None]\n        return [str(int(x))]\n    except Exception:\n        return [None]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['MOIRA_LIST_MEMBER_MIT_ID'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['member_mit_id'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'MOIRA_LIST_KEY': 'list_key', 'MOIRA_LIST_OWNER_KEY': 'list_owner_key', 'MOIRA_LIST_MEMBER_FULL_NAME': 'member_full_name', 'moira_list_member': 'member_login', 'LAST_UPDATE_DATE': 'last_update_date', 'COUNTER': 'counter', 'WAREHOUSE_LOAD_DATE': 'warehouse_load_date'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['list_key', 'list_owner_key', 'member_login', 'member_full_name', 'member_mit_id', 'last_update_date', 'counter', 'warehouse_load_date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MIT_ID'] = tmp_0['MIT_ID'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'DEPARTMENT_NAME': 'department_name'})
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    orig = s\n    upper = str(s).upper()\n    return [orig, upper]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_3['department_name'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['department_name'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['department_name_upper'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MIT_ID', 'department_name', 'department_name_upper', 'FULL_NAME', 'EMAIL_ADDRESS', 'krb_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, left_on='member_mit_id', right_on='MIT_ID', how='left')
# Filter to Electrical Engineering and Computer Science department (robust, case-insensitive)
if 'department_name_upper' in integrated.columns:
    mask_eecs = integrated['department_name_upper'].fillna('').str.contains('ELECTRICAL ENGINEERING AND COMPUTER SCIENCE', case=False, na=False)
else:
    mask_eecs = integrated['department_name'].fillna('').str.contains('Electrical Engineering and Computer Science', case=False, na=False)
filtered = integrated[mask_eecs].copy()
# Consider mailing lists whose names start with 'B' (case-insensitive)
filtered['list_key_upper'] = filtered['list_key'].fillna('').str.upper()
filtered_b = filtered[filtered['list_key_upper'].str.startswith('B')].copy()
# Compute per-list counts of EECS members
counts = filtered_b.groupby('list_key', as_index=False).size().rename(columns={'size':'eecs_member_count'})
# Overall count of distinct lists starting with B that include EECS members
total_lists = len(counts)
# Find the list(s) with the maximum EECS member count
if not counts.empty:
    max_count = counts['eecs_member_count'].max()
    top_lists = counts[counts['eecs_member_count'] == max_count].copy()
    # If multiple tie, take the first alphabetically for determinism
    top_lists = top_lists.sort_values(['list_key']).head(1)
else:
    # Fallback: if no matches, relax department filter by looking for 'EECS' token anywhere
    relaxed = integrated[integrated['department_name'].fillna('').str.contains('EECS', case=False, na=False)].copy()
    relaxed['list_key_upper'] = relaxed['list_key'].fillna('').str.upper()
    filtered_b2 = relaxed[relaxed['list_key_upper'].str.startswith('B')].copy()
    counts = filtered_b2.groupby('list_key', as_index=False).size().rename(columns={'size':'eecs_member_count'})
    total_lists = len(counts)
    if not counts.empty:
        max_count = counts['eecs_member_count'].max()
        top_lists = counts[counts['eecs_member_count'] == max_count].sort_values(['list_key']).head(1)
    else:
        # As last resort, compute over all B lists regardless of department
        all_b = integrated[integrated['list_key'].fillna('').str.upper().str.startswith('B')].copy()
        counts = all_b.groupby('list_key', as_index=False).size().rename(columns={'size':'eecs_member_count'})
        total_lists = len(counts)
        if not counts.empty:
            max_count = counts['eecs_member_count'].max()
            top_lists = counts[counts['eecs_member_count'] == max_count].sort_values(['list_key']).head(1)
        else:
            top_lists = counts.head(0)
            max_count = 0
# Build final target with required outputs: count of such lists, the top list name, and its member count
summary = top_lists.copy()
if summary.empty:
    # Return a single row with totals but empty top list name if none found
    target = counts.head(0).copy()
    target['b_list_count_with_eecs_members'] = [total_lists]
    target['top_b_list_name'] = ['']
    target['top_b_list_eecs_member_count'] = [int(0)]
else:
    summary = summary.assign(b_list_count_with_eecs_members=total_lists)
    summary = summary.rename(columns={'list_key':'top_b_list_name','eecs_member_count':'top_b_list_eecs_member_count'})
    target = summary[['b_list_count_with_eecs_members','top_b_list_name','top_b_list_eecs_member_count']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
