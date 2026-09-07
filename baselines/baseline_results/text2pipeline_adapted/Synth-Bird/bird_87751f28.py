import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'personal_info', 'target_columns': ['sex_raw', 'birthdate_raw', 'code_raw'], 'func': "def transform(s):\n    parts = str(s).split('#')\n    parts += [None] * (3 - len(parts))\n    return parts[:3]"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'birthdate_raw', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'birthdate_raw', 'target_columns': ['birth_year'], 'func': 'def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year)]\n    except Exception:\n        return [None]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'birth_year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'birth_year']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'type', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'account_id', 'type']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['account_id', 'district_id']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'kraj', 'func': "def transform(s):\n    import unicodedata\n    if s is None:\n        return None\n    s = str(s).strip().casefold()\n    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))\n    return s"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['district_id', 'kraj']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('#')\n    parts += [None] * (3 - len(parts))\n    return parts[:3]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['personal_info'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['sex_raw'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['birthdate_raw'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_0['code_raw'] = _split_values_1.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['birthdate_raw'] = pd.to_datetime(tmp_1['birthdate_raw'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['client_id'] = pd.to_numeric(tmp_2['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s)\n        return [int(dt.year)]\n    except Exception:\n        return [None]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_3['birthdate_raw'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['birth_year'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['birth_year'] = pd.to_numeric(tmp_4['birth_year'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['client_id', 'birth_year']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['client_id'] = pd.to_numeric(tmp_0['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['account_id'] = pd.to_numeric(tmp_1['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['type'] = tmp_2['type'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['client_id', 'account_id', 'type']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['account_id'] = pd.to_numeric(tmp_0['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['district_id'] = pd.to_numeric(tmp_1['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date'] = pd.to_datetime(tmp_2['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['account_id', 'district_id']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['district_id'] = pd.to_numeric(tmp_0['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import unicodedata\n    if s is None:\n        return None\n    s = str(s).strip().casefold()\n    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['kraj'] = tmp_1['kraj'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['district_id', 'kraj']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='client_id', how='inner').merge(prepared_table_3, on='account_id', how='inner').merge(prepared_table_4, on='district_id', how='inner')
# Filter clients born in 1920 and in east Bohemia (case-insensitive, robust)
mask_year = integrated['birth_year'] == 1920
mask_region = integrated['kraj'].astype(str).str.strip().str.lower() == 'east bohemia'
filtered = integrated[mask_year & mask_region]
# Count unique clients who satisfy the condition (a client may have multiple accounts/dispositions)
result = filtered[['client_id']].drop_duplicates()
target = result.assign(count=1).agg({'count':'sum'}).to_frame().T.rename(columns={'count':'num_clients'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
