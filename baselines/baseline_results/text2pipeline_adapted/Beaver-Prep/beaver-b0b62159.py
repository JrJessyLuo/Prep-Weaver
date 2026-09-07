import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'MOIRA_LIST_MEMBER_MIT_ID', 'target_columns': ['MIT_ID_STR', '_drop_tmp'], 'func': "def transform(s):\n    import math\n    v = s\n    if v is None or (isinstance(v, float) and math.isnan(v)):\n        return [None, None]\n    try:\n        f = float(v)\n        i = int(f)\n        return [str(i), None]\n    except Exception:\n        try:\n            # if already string like '984301411.0'\n            if isinstance(v, str) and v.endswith('.0') and v.replace('.0','').isdigit():\n                return [v[:-2], None]\n        except Exception:\n            pass\n        return [str(v), None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_drop_tmp']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    return str(s).upper()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MOIRA_LIST_KEY', 'new_name': 'LIST_KEY'}, {'old_name': 'moira_list_member', 'new_name': 'KRB_NAME_UPPER'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIST_KEY', 'KRB_NAME_UPPER', 'MIT_ID_STR', 'MOIRA_LIST_MEMBER_FULL_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'KRB_NAME_UPPERCASE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'KRB_NAME', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFICE_LOCATION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'MIT_ID', 'new_name': 'MIT_ID_STR'}, {'old_name': 'KRB_NAME_UPPERCASE', 'new_name': 'KRB_NAME_UPPER'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MIT_ID_STR', 'KRB_NAME_UPPER', 'OFFICE_LOCATION', 'FIRST_NAME', 'LAST_NAME', 'UNIT_NAME']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'BUILDING_MAILING_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_COUNTER', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['moira_list_member'] = tmp_0['moira_list_member'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import math\n    v = s\n    if v is None or (isinstance(v, float) and math.isnan(v)):\n        return [None, None]\n    try:\n        f = float(v)\n        i = int(f)\n        return [str(i), None]\n    except Exception:\n        try:\n            # if already string like '984301411.0'\n            if isinstance(v, str) and v.endswith('.0') and v.replace('.0','').isdigit():\n                return [v[:-2], None]\n        except Exception:\n            pass\n        return [str(v), None]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['MIT_ID_STR'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['_drop_tmp'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: DropColumn
    tmp_2 = tmp_1.drop(columns=['_drop_tmp'], errors='ignore').copy()
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).upper()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['moira_list_member'] = tmp_3['moira_list_member'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'MOIRA_LIST_KEY': 'LIST_KEY', 'moira_list_member': 'KRB_NAME_UPPER'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['LIST_KEY', 'KRB_NAME_UPPER', 'MIT_ID_STR', 'MOIRA_LIST_MEMBER_FULL_NAME']].copy()
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
    tmp_1['KRB_NAME_UPPERCASE'] = tmp_1['KRB_NAME_UPPERCASE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['KRB_NAME'] = tmp_2['KRB_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['OFFICE_LOCATION'] = tmp_3['OFFICE_LOCATION'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'MIT_ID': 'MIT_ID_STR', 'KRB_NAME_UPPERCASE': 'KRB_NAME_UPPER'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['MIT_ID_STR', 'KRB_NAME_UPPER', 'OFFICE_LOCATION', 'FIRST_NAME', 'LAST_NAME', 'UNIT_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'BUILDING_MAILING_ADDRESS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_COUNTER', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
_frames = []
if isinstance(prepared_table_1, pd.DataFrame) and not prepared_table_1.empty:
    _tmp = prepared_table_1.copy()
    _tmp['__prepared_table__'] = 'prepared_table_1'
    _frames.append(_tmp)
if isinstance(prepared_table_2, pd.DataFrame) and not prepared_table_2.empty:
    _tmp = prepared_table_2.copy()
    _tmp['__prepared_table__'] = 'prepared_table_2'
    _frames.append(_tmp)
if isinstance(prepared_table_3, pd.DataFrame) and not prepared_table_3.empty:
    _tmp = prepared_table_3.copy()
    _tmp['__prepared_table__'] = 'prepared_table_3'
    _frames.append(_tmp)
target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
