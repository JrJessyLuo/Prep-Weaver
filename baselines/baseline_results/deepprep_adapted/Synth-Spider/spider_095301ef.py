import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Conference_ID', 'Conference_Name', 'Year'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Conference_ID', 'Conference_Name', 'Year'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Conference_ID', 'Conference_Name', 'Year'])
    # SelectCol
    _cols = [c for c in ['Conference_ID', 'Conference_Name', 'Year'] if c in table_1.columns]
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
    # ErrorDetection(table_name="table_1", column_name="r", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['r'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="r", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     x = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(x) >= 2) and ((x[0] == x[-1]) and x[0] in ["'", '"']):
    #         x = x[1:-1].strip()
    #     # collapse multiple spaces
    #     x = re.sub(r'\s+', ' ', x)
    #     return x
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        x = str(s).strip()
        # remove surrounding single/double quotes if present
        if (len(x) >= 2) and ((x[0] == x[-1]) and x[0] in ["'", '"']):
            x = x[1:-1].strip()
        # collapse multiple spaces
        x = re.sub(r'\s+', ' ', x)
        return x
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["r"] = table_1["r"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="conf_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['conf_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['conf_id']
    if _dtype == "datetime64":
        table_1['conf_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['conf_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['conf_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['conf_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="staff_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['staff_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['staff_ID']
    if _dtype == "datetime64":
        table_1['staff_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['staff_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['staff_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['staff_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['conf_id', 'staff_ID', 'r'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['conf_id', 'staff_ID', 'r'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['conf_id', 'staff_ID', 'r'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['conf_id', 'staff_ID', 'r'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['conf_id', 'staff_ID', 'r'])
    # SelectCol
    _cols = [c for c in ['conf_id', 'staff_ID', 'r'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
prepared_conferences = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_participation = prepared_table_2

target = prepared_conferences.merge(prepared_participation, left_on='Conference_ID', right_on='conf_id', how='left')
result = target.groupby(['Conference_Name','Year'], as_index=False)['staff_ID'].nunique().rename(columns={'staff_ID':'num_participants'})
result = result[['Conference_Name','Year','num_participants']]

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
