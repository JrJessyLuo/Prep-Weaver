import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'language', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'set_info', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'set_info', 'target_columns': ['set_code_src', 'set_name'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    if '|' in s:\n        left, right = s.split('|', 1)\n        left = left if left != '' else None\n        right = right\n        return [left, right]\n    else:\n        return [None, s]"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'set_code_src', 'new_name': 'set_code'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'language', 'set_code', 'set_name']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['id', 'flavorText', 'language', 'multiverseid', 'name', 'text', 'type', 'uuid']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['language'] = tmp_1['language'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['set_info'] = tmp_2['set_info'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    if '|' in s:\n        left, right = s.split('|', 1)\n        left = left if left != '' else None\n        right = right\n        return [left, right]\n    else:\n        return [None, s]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['set_info'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['set_code_src'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['set_name'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'set_code_src': 'set_code'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['id', 'language', 'set_code', 'set_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['id', 'flavorText', 'language', 'multiverseid', 'name', 'text', 'type', 'uuid']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t = prepared_table_1.copy()
# Normalize language values for robust matching
lang_norm = t['language'].str.strip().str.lower()
t = t.assign(language_norm=lang_norm)
# Identify sets with Korean translation and those with Japanese translation
has_ko = t.loc[t['language_norm'].eq('korean'), ['set_code']].drop_duplicates()
has_ja = t.loc[t['language_norm'].eq('japanese'), ['set_code']].drop_duplicates()
# Sets that have Korean but not Japanese
ko_not_ja = has_ko.merge(has_ja, on='set_code', how='left', indicator=True)
ko_not_ja = ko_not_ja.loc[ko_not_ja['_merge'] == 'left_only', ['set_code']]
# For those sets, list the set names (from any available language; prefer Korean name when available)
subset = t.merge(ko_not_ja, on='set_code', how='inner')
# Prefer Korean names when available, otherwise fall back to any name for the set
subset['is_korean'] = subset['language_norm'].eq('korean')
subset = subset.sort_values(['set_code', 'is_korean'], ascending=[True, False])
# Take first name per set_code after preferring Korean
names = subset.groupby('set_code', as_index=False).first()[['set_code', 'set_name']]
# Final target: list of set names without Japanese translation but with Korean translation
target = names[['set_name']].drop_duplicates().rename(columns={'set_name': 'set_name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
