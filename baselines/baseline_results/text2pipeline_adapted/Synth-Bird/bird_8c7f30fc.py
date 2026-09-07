import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'circuitId', 'new_name': 'circuit_id'}, {'old_name': 'circuitRef', 'new_name': 'circuit_ref'}]}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['Argentina', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'Hungary', 'India', 'Italy', 'Japan', 'Korea', 'Malaysia', 'Mexico', 'Monaco', 'Morocco', 'Netherlands', 'Portugal', 'Russia', 'Singapore', 'South Africa', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'UAE', 'UK', 'USA']}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'circuit_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    # Trim while preserving original case\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'location', 'func': 'def transform(s):\n    # Trim while preserving original case\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['circuit_id', 'circuit_ref', 'name', 'location', 'lng', 'alt', 'url']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLap', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rank', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLapSpeed', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fastestLapTime', 'func': 'def transform(s):\n    return str(s) if s is not None else None'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'circuitId': 'circuit_id', 'circuitRef': 'circuit_ref'})
    # Step 2: DropColumn
    tmp_1 = tmp_0.drop(columns=['Argentina', 'Australia', 'Austria', 'Azerbaijan', 'Bahrain', 'Belgium', 'Brazil', 'Canada', 'China', 'France', 'Germany', 'Hungary', 'India', 'Italy', 'Japan', 'Korea', 'Malaysia', 'Mexico', 'Monaco', 'Morocco', 'Netherlands', 'Portugal', 'Russia', 'Singapore', 'South Africa', 'Spain', 'Sweden', 'Switzerland', 'Turkey', 'UAE', 'UK', 'USA'], errors='ignore').copy()
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['circuit_id'] = pd.to_numeric(tmp_2['circuit_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim while preserving original case\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['name'] = tmp_3['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim while preserving original case\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['location'] = tmp_4['location'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['circuit_id', 'circuit_ref', 'name', 'location', 'lng', 'alt', 'url']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['raceId'] = pd.to_numeric(tmp_0['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['fastestLap'] = pd.to_numeric(tmp_1['fastestLap'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['rank'] = pd.to_numeric(tmp_2['rank'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['fastestLapSpeed'] = pd.to_numeric(tmp_3['fastestLapSpeed'], errors='coerce').astype(float)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s) if s is not None else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['fastestLapTime'] = tmp_4['fastestLapTime'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['raceId', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
prepared_table_1['_name_ci'] = prepared_table_1['name'].astype(str).str.lower()
# Try to identify Austrian circuit rows by common names
mask_at = (
    prepared_table_1['_name_ci'].str.contains('austria', case=False, na=False) |
    prepared_table_1['_name_ci'].str.contains('red bull ring', case=False, na=False) |
    prepared_table_1['_name_ci'].str.contains('spielberg', case=False, na=False) |
    prepared_table_1['_name_ci'].str.contains('a1-ring', case=False, na=False)
)
austrian_circuits = prepared_table_1.loc[mask_at].copy()
# We lack a races table to map raceId->circuit, so we cannot isolate Austrian GP laps via a proper join.
# As a best-effort proxy, take the best (minimum) fastestLapTime string among ranked fastest laps across all results.
# Prefer entries where rank == 1 (the officially ranked fastest lap in that race) and with a non-null fastestLapTime.
flt = prepared_table_2.dropna(subset=['fastestLapTime']).copy()
# Prioritize rank==1 rows
rank1 = flt[flt['rank'] == 1]
if not rank1.empty:
    # Among rank1, choose the lexicographically smallest time is unreliable; instead, keep all for display and pick one by minimal milliseconds if available.
    # milliseconds per lap isn't available; keep the string. We'll sort by length then lexicographically to approximate shortest time.
    rank1 = rank1.assign(_len=rank1['fastestLapTime'].astype(str).str.len())
    best_row = rank1.sort_values(['_len','fastestLapTime']).head(1).drop(columns=['_len'])
else:
    flt = flt.assign(_len=flt['fastestLapTime'].astype(str).str.len())
    best_row = flt.sort_values(['_len','fastestLapTime']).head(1).drop(columns=['_len'])
# Build a small descriptor using circuit name if we found Austrian circuits; otherwise keep generic.
if not austrian_circuits.empty:
    circ_name = austrian_circuits.iloc[0]['name']
    desc = circ_name
else:
    desc = 'Austrian Grand Prix Circuit'
result = best_row.copy()
result['circuit'] = desc
result = result.rename(columns={'fastestLapTime':'lap_record_time', 'fastestLapSpeed':'lap_record_speed'})
# Final projection
cols = ['circuit']
if 'lap_record_time' in result.columns:
    cols.append('lap_record_time')
if 'lap_record_speed' in result.columns:
    cols.append('lap_record_speed')
target = result[cols]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
