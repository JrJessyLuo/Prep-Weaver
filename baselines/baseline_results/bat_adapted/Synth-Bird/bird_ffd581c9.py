import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['driverId','guoji']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['driverId', 'fastestLapTime']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_11'])
prepared_results = prepared_table_2

# Merge prepared tables on driverId
merged = prepared_results.merge(prepared_drivers, on='driverId', how='inner')

# Keep only French drivers (exact match as stored in drivers.guoji)
fr = merged[merged['guoji'].str.strip().str.lower() == 'french']

# Parse fastestLapTime like 'M:SS.mmm' into total seconds
# Drop rows with missing/invalid times
valid = fr['fastestLapTime'].dropna().astype(str)

# Function to parse 'M:SS.mmm' -> seconds (float)
def parse_lap(s):
    s = s.strip()
    if not s or s.lower() in {'nan', 'none'}:
        return pd.NA
    # Expect format M:SS.mmm (e.g., '1:27.452')
    parts = s.split(':')
    if len(parts) != 2:
        return pd.NA
    try:
        mins = int(parts[0])
        secs = float(parts[1])
        return mins * 60 + secs
    except Exception:
        return pd.NA

secs = valid.map(parse_lap)
fr = fr.loc[valid.index].assign(_lap_seconds=secs)
fr = fr.dropna(subset=['_lap_seconds'])

# Threshold 02:00.00 => 120.0 seconds
answer = (fr['_lap_seconds'] < 120.0).sum()

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
