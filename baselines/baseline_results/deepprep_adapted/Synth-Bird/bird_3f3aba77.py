import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['position'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['position'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'position'])
    # SelectCol
    _cols = [c for c in ['member_id', 'position'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['member_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['member_id'], keep='first').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['income_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['income_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date_received", date_format="%Y-%m-%d")
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
    table_1['date_received'] = table_1['date_received'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date_received'] = table_1['date_received'].dt.strftime('%Y-%m-%d')

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
    # DropNulls(table_name="table_1", subset=['link_to_member'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['link_to_member'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['link_to_member', 'amount', 'source', 'date_received'])
    # SelectCol
    _cols = [c for c in ['link_to_member', 'amount', 'source', 'date_received'] if c in table_1.columns]
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
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_payments = prepared_table_2

target = prepared_payments.merge(prepared_members, left_on='link_to_member', right_on='member_id', how='inner')
# Filter to students in a position other than 'Member'. Assuming 'Member' denotes the member role; include all others
target_non_members = target[target['position'].str.lower() != 'member']
# Compute the average amount paid by these students
result = target_non_members['amount'].astype(float).mean()
answer = result

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
