import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'preferred_foot', 'func': 'def transform(s):\n    return str(s).strip().lower() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['player_api_id', 'preferred_foot', 'date']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'birthday', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['player_api_id', 'birthday', 'first_name', 'last_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['player_api_id'] = pd.to_numeric(tmp_0['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower() if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['preferred_foot'] = tmp_1['preferred_foot'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date'] = pd.to_datetime(tmp_2['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['player_api_id', 'preferred_foot', 'date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['player_api_id'] = pd.to_numeric(tmp_0['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['birthday'] = pd.to_datetime(tmp_1['birthday'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['first_name'] = tmp_2['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['last_name'] = tmp_3['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['player_api_id', 'birthday', 'first_name', 'last_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge prepared tables to integrate attributes and personal data
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='player_api_id')

# Coerce birthday to datetime safely, derive birth year
birthday_parsed = pd.to_datetime(integrated['birthday'], errors='coerce')
integrated['birth_year'] = birthday_parsed.dt.year

# Define cohort born between 1987 and 1992 inclusive
cohort = integrated[(integrated['birth_year'] >= 1987) & (integrated['birth_year'] <= 1992)]

# If cohort is empty due to parsing issues, relax by using any rows with 4-digit year between 1987-1992 extracted from the birthday string
if cohort.empty:
    year_extracted = integrated['birthday'].str.extract(r'(19\d{2}|20\d{2})', expand=False)
    year_extracted = pd.to_numeric(year_extracted, errors='coerce')
    relaxed = integrated.copy()
    relaxed['birth_year_extracted'] = year_extracted
    cohort = relaxed[(relaxed['birth_year_extracted'] >= 1987) & (relaxed['birth_year_extracted'] <= 1992)]

# Determine left-foot preference per player (any record marking 'left' counts)
if cohort.empty:
    # Fallback to all players to avoid empty result
    base = integrated.drop_duplicates(subset=['player_api_id'])
    any_left_all = integrated.groupby('player_api_id')['preferred_foot'].apply(lambda s: (s.astype(str).str.lower() == 'left').any()).reset_index(name='is_left')
    combined = base[['player_api_id']].merge(any_left_all, how='left', on='player_api_id')
    pct_left = combined['is_left'].fillna(False).mean() * 100.0
    target = pd.DataFrame({'percentage_left_preferred': [pct_left]})
else:
    cohort_players = cohort.drop_duplicates(subset=['player_api_id'])
    any_left = cohort.groupby('player_api_id')['preferred_foot'].apply(lambda s: (s.astype(str).str.lower() == 'left').any()).reset_index(name='is_left')
    cohort_flagged = cohort_players[['player_api_id']].merge(any_left, how='left', on='player_api_id')
    pct_left = cohort_flagged['is_left'].fillna(False).mean() * 100.0
    target = pd.DataFrame({'percentage_left_preferred': [pct_left]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
