import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # name-based Austrian circuit candidates
    #     nm = str(row.get('name', '')).lower()
    #     return ('austr' in nm) or ('red bull ring' in nm) or ('österreich' in nm) or ('osterreich' in nm)
    # """)
    # Filter
    def filter_func(row):
        # name-based Austrian circuit candidates
        nm = str(row.get('name', '')).lower()
        return ('austr' in nm) or ('red bull ring' in nm) or ('österreich' in nm) or ('osterreich' in nm)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['circuitId', 'circuitRef', 'name', 'location'])
    # SelectCol
    _cols = [c for c in ['circuitId', 'circuitRef', 'name', 'location'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # CastType(table_name="table_1", column="luquId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['luquId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['luquId']
    if _dtype == "datetime64":
        table_1['luquId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['luquId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['luquId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['luquId'] = _series.astype(str)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="time", date_format="%H:%M:%S")
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
    table_1['time'] = table_1['time'].apply(_sd_parse)
    if '%H:%M:%S':
        table_1['time'] = table_1['time'].dt.strftime('%H:%M:%S')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'year', 'round', 'luquId', 'mingcheng', 'date', 'time'])
    # SelectCol
    _cols = [c for c in ['raceId', 'year', 'round', 'luquId', 'mingcheng', 'date', 'time'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['raceId', 'driverId', 'lap', 'time'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['raceId', 'driverId', 'lap', 'time'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'driverId', 'lap', 'time', 'milliseconds'])
    # SelectCol
    _cols = [c for c in ['raceId', 'driverId', 'lap', 'time', 'milliseconds'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="raceId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['raceId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['raceId']
    if _dtype == "datetime64":
        table_1['raceId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['raceId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['raceId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['raceId'] = _series.astype(str)

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
    # CastType(table_name="table_1", column="lap", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['lap'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['lap']
    if _dtype == "datetime64":
        table_1['lap'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['lap'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['lap'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['lap'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="milliseconds", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['milliseconds'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['milliseconds']
    if _dtype == "datetime64":
        table_1['milliseconds'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['milliseconds'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['milliseconds'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['milliseconds'] = _series.astype(str)

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
prepared_circuits = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_races = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_lap_times = prepared_table_3

# Assume prepared_* DataFrames already exist
circuits = prepared_circuits.copy()
races = prepared_races.copy()
laps = prepared_lap_times.copy()

# Join races to circuits to know which races are at Austrian circuit
races_circuits = races.merge(circuits, left_on='luquId', right_on='circuitId', how='inner')

# Filter races that are Austrian GP by race name or by circuit name containing Austria indicators
is_austria_race = races_circuits['mingcheng'].str.contains('Austrian', case=False, na=False) | races_circuits['name'].str.contains('Austria|Austrian|Red Bull Ring|Österreich', case=False, na=False)
races_at_austria = races_circuits.loc[is_austria_race, ['raceId']]

# Join lap times for those races
laps_at_austria = laps.merge(races_at_austria, on='raceId', how='inner')

# Compute absolute lap record (minimum milliseconds)
if len(laps_at_austria) == 0:
    target = pd.DataFrame([], columns=['lap_record_time', 'lap_record_ms'])
else:
    idx = laps_at_austria['milliseconds'].idxmin()
    best_ms = int(laps_at_austria.loc[idx, 'milliseconds'])
    best_time = laps_at_austria.loc[idx, 'time']
    target = pd.DataFrame([{'lap_record_time': best_time, 'lap_record_ms': best_ms}])

target

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
