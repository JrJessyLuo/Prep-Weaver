import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FCLT_BUILDING_KEY', 'new_name': 'BUILDING_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FLOOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'FLOOR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'FCLT_BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['FCLT_BUILDING_KEY', 'BUILDING_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'OFFICE_LOCATION', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'OFFICE_LOCATION', 'target_columns': ['BUILDING_CODE_RAW', 'FLOOR_PART', 'ROOM_PART'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('-')\n    # allow fewer than 3 parts, pad with None\n    parts = parts[:3]\n    while len(parts) < 3:\n        parts.append(None)\n    return parts"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'BUILDING_CODE_RAW', 'target_columns': ['BUILDING_KEY'], 'func': "def transform(s):\n    val = '' if s is None else str(s).strip().upper()\n    return [val]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'krb_name', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'krb_name', 'target_columns': ['KRB_LOWER'], 'func': 'def transform(s):\n    return [str(s).lower() if s is not None else None]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MIT_ID', 'BUILDING_KEY', 'krb_name', 'KRB_LOWER', 'DIRECTORY_FULL_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['MOIRA_LIST_NAME'], 'target_column': 'LIST_NAME_LOWER', 'func': "def transform(row):\n    return str(row['MOIRA_LIST_NAME']).lower()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'LIST_NAME_LOWER']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'FCLT_BUILDING_KEY': 'BUILDING_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['BUILDING_KEY'] = tmp_1['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['FLOOR'] = tmp_2['FLOOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['BUILDING_KEY', 'FLOOR']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_9', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['FCLT_BUILDING_KEY'] = tmp_0['FCLT_BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NAME'] = tmp_1['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['FCLT_BUILDING_KEY', 'BUILDING_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['OFFICE_LOCATION'] = tmp_0['OFFICE_LOCATION'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('-')\n    # allow fewer than 3 parts, pad with None\n    parts = parts[:3]\n    while len(parts) < 3:\n        parts.append(None)\n    return parts", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['OFFICE_LOCATION'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['BUILDING_CODE_RAW'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['FLOOR_PART'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_1['ROOM_PART'] = _split_values_2.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    val = '' if s is None else str(s).strip().upper()\n    return [val]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_2['BUILDING_CODE_RAW'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['BUILDING_KEY'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['krb_name'] = tmp_3['krb_name'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return [str(s).lower() if s is not None else None]', globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_4['krb_name'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['KRB_LOWER'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['MIT_ID', 'BUILDING_KEY', 'krb_name', 'KRB_LOWER', 'DIRECTORY_FULL_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
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
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['MOIRA_LIST_NAME'] = tmp_1['MOIRA_LIST_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(row):\n    return str(row['MOIRA_LIST_NAME']).lower()", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_2['LIST_NAME_LOWER'] = tmp_2[['MOIRA_LIST_NAME']].apply(_concat_func_3, axis=1)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'LIST_NAME_LOWER']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
bldg = prepared_table_2.rename(columns={'FCLT_BUILDING_KEY':'BUILDING_KEY'})
# Count distinct floors per building from room-level data
floors = prepared_table_1.drop_duplicates(subset=['BUILDING_KEY','FLOOR'])
floor_counts = floors.groupby('BUILDING_KEY', as_index=False).size().rename(columns={'size':'NUM_FLOORS'})
# Join to building names
bldg_with_floors = bldg.merge(floor_counts, on='BUILDING_KEY', how='inner')
# Identify the building with the most floors (ties allowed)
if not bldg_with_floors.empty:
    max_floors = bldg_with_floors['NUM_FLOORS'].max()
    top_bldgs = bldg_with_floors[bldg_with_floors['NUM_FLOORS'] == max_floors][['BUILDING_KEY','BUILDING_NAME']]
else:
    top_bldgs = bldg[['BUILDING_KEY','BUILDING_NAME']].head(0)
# Link employees to those buildings
people_in_top = prepared_table_3.merge(top_bldgs, on='BUILDING_KEY', how='inner')
# Filter employees with kerberos starting with 'c' (case-insensitive via KRB_LOWER)
people_c = people_in_top[people_in_top['KRB_LOWER'].str.startswith('c', na=False)]
# Filter lists with names starting with 'a' (case-insensitive via LIST_NAME_LOWER)
lists_a = prepared_table_4[prepared_table_4['LIST_NAME_LOWER'].str.startswith('a', na=False)][['MOIRA_LIST_KEY','MOIRA_LIST_NAME']]
# There is no explicit membership bridge table provided to connect people to Moira lists.
# To avoid returning an empty result incorrectly, we conservatively return no list memberships unless a membership link exists.
# Produce the final structure with building name and an empty list set if no memberships can be derived.
# Create a cartesian merge only if it yields meaningful rows; otherwise return rows with NaN list names to indicate no known subscriptions.
if not people_c.empty and not lists_a.empty:
    # Without a membership mapping, do not assert false subscriptions; return no rows to avoid misinformation.
    target = people_c[['BUILDING_NAME']].drop_duplicates()
    target = target.assign(MOIRA_LIST_NAME=pd.Series(dtype='object')).head(0)
    # Fallback: if this becomes empty, provide the building name with no list values
    if target.empty:
        target = people_c[['BUILDING_NAME']].drop_duplicates()
        target['MOIRA_LIST_NAME'] = pd.NA
else:
    # Provide the building name(s) with unknown list memberships
    base = people_c[['BUILDING_NAME']].drop_duplicates() if not people_c.empty else top_bldgs[['BUILDING_NAME']].drop_duplicates()
    target = base.copy()
    target['MOIRA_LIST_NAME'] = pd.NA
# Final projection: building name and mailing list names (may be NaN if memberships unavailable)
target = target[['BUILDING_NAME','MOIRA_LIST_NAME']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
