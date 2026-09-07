import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_BUILT', 'date_format': '%m/%d/%Y'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'DATE_BUILT', 'new_name': 'DATE_BUILT_DT'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'DATE_BUILT_DT', 'target_columns': ['BUILT_YEAR'], 'func': 'def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year)]\n    except Exception:\n        return [None]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'DATE_BUILT_DT', 'BUILT_YEAR']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'BUILDING_ROOM', 'target_columns': ['BUILDING_NUMBER_RAW', 'rest'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NUMBER_RAW', 'func': "def transform(s):\n    s = '' if s is None else str(s).strip()\n    # Remove leading zeros that are purely padding; preserve '0' as '0'\n    if s == '':\n        return ''\n    # Keep signless numeric-like strings only; otherwise return trimmed\n    if s.isdigit():\n        # strip leading zeros, but keep single zero\n        s2 = s.lstrip('0')\n        return s2 if s2 != '' else '0'\n    return s"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'BUILDING_NUMBER_RAW', 'new_name': 'BUILDING_NUMBER'}]}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['rest']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_NUMBER', 'BUILDING_ROOM', 'BUILDING_COMPONENT', 'FLOOR', 'SPACE_USAGE', 'SPACE_UNIT_CODE', 'HR_ORG_UNIT_ID', 'ACCESS_LEVEL']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['BUILDING_NUMBER'] = tmp_0['BUILDING_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['DATE_BUILT'] = pd.to_datetime(tmp_1['DATE_BUILT'], errors='coerce').dt.strftime('%m/%d/%Y')
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'DATE_BUILT': 'DATE_BUILT_DT'})
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year)]\n    except Exception:\n        return [None]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_3['DATE_BUILT_DT'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['BUILT_YEAR'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'DATE_BUILT_DT', 'BUILT_YEAR']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['BUILDING_ROOM'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['BUILDING_NUMBER_RAW'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['rest'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s).strip()\n    # Remove leading zeros that are purely padding; preserve '0' as '0'\n    if s == '':\n        return ''\n    # Keep signless numeric-like strings only; otherwise return trimmed\n    if s.isdigit():\n        # strip leading zeros, but keep single zero\n        s2 = s.lstrip('0')\n        return s2 if s2 != '' else '0'\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['BUILDING_NUMBER_RAW'] = tmp_1['BUILDING_NUMBER_RAW'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'BUILDING_NUMBER_RAW': 'BUILDING_NUMBER'})
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['rest'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_NUMBER', 'BUILDING_ROOM', 'BUILDING_COMPONENT', 'FLOOR', 'SPACE_USAGE', 'SPACE_UNIT_CODE', 'HR_ORG_UNIT_ID', 'ACCESS_LEVEL']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='BUILDING_NUMBER', how='inner')
# Treat each room row as one occupied space proxy; count rows per building as employee/occupant proxy
emp_counts = integrated.groupby(['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILT_YEAR'], as_index=False).size()
emp_counts = emp_counts.rename(columns={'size': 'num_employees'})
# Buildings constructed before 1950 with more than 100 employees
result = emp_counts[(emp_counts['BUILT_YEAR'].notna()) & (emp_counts['BUILT_YEAR'] < 1950) & (emp_counts['num_employees'] > 100)]
# Final projection and sort by name
target = result[['BUILDING_NAME_LONG', 'BUILT_YEAR', 'num_employees']].sort_values(['BUILDING_NAME_LONG', 'BUILT_YEAR']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
