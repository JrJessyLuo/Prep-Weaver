import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'guoji', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s.title()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ming', 'new_name': 'givenName'}, {'old_name': 'xing', 'new_name': 'familyName'}, {'old_name': 'guoji', 'new_name': 'nationality'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'driverRef', 'number', 'code', 'givenName', 'familyName', 'dob', 'nationality', 'url']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fastestLapTime', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'fastestLapTime', 'target_columns': ['fastestLapTime_seconds'], 'func': "def transform(s):\n    import math\n    try:\n        s = str(s).strip()\n        if s in (None, '', 'nan', 'NaN'):\n            return [math.nan]\n        # Expect format M:SS.mmm\n        parts = s.split(':')\n        if len(parts) != 2:\n            return [math.nan]\n        minutes = float(parts[0])\n        sec_milli = float(parts[1])\n        total = minutes * 60.0 + sec_milli\n        return [total]\n    except Exception:\n        return [math.nan]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['resultId', 'raceId', 'driverId', 'fastestLapTime', 'fastestLapTime_seconds']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s.title()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['guoji'] = tmp_1['guoji'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'ming': 'givenName', 'xing': 'familyName', 'guoji': 'nationality'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['driverId', 'driverRef', 'number', 'code', 'givenName', 'familyName', 'dob', 'nationality', 'url']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['fastestLapTime'] = tmp_1['fastestLapTime'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import math\n    try:\n        s = str(s).strip()\n        if s in (None, '', 'nan', 'NaN'):\n            return [math.nan]\n        # Expect format M:SS.mmm\n        parts = s.split(':')\n        if len(parts) != 2:\n            return [math.nan]\n        minutes = float(parts[0])\n        sec_milli = float(parts[1])\n        total = minutes * 60.0 + sec_milli\n        return [total]\n    except Exception:\n        return [math.nan]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['fastestLapTime'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['fastestLapTime_seconds'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['resultId', 'raceId', 'driverId', 'fastestLapTime', 'fastestLapTime_seconds']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_11', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='driverId', how='inner')
# Filter French drivers with lap time strictly less than 2 minutes (120 seconds). Handle missing or unparsable times by excluding NaNs.
mask_nationality = integrated['nationality'].str.contains('French', case=False, na=False)
mask_time = (integrated['fastestLapTime_seconds'].notna()) & (integrated['fastestLapTime_seconds'] < 120.0)
filtered = integrated[mask_nationality & mask_time]
# Count unique drivers who achieved such a laptime
count_df = filtered[['driverId']].drop_duplicates()
target = count_df.assign(count=1).agg({'count':'sum'}).to_frame().T

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
