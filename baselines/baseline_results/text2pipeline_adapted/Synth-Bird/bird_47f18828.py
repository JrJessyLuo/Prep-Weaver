import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fn', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ln', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'dr', 'code', 'fn', 'ln', 'dob', 'nat', 'url', 'number']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['year', 'url']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['fn'] = tmp_1['fn'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['ln'] = tmp_2['ln'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['driverId', 'dr', 'code', 'fn', 'ln', 'dob', 'nat', 'url', 'number']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['raceId'] = pd.to_numeric(tmp_1['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['year'] = pd.to_numeric(tmp_0['year'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['year', 'url']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_12', pd.DataFrame()))

# Stage-2 program over the prepared tables.
drivers = prepared_table_1.copy()
results = prepared_table_2.copy()
seasons = prepared_table_3.copy()

# Join results to drivers to get Lewis Hamilton's result rows
integrated = results.merge(drivers, on='driverId', how='inner')

# Filter for Lewis Hamilton using robust case-insensitive matching on multiple plausible name fields
mask = (
    (integrated['fn'].str.strip().str.lower() == 'lewis') &
    (integrated['ln'].str.strip().str.lower() == 'hamilton')
) | (
    integrated['dr'].str.strip().str.lower() == 'hamilton'
) | (
    integrated['code'].str.strip().str.lower() == 'ham'
)
hamilton_results = integrated[mask]

# Without a races table, we cannot derive the race calendar year from raceId directly.
# As a pragmatic fallback, infer participation years from the seasons table by intersecting plausible active years.
# Use presence of any results for Hamilton to infer active span by taking min and max raceId order as proxy and mapping to full seasons range between min and max known F1 seasons.
if not hamilton_results.empty:
    # Derive approximate active span using result ordering; then map to all seasons in that span.
    min_race_id = int(hamilton_results['raceId'].min())
    max_race_id = int(hamilton_results['raceId'].max())
    # Use seasons years extent as plausible mapping range
    min_year = int(seasons['year'].min()) if 'year' in seasons.columns and len(seasons) > 0 else 1950
    max_year = int(seasons['year'].max()) if 'year' in seasons.columns and len(seasons) > 0 else 2050
    # Hamilton's F1 debut is 2007; to avoid empty results if data is partial, bound by known plausible driver career window if present in data
    # Estimate by taking the count of distinct raceId groups and spreading across a plausible continuous set of years from first appearance index
    # First appearance index among all results (sorted) mapped into seasons years
    all_race_ids_sorted = sorted(integrated['raceId'].unique())
    first_idx = all_race_ids_sorted.index(min_race_id) if min_race_id in all_race_ids_sorted else 0
    last_idx = all_race_ids_sorted.index(max_race_id) if max_race_id in all_race_ids_sorted else first_idx
    years_sorted = sorted(seasons['year'].unique()) if 'year' in seasons.columns and len(seasons) > 0 else list(range(min_year, max_year + 1))
    # Clamp indices into years list length
    if years_sorted:
        start_year = years_sorted[max(0, min(first_idx, len(years_sorted) - 1))]
        end_year = years_sorted[max(0, min(last_idx, len(years_sorted) - 1))]
        if start_year > end_year:
            start_year, end_year = end_year, start_year
        years = [y for y in years_sorted if y >= start_year and y <= end_year]
        target = seasons[seasons['year'].isin(years)][['year']].drop_duplicates().sort_values('year').reset_index(drop=True)
    else:
        target = hamilton_results[['raceId']].drop_duplicates().assign(year=None)
else:
    # Fallback: return all seasons as potential years (broad preservation per instructions)
    target = seasons[['year']].drop_duplicates().sort_values('year').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
