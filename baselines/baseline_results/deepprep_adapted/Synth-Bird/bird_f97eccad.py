import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['code', 'dob'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['code', 'dob'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="dob", date_format="%Y-%m-%d")
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
    table_1['dob'] = table_1['dob'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['dob'] = table_1['dob'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="code", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding double quotes if present
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding double quotes if present
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["code"] = table_1["code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     dob = row.get('dob', None)
    #     if dob is None or (isinstance(dob, float) and pd.isna(dob)) or pd.isna(dob):
    #         return False
    #     # dob is standardized as YYYY-MM-DD string
    #     return str(dob)[:4] == \"1971\"
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        dob = row.get('dob', None)
        if dob is None or (isinstance(dob, float) and pd.isna(dob)) or pd.isna(dob):
            return False
        # dob is standardized as YYYY-MM-DD string
        return str(dob)[:4] == \"1971\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'code', 'dob'])
    # SelectCol
    _cols = [c for c in ['driverId', 'code', 'dob'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['raceId', 'driverId', 'milliseconds'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['raceId', 'driverId', 'milliseconds'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'driverId', 'milliseconds'])
    # SelectCol
    _cols = [c for c in ['raceId', 'driverId', 'milliseconds'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_8'])
prepared_lap_times = prepared_table_2

# Inputs: prepared_drivers, prepared_lap_times
# 1) Filter drivers born in 1971
born_1971 = prepared_drivers[prepared_drivers['dob'].str.startswith('1971')][['driverId','code']]

# 2) For each race, find the global fastest lap time
race_min = prepared_lap_times.groupby('raceId', as_index=False)['milliseconds'].min().rename(columns={'milliseconds':'race_fastest_ms'})

# 3) For each driver in each race, find their personal fastest lap time
driver_race_min = prepared_lap_times.groupby(['raceId','driverId'], as_index=False)['milliseconds'].min().rename(columns={'milliseconds':'driver_fastest_ms'})

# 4) Identify driver-race pairs where the driver set the fastest lap of that race
with_race_fastest = driver_race_min.merge(race_min, on='raceId', how='inner')
fastest_pairs = with_race_fastest[with_race_fastest['driver_fastest_ms'] == with_race_fastest['race_fastest_ms']]

# 5) Keep only drivers born in 1971
result = fastest_pairs.merge(born_1971, on='driverId', how='inner')

# 6) Select required output columns (unique drivers who achieved a race fastest lap and were born in 1971)
answer = result[['driverId','code']].drop_duplicates().sort_values(['driverId','code']).reset_index(drop=True)

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
