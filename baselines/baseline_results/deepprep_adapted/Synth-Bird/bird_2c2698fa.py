import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['driverId', 'attribute'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['driverId', 'attribute'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'attribute', 'value'])
    # SelectCol
    _cols = [c for c in ['driverId', 'attribute', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace and lowercase attribute keys
    #     s = re.sub(r'\s+', ' ', s)
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        # normalize internal whitespace and lowercase attribute keys
        s = re.sub(r'\s+', ' ', s)
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute"] = table_1["attribute"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="driverId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['driverId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['driverId']
    if _dtype == "datetime64":
        table_1['driverId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['driverId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['driverId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['driverId'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['driverId', 'attribute', 'value'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['driverId', 'attribute', 'value'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['resultId', 'raceId', 'driverId'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['resultId', 'raceId', 'driverId'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['resultId', 'raceId', 'driverId', 'position', 'positionText', 'positionOrder', 'fastestLap', 'fastestLapTime', 'fastestLapSpeed'])
    # SelectCol
    _cols = [c for c in ['resultId', 'raceId', 'driverId', 'position', 'positionText', 'positionOrder', 'fastestLap', 'fastestLapTime', 'fastestLapSpeed'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="positionText", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["positionText"] = table_1["positionText"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fastestLapTime", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fastestLapTime"] = table_1["fastestLapTime"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fastestLapSpeed", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fastestLapSpeed"] = table_1["fastestLapSpeed"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="position", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['position'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['position']
    if _dtype == "datetime64":
        table_1['position'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['position'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['position'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['position'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="positionOrder", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['positionOrder'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['positionOrder']
    if _dtype == "datetime64":
        table_1['positionOrder'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['positionOrder'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['positionOrder'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['positionOrder'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="fastestLap", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['fastestLap'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['fastestLap']
    if _dtype == "datetime64":
        table_1['fastestLap'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['fastestLap'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['fastestLap'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['fastestLap'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="fastestLapSpeed", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['fastestLapSpeed'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['fastestLapSpeed']
    if _dtype == "datetime64":
        table_1['fastestLapSpeed'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['fastestLapSpeed'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['fastestLapSpeed'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['fastestLapSpeed'] = _series.astype(str)

    # ---------------- Step 10 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['round', 'time', 'url'])
    # DropColumn
    table_1 = table_1.drop(columns=['round', 'time', 'url'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="round", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     return None
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["round"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'circuitId', 'name', 'year', 'round', 'date'])
    # SelectCol
    _cols = [c for c in ['raceId', 'circuitId', 'name', 'year', 'round', 'date'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['circuitId', 'name', 'location', 'country'])
    # SelectCol
    _cols = [c for c in ['circuitId', 'name', 'location', 'country'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name"] = table_1["name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="location", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["location"] = table_1["location"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="country", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["country"] = table_1["country"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['circuitId'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['circuitId'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['circuitId', 'name', 'location', 'country'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['circuitId', 'name', 'location', 'country'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
drivers_kv = prepared_table_1
prepared_table_2 = _prep_2(tables['table_11'])
results = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
races = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
circuits = prepared_table_4

# 1) Identify Lewis Hamilton's driverId from drivers_kv
hamilton_ids = drivers_kv[drivers_kv['attribute'].str.lower().eq('surname') & drivers_kv['value'].str.lower().eq('hamilton')]['driverId'].unique()
# Also allow matching by url or full name if present
hamilton_ids = pd.Index(hamilton_ids).union(drivers_kv[(drivers_kv['attribute'].str.lower().eq('url')) & (drivers_kv['value'].str.contains('Lewis_Hamilton', case=False, na=False))]['driverId'].unique())

# 2) Filter results to Hamilton's rows that have a recorded fastest lap time
ham_results = results[results['driverId'].isin(hamilton_ids) & results['fastestLapTime'].notna()]

# 3) Determine the fastest lap across all his races (minimum fastestLapTime). Convert lap time to timedeltas when possible
# Handle formats like 'M:SS.mmm'
def parse_lap(t):
    if pd.isna(t):
        return pd.NaT
    # expected like '1:27.452' -> minutes:seconds.milliseconds
    try:
        mins, sec_ms = t.split(':')
        secs = float(sec_ms)
        return pd.to_timedelta(int(mins), unit='m') + pd.to_timedelta(secs, unit='s')
    except Exception:
        return pd.NaT

parsed = ham_results['fastestLapTime'].apply(parse_lap)
ham_results = ham_results.assign(fastest_td=parsed)
# Drop rows without parsable time and pick the minimum
ham_results = ham_results[ham_results['fastest_td'].notna()]
if ham_results.empty:
    target = pd.DataFrame({'answer': [None]})
else:
    fastest_row = ham_results.loc[ham_results['fastest_td'].idxmin()]

    # 4) Join to races and circuits to get the circuit of that race
    fastest_df = pd.DataFrame([fastest_row])
    fastest_df = fastest_df.merge(races[['raceId','circuitId','name','year','round','date']], on='raceId', how='left')
    fastest_df = fastest_df.merge(circuits[['circuitId','name','location','country']].rename(columns={'name':'circuit_name'}), on='circuitId', how='left')

    # 5) The question: "What was the position of the circuits during Lewis Hamilton's fastest lap in a Formula_1 race?"
    # Interpret as the race finishing position associated with Hamilton's fastest lap race.
    # Use 'positionText' if present; else fall back to numeric 'position' or 'positionOrder'.
    pos = fastest_df['positionText'].iloc[0]
    if pd.isna(pos) or pos == '':
        pos = fastest_df['position'].iloc[0]
        if pd.isna(pos):
            pos = fastest_df['positionOrder'].iloc[0]

    target = pd.DataFrame({
        'circuit': [fastest_df['circuit_name'].iloc[0]],
        'race': [fastest_df['name'].iloc[0]],
        'year': [fastest_df['year'].iloc[0]],
        'fastest_lap_time': [fastest_df['fastestLapTime'].iloc[0]],
        'position_at_race_finish': [pos]
    })

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
