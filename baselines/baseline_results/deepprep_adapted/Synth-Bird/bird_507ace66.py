import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['raceId', 'attribute', 'value'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['raceId', 'attribute', 'value'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute"] = table_1["attribute"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="value", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["value"] = table_1["value"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'attribute', 'value'])
    # SelectCol
    _cols = [c for c in ['raceId', 'attribute', 'value'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['raceId', 'driverId', 'statusId', 'positionText'])
    # SelectCol
    _cols = [c for c in ['raceId', 'driverId', 'statusId', 'positionText'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['raceId', 'driverId'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['raceId', 'driverId'], keep='last').reset_index(drop=True)

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
    # ErrorDetection(table_name="table_1", column_name="status", func="""
    # def is_valid_status(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip().strip('"').strip("'")
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_status(val):
        if val is None:
            return False
        s = str(val).strip().strip('"').strip("'")
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_status(val))
        except Exception:
            return False
    table_1 = table_1[table_1['status'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="status", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     # trim whitespace and remove surrounding single/double quotes if present
    #     x = str(s).strip()
    #     x = re.sub(r'^(["\'])(.*)\1$', r'\2', x)  # removes matching surrounding quotes
    #     x = x.strip()
    #     return x if x != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        # trim whitespace and remove surrounding single/double quotes if present
        x = str(s).strip()
        x = re.sub(r'^(["\'])(.*)\1$', r'\2', x)  # removes matching surrounding quotes
        x = x.strip()
        return x if x != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["status"] = table_1["status"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['statusId', 'status'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['statusId', 'status'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['statusId'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['statusId'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['statusId', 'status'])
    # SelectCol
    _cols = [c for c in ['statusId', 'status'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
races_long = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
results = prepared_table_2
prepared_table_3 = _prep_3(tables['table_13'])
status_lu = prepared_table_3

# Assume prepared tables are provided as DataFrames: races_long, results, status_lu
# 1) Identify raceId for the Bahrain Grand Prix in 2007.
# Filter for year==2007
races_2007 = races_long[(races_long['attribute'] == 'year') & (races_long['value'].astype(str) == '2007')][['raceId']].drop_duplicates()
# Join to find name == 'Bahrain Grand Prix' (attribute could be 'name')
race_names = races_long[races_long['attribute'].str.lower().eq('name')][['raceId','value']].rename(columns={'value':'race_name'})
races_2007_named = races_2007.merge(race_names, on='raceId', how='left')
# Select Bahrain GP
bahrain_2007 = races_2007_named[races_2007_named['race_name'].str.lower() == 'bahrain grand prix']

# Safety: if multiple, take unique raceIds
race_ids = bahrain_2007['raceId'].dropna().unique()

# 2) Get results for those raceIds
res = results[results['raceId'].isin(race_ids)].copy()

# 3) Map status to determine non-finishers
res = res.merge(status_lu, on='statusId', how='left')
# Define non-finish: status not equal to 'Finished' (case-insensitive)
non_finish = res[res['status'].str.lower() != 'finished']

# 4) Count distinct drivers who did not finish
answer = int(non_finish['driverId'].nunique())

result = {'answer': answer}

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
