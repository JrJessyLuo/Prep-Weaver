import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['nationality']).strip() == 'Japanese'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['nationality']).strip() == 'Japanese'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'nationality', 'forename', 'surname'])
    # SelectCol
    _cols = [c for c in ['driverId', 'nationality', 'forename', 'surname'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     y = row['year']
    #     return pd.notnull(y) and 2007 <= int(y) <= 2009
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        y = row['year']
        return pd.notnull(y) and 2007 <= int(y) <= 2009
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'year'])
    # SelectCol
    _cols = [c for c in ['raceId', 'year'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['raceId', 'year'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['raceId', 'year'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
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
    # CastType(table_name="table_1", column="statusId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['statusId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['statusId']
    if _dtype == "datetime64":
        table_1['statusId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['statusId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['statusId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['statusId'] = _series.astype(str)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'driverId', 'statusId'])
    # SelectCol
    _cols = [c for c in ['raceId', 'driverId', 'statusId'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['statusId'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['statusId'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['statusId', 'status'])
    # SelectCol
    _cols = [c for c in ['statusId', 'status'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
drivers_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
races_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
results_prepared = prepared_table_3
prepared_table_4 = _prep_4(tables['table_13'])
status_prepared = prepared_table_4

# Assume prepared tables are DataFrames: drivers_prepared, races_prepared, results_prepared, status_prepared
# 1) Integrate
res_dr = results_prepared.merge(drivers_prepared, on='driverId', how='inner')
res_dr_ra = res_dr.merge(races_prepared, on='raceId', how='inner')
full = res_dr_ra.merge(status_prepared, on='statusId', how='left')

# 2) Filter Japanese drivers and years 2007-2009
mask = (full['nationality'].str.lower() == 'japanese') & (full['year'].between(2007, 2009))
sub = full.loc[mask].copy()

# 3) Define completion: status == 'Finished' (exact match)
sub['finished'] = (sub['status'] == 'Finished')

# 4) Compute completion percentage overall across 2007-2009 for Japanese drivers
#    If per-driver breakdown desired, groupby(['driverId','forename','surname']). Here we compute overall percentage.
total_starts = len(sub)
finished_starts = sub['finished'].sum()
completion_percentage = float(finished_starts) / total_starts * 100 if total_starts > 0 else float('nan')

answer = {
    'total_starts_2007_2009_japanese': int(total_starts),
    'finished_starts': int(finished_starts),
    'completion_percentage': completion_percentage
}

target = pd.DataFrame([answer])

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
