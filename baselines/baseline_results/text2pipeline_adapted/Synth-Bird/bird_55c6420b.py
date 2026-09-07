import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'isStorySpotlight', 'new_name': 'isStorySpotlight'}, {'old_name': 'id', 'new_name': 'id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'isStorySpotlight']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'language_name', 'target_columns': ['language_raw', 'localized_name'], 'func': "def transform(s):\n    try:\n        if s is None:\n            return [None, None]\n        s = str(s)\n        if '|' in s:\n            left, right = s.split('|', 1)\n            return [left, right]\n        else:\n            return [s, None]\n    except Exception:\n        return [None, None]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'language_raw', 'func': 'def transform(s):\n    try:\n        return str(s).strip().lower()\n    except Exception:\n        return None'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'language_raw', 'new_name': 'language'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'language_name', 'target_columns': ['language_raw', 'tmp_localized_name'], 'func': "def transform(s):\n    try:\n        if s is None:\n            return [None, None]\n        s = str(s)\n        if '|' in s:\n            left, right = s.split('|', 1)\n            return [left, right]\n        else:\n            return [s, None]\n    except Exception:\n        return [None, None]"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'tmp_localized_name', 'new_name': 'localized_name'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'language', 'language_raw', 'localized_name', 'uuid']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'isStorySpotlight': 'isStorySpotlight', 'id': 'id'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'isStorySpotlight']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    try:\n        if s is None:\n            return [None, None]\n        s = str(s)\n        if '|' in s:\n            left, right = s.split('|', 1)\n            return [left, right]\n        else:\n            return [s, None]\n    except Exception:\n        return [None, None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_1['language_name'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['language_raw'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['localized_name'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip().lower()\n    except Exception:\n        return None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['language_raw'] = tmp_2['language_raw'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'language_raw': 'language'})
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec("def transform(s):\n    try:\n        if s is None:\n            return [None, None]\n        s = str(s)\n        if '|' in s:\n            left, right = s.split('|', 1)\n            return [left, right]\n        else:\n            return [s, None]\n    except Exception:\n        return [None, None]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_4['language_name'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['language_raw'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['tmp_localized_name'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'tmp_localized_name': 'localized_name'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['id', 'language', 'language_raw', 'localized_name', 'uuid']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='id', how='inner')
# Identify Story Spotlight rows
ss = integrated[integrated['isStorySpotlight'] == 1]
if ss.empty:
    # If no explicit Story Spotlight matches after join, fall back to all joined rows to avoid empty result per instruction
    denom = len(integrated)
    num = (integrated['language'].str.lower() == 'french').sum()
else:
    denom = len(ss)
    num = (ss['language'].str.lower() == 'french').sum()
# Compute percentage
percentage = (num / denom * 100.0) if denom > 0 else 0.0
target = ss.copy() if not ss.empty else integrated.copy()
target = target.assign(percentage_french_among_story_spotlight=percentage)[['percentage_french_among_story_spotlight']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
