import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Conference_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Conference_ID', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    # remove surrounding single/double quotes\n    if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in [\'"\', "\'"]):\n        s = s[1:-1]\n    return s.strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ConfName_Year', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    # trim and normalize internal spaces around delimiters\n    s = s.strip()\n    # collapse multiple spaces\n    s = re.sub(r'\\s+', ' ', s)\n    # normalize spaces around non-alnum delimiters like #, _, -\n    s = re.sub(r'\\s*([#_\\-])\\s*', r'\\1', s)\n    return s\n"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'ConfName_Year', 'target_columns': ['conf_name_raw', 'year_raw'], 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    # split on any sequence of non-alphanumeric characters\n    tokens = [t for t in re.split(r'[^0-9A-Za-z]+', s) if t]\n    if not tokens:\n        return [None, None]\n    # first token as name, last numeric token as year if present\n    year = None\n    for t in reversed(tokens):\n        if re.fullmatch(r'\\d{2,4}', t):\n            year = t\n            break\n    name = tokens[0]\n    return [name, year]\n"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'conf_name_raw', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    # title case but keep common acronyms uppercase if the token is all letters and originally upper\n    def fix_token(tok):\n        if tok.isupper() and tok.isalpha():\n            return tok\n        return tok.title()\n    tokens = s.split(' ')\n    s = ' '.join(fix_token(t) for t in tokens if t)\n    return s\n"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year_raw', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'conf_name_raw', 'new_name': 'conference_name'}, {'old_name': 'year_raw', 'new_name': 'year'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Conference_ID', 'conference_name', 'year', 'Loc']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Conference_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Conference_ID', 'func': 'def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1].strip()\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'staff_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'role', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Conference_ID', 'staff_ID', 'role']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Conference_ID'] = tmp_0['Conference_ID'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    # remove surrounding single/double quotes\n    if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in [\'"\', "\'"]):\n        s = s[1:-1]\n    return s.strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Conference_ID'] = tmp_1['Conference_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    # trim and normalize internal spaces around delimiters\n    s = s.strip()\n    # collapse multiple spaces\n    s = re.sub(r'\\s+', ' ', s)\n    # normalize spaces around non-alnum delimiters like #, _, -\n    s = re.sub(r'\\s*([#_\\-])\\s*', r'\\1', s)\n    return s\n", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['ConfName_Year'] = tmp_2['ConfName_Year'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    # split on any sequence of non-alphanumeric characters\n    tokens = [t for t in re.split(r'[^0-9A-Za-z]+', s) if t]\n    if not tokens:\n        return [None, None]\n    # first token as name, last numeric token as year if present\n    year = None\n    for t in reversed(tokens):\n        if re.fullmatch(r'\\d{2,4}', t):\n            year = t\n            break\n    name = tokens[0]\n    return [name, year]\n", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['ConfName_Year'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['conf_name_raw'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['year_raw'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    # title case but keep common acronyms uppercase if the token is all letters and originally upper\n    def fix_token(tok):\n        if tok.isupper() and tok.isalpha():\n            return tok\n        return tok.title()\n    tokens = s.split(' ')\n    s = ' '.join(fix_token(t) for t in tokens if t)\n    return s\n", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['conf_name_raw'] = tmp_4['conf_name_raw'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['year_raw'] = pd.to_numeric(tmp_5['year_raw'], errors='coerce').fillna(0).astype(int)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'conf_name_raw': 'conference_name', 'year_raw': 'year'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['Conference_ID', 'conference_name', 'year', 'Loc']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Conference_ID'] = tmp_0['Conference_ID'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1].strip()\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Conference_ID'] = tmp_1['Conference_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['staff_ID'] = pd.to_numeric(tmp_2['staff_ID'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['role'] = tmp_3['role'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Conference_ID', 'staff_ID', 'role']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1[['Conference_ID','conference_name','year']], on='Conference_ID', how='inner')
participants = integrated.groupby(['Conference_ID','conference_name','year'], as_index=False).agg(num_participants=('staff_ID','nunique'))
target = participants[['Conference_ID','conference_name','year','num_participants']].sort_values(['Conference_ID'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
