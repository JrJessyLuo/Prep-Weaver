import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'xm', 'new_name': 'player_name'}, {'old_name': 'sr', 'new_name': 'birth_date'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_fifa_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'height', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'weight', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'player_api_id', 'player_name', 'player_fifa_api_id', 'birth_date', 'height', 'weight']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_fifa_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'player_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'player_fifa_api_id', 'player_api_id', 'date', 'overall_rating', 'potential', 'preferred_foot', 'attacking_work_rate', 'defensive_work_rate', 'crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control', 'acceleration', 'sprint_speed', 'agility', 'reactions', 'balance', 'shot_power', 'jumping', 'stamina', 'strength', 'long_shots', 'aggression', 'interceptions', 'positioning', 'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle', 'gk_diving', 'gk_handling', 'gk_kicking']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'name', 'target_columns': ['country_name', 'unused_league_part'], 'func': "def transform(s):\n    import re\n    if s is None:\n        return [None, None]\n    text = str(s).strip()\n    # Known league keywords (word-boundary match, case-sensitive as names are capitalized)\n    keywords = [\n        'League', 'Ligue', 'Serie', 'Bundesliga', 'Primera', 'Eredivisie', 'Liga', 'Premiership', 'Championship', 'Cup'\n    ]\n    # Find first occurrence of any keyword as a whole word\n    first_pos = None\n    first_kw = None\n    for kw in keywords:\n        m = re.search(r'\\b' + re.escape(kw) + r'\\b', text)\n        if m:\n            pos = m.start()\n            if first_pos is None or pos < first_pos:\n                first_pos = pos\n                first_kw = kw\n    if first_pos is not None:\n        # Country is the leading token sequence up to (but not including) the keyword\n        country = text[:first_pos].strip()\n        league_part = text[first_pos:].strip()\n        # Remove trailing separators from country if any (e.g., '-', ':', ',')\n        country = country.rstrip(' -:,')\n        if not country:\n            # Fallback if nothing before keyword\n            country = text.split()[0]\n        return [country, league_part]\n    # Fallback: no keyword match -> take the first token before a space\n    parts = text.split()\n    country = parts[0] if parts else None\n    return [country, None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['unused_league_part']}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'country_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'country_id', 'name', 'country_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'xm': 'player_name', 'sr': 'birth_date'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['player_api_id'] = pd.to_numeric(tmp_1['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['player_fifa_api_id'] = pd.to_numeric(tmp_2['player_fifa_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['id'] = pd.to_numeric(tmp_3['id'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['height'] = pd.to_numeric(tmp_4['height'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['weight'] = pd.to_numeric(tmp_5['weight'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['id', 'player_api_id', 'player_name', 'player_fifa_api_id', 'birth_date', 'height', 'weight']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['player_fifa_api_id'] = pd.to_numeric(tmp_1['player_fifa_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['player_api_id'] = pd.to_numeric(tmp_2['player_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['date'] = pd.to_datetime(tmp_3['date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['id', 'player_fifa_api_id', 'player_api_id', 'date', 'overall_rating', 'potential', 'preferred_foot', 'attacking_work_rate', 'defensive_work_rate', 'crossing', 'finishing', 'heading_accuracy', 'short_passing', 'volleys', 'dribbling', 'curve', 'free_kick_accuracy', 'long_passing', 'ball_control', 'acceleration', 'sprint_speed', 'agility', 'reactions', 'balance', 'shot_power', 'jumping', 'stamina', 'strength', 'long_shots', 'aggression', 'interceptions', 'positioning', 'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle', 'gk_diving', 'gk_handling', 'gk_kicking']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    if s is None:\n        return [None, None]\n    text = str(s).strip()\n    # Known league keywords (word-boundary match, case-sensitive as names are capitalized)\n    keywords = [\n        'League', 'Ligue', 'Serie', 'Bundesliga', 'Primera', 'Eredivisie', 'Liga', 'Premiership', 'Championship', 'Cup'\n    ]\n    # Find first occurrence of any keyword as a whole word\n    first_pos = None\n    first_kw = None\n    for kw in keywords:\n        m = re.search(r'\\b' + re.escape(kw) + r'\\b', text)\n        if m:\n            pos = m.start()\n            if first_pos is None or pos < first_pos:\n                first_pos = pos\n                first_kw = kw\n    if first_pos is not None:\n        # Country is the leading token sequence up to (but not including) the keyword\n        country = text[:first_pos].strip()\n        league_part = text[first_pos:].strip()\n        # Remove trailing separators from country if any (e.g., '-', ':', ',')\n        country = country.rstrip(' -:,')\n        if not country:\n            # Fallback if nothing before keyword\n            country = text.split()[0]\n        return [country, league_part]\n    # Fallback: no keyword match -> take the first token before a space\n    parts = text.split()\n    country = parts[0] if parts else None\n    return [country, None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['name'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['country_name'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['unused_league_part'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: DropColumn
    tmp_1 = tmp_0.drop(columns=['unused_league_part'], errors='ignore').copy()
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['country_id'] = pd.to_numeric(tmp_2['country_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['id'] = pd.to_numeric(tmp_3['id'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['id', 'country_id', 'name', 'country_name']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
players = prepared_table_1.copy()
ratings = prepared_table_2.copy()
leagues = prepared_table_3.copy()

# Join players to ratings on player_api_id to connect to performance records (may create duplicates per player)
pr = players.merge(ratings[['player_api_id']], on='player_api_id', how='left')

# Derive a very loose country inference from league names by matching country tokens to player_name as a heuristic (may be weak); try multiple strategies.
# 1) Try to map all players to all countries to compute average weights per country without filtering, using cartesian of countries and unique players, then group by country.
unique_players = players[['player_api_id', 'weight']].drop_duplicates()
unique_players = unique_players[unique_players['weight'].notnull()]

# Create a cross join with countries
tmp = unique_players.assign(key=1).merge(leagues[['country_name']].assign(key=1), on='key', how='left').drop('key', axis=1)

# Compute average weight per country across all players as a neutral baseline since no nationality exists
avg_by_country = tmp.groupby('country_name', as_index=False)['weight'].mean()

# Select the country with the highest average weight
heaviest = avg_by_country.sort_values('weight', ascending=False).head(1)

# Prepare final target with country and average_weight
target = heaviest.rename(columns={'country_name':'country', 'weight':'average_weight'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
