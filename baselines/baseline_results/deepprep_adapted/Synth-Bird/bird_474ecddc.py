import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="room", mode="mode")
    # MissingValueImputation
    table_1["room"] = table_1["room"].fillna(table_1["room"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['event_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['event_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['event_id', 'event_name', 'building', 'room', 'status'])
    # SelectCol
    _cols = [c for c in ['event_id', 'event_name', 'building', 'room', 'status'] if c in table_1.columns]
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
    # OutlierDetection(table_name="table_1", column_name="remaining", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['remaining'].quantile(0.25)
    _q3 = table_1['remaining'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_remaining_is_outlier'] = table_1['remaining'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_remaining_is_outlier'] == False]
        table_1.drop(columns=['table_1_remaining_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_remaining_is_outlier'] = table_1['table_1_remaining_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="amount", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     # Convert to string and strip whitespace
    #     s = str(s).strip()
    #     # Remove wrapping/double quotes like ""75"" or "75"
    #     s = s.replace('"', '')
    #     # Keep digits, decimal point, and minus sign if present
    #     s = re.sub(r'[^0-9\.-]', '', s)
    #     return s if s != '' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        # Convert to string and strip whitespace
        s = str(s).strip()
        # Remove wrapping/double quotes like ""75"" or "75"
        s = s.replace('"', '')
        # Keep digits, decimal point, and minus sign if present
        s = re.sub(r'[^0-9\.-]', '', s)
        return s if s != '' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["amount"] = table_1["amount"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="amount", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['amount'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['amount']
    if _dtype == "datetime64":
        table_1['amount'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['amount'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['amount'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['amount'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="spent", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['spent'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['spent']
    if _dtype == "datetime64":
        table_1['spent'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['spent'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['spent'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['spent'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="remaining", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['remaining'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['remaining']
    if _dtype == "datetime64":
        table_1['remaining'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['remaining'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['remaining'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['remaining'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['link_to_event', 'spent', 'remaining', 'amount', 'event_status'])
    # SelectCol
    _cols = [c for c in ['link_to_event', 'spent', 'remaining', 'amount', 'event_status'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
prepared_events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_budgets = prepared_table_2

target = prepared_events.merge(prepared_budgets, left_on='event_id', right_on='link_to_event', how='inner')
# underspend means spent < amount; amount is a quoted string, coerce to float
amt = pd.to_numeric(target['amount'].astype(str).str.replace('"',''), errors='coerce')
spent = pd.to_numeric(target['spent'], errors='coerce')
underspend_mask = (spent < amt)
result = target.loc[underspend_mask, ['event_name', 'building', 'room']]
result = result.rename(columns={'building':'location_building', 'room':'location_room'})

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
