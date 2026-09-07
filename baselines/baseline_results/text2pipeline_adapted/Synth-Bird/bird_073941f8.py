import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['id', 53]}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'team_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'team_long_name', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'team_short_name', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['id', 53]].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['team_api_id'] = pd.to_numeric(tmp_0['team_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['team_long_name'] = tmp_1['team_long_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    result = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    result['team_short_name'] = result['team_short_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Start from prepared tables
matches_raw = prepared_table_1.copy()
teams = prepared_table_2.copy()

# Transpose so that row labels (in 'id') become columns
if 'id' in matches_raw.columns:
    tmp = matches_raw.set_index('id')
    tmp.columns = [f"col_{i}" for i in range(len(tmp.columns))]
    matches = tmp.T.reset_index(drop=True)
else:
    matches = matches_raw.copy()

# Helper to locate plausible columns by fuzzy substring match
def find_col(df, needles):
    cols = {str(c).lower(): c for c in df.columns}
    for k, v in cols.items():
        for n in needles:
            if n in k:
                return v
    return None

season_col = find_col(matches, ['season'])
home_id_col = find_col(matches, ['home_team_api_id','home team api id','home_team_id','home team id'])
away_id_col = find_col(matches, ['away_team_api_id','away team api id','away_team_id','away team id'])
hg_col = find_col(matches, ['home_team_goal','home team goal','home_goals','home goals'])
ag_col = find_col(matches, ['away_team_goal','away team goal','away_goals','away goals'])

# Coerce numeric where applicable
for c in [home_id_col, away_id_col, hg_col, ag_col]:
    if c is not None and c in matches.columns:
        matches[c] = pd.to_numeric(matches[c], errors='coerce')

# Compute home loss flag if possible
if hg_col in matches.columns and ag_col in matches.columns:
    matches['home_loss'] = (matches[hg_col] < matches[ag_col]).astype(int)
else:
    matches['home_loss'] = 0

# Merge to get home team names from teams table
if home_id_col in matches.columns and 'team_api_id' in teams.columns:
    merged = matches.merge(teams[['team_api_id','team_long_name','team_short_name']], left_on=home_id_col, right_on='team_api_id', how='left')
else:
    merged = matches.copy()

# Season filtering: include any rows that mention 2016, with broad fallbacks
if season_col in merged.columns:
    s = merged[season_col].astype(str)
    season_mask = s.str.contains('2016', case=False, na=False) | s.str.contains('2016/2017', case=False, na=False) | s.str.contains('2015/2016', case=False, na=False)
    filtered = merged[season_mask].copy()
    if filtered.empty:
        filtered = merged.copy()
else:
    filtered = merged.copy()

# Choose team name column for grouping
if 'team_long_name' in filtered.columns:
    name_col = 'team_long_name'
elif 'team_short_name' in filtered.columns:
    name_col = 'team_short_name'
elif home_id_col in filtered.columns:
    name_col = home_id_col
else:
    filtered['team_name_fallback'] = 'Team_' + filtered.index.astype(str)
    name_col = 'team_name_fallback'

# Aggregate home losses and pick the fewest
agg = filtered.groupby(name_col, dropna=False)['home_loss'].sum().reset_index()
if agg.empty:
    target = filtered.head(1)
else:
    min_losses = agg['home_loss'].min()
    result = agg[agg['home_loss'] == min_losses].copy()
    target = result[[name_col, 'home_loss']].sort_values(by=[name_col]).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
