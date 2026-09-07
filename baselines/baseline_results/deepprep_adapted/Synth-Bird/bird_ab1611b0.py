import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fastestLapTime", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fastestLapTime"] = table_1["fastestLapTime"].apply(_std_apply)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['driverId', 'raceId', 'fastestLapSpeed'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['driverId', 'raceId', 'fastestLapSpeed'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'fastestLapSpeed', 'fastestLapTime', 'raceId'])
    # SelectCol
    _cols = [c for c in ['driverId', 'fastestLapSpeed', 'fastestLapTime', 'raceId'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="nationality", func="""
    # def is_valid_nationality(val):
    #     return val is not None and str(val).strip() != ''
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_nationality(val):
        return val is not None and str(val).strip() != ''
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_nationality(val))
        except Exception:
            return False
    table_1 = table_1[table_1['nationality'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['driverId'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['driverId'], keep='last').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'forename', 'surname', 'nationality'])
    # SelectCol
    _cols = [c for c in ['driverId', 'forename', 'surname', 'nationality'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_results = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_drivers = prepared_table_2

# prepared_results and prepared_drivers are pre-synthesized as per target schemas
merged = prepared_results.merge(prepared_drivers, on='driverId', how='left')
# Identify the driver with the maximum fastestLapSpeed
merged_nonnull = merged.dropna(subset=['fastestLapSpeed'])
# Ensure numeric comparison
merged_nonnull['fastestLapSpeed'] = pd.to_numeric(merged_nonnull['fastestLapSpeed'], errors='coerce')
max_row = merged_nonnull.loc[merged_nonnull['fastestLapSpeed'].idxmax()]
answer = {
    'nationality': max_row['nationality'],
    'driverId': max_row['driverId'],
    'driver_name': f"{max_row.get('forename', '')} {max_row.get('surname', '')}".strip(),
    'fastestLapSpeed': max_row['fastestLapSpeed']
}

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
