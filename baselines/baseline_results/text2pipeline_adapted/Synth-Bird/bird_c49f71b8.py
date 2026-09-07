import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'team_api_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name']}, 'table_indices': [0]}], [{'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'team_fifa_api_id', 'team_api_id', 'date', 'buildUpPlaySpeed', 'buildUpPlaySpeedClass', 'buildUpPlayDribbling', 'buildUpPlayDribblingClass', 'buildUpPlayPassing', 'buildUpPlayPassingClass', 'buildUpPlayPositioningClass', 'chanceCreationPassing', 'chanceCreationPassingClass', 'chanceCreationCrossing', 'chanceCreationCrossingClass', 'chanceCreationShooting', 'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressure', 'defencePressureClass', 'defenceAggression', 'defenceAggressionClass', 'defenceTeamWidth', 'defenceTeamWidthClass', 'defenceDefenderLineClass']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['team_api_id'] = pd.to_numeric(tmp_0['team_api_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['id', 'team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['date'] = pd.to_datetime(tmp_0['date'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['id', 'team_fifa_api_id', 'team_api_id', 'date', 'buildUpPlaySpeed', 'buildUpPlaySpeedClass', 'buildUpPlayDribbling', 'buildUpPlayDribblingClass', 'buildUpPlayPassing', 'buildUpPlayPassingClass', 'buildUpPlayPositioningClass', 'chanceCreationPassing', 'chanceCreationPassingClass', 'chanceCreationCrossing', 'chanceCreationCrossingClass', 'chanceCreationShooting', 'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressure', 'defencePressureClass', 'defenceAggression', 'defenceAggressionClass', 'defenceTeamWidth', 'defenceTeamWidthClass', 'defenceDefenderLineClass']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='team_api_id')
mask = integrated['team_long_name'].str.contains('Heart of Midlothian', case=False, na=False)
subset = integrated[mask]
if subset.empty:
    # Fallback: try matching by short name patterns (e.g., HEARTS) or partial 'Hearts'
    alt_mask = integrated['team_long_name'].str.contains('Hearts|Heart', case=False, na=False)
    subset = integrated[alt_mask]
# Compute the average build up play speed for the matched team rows
result = subset[['team_long_name', 'buildUpPlaySpeed']].copy()
agg = result.groupby('team_long_name', as_index=False)['buildUpPlaySpeed'].mean()
agg.rename(columns={'buildUpPlaySpeed': 'average_buildUpPlaySpeed'}, inplace=True)
target = agg

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
