import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['raceId', 'year']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'fastestLapSpeed', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'fastestLapSpeed']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['raceId', 'year']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['fastestLapSpeed'] = pd.to_numeric(tmp_0['fastestLapSpeed'], errors='coerce').astype(float)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['raceId', 'fastestLapSpeed']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_11', pd.DataFrame()))

# Stage-2 program over the prepared tables.
merged = prepared_table_2.merge(prepared_table_1, on='raceId', how='inner')
# Compute the minimum fastest lap speed per year, then select the year with the overall lowest speed
by_year = merged.groupby('year', as_index=False)['fastestLapSpeed'].min()
# Identify the year(s) with the global minimum speed
min_speed = by_year['fastestLapSpeed'].min()
result = by_year[by_year['fastestLapSpeed'] == min_speed]
# If multiple years tie, keep them all
target = result[['year']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
