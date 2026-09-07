import pandas as pd
import numpy as np

def _prep_1(table_1):
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['link_to_event', 'category', 'spent', 'remaining', 'amount', 'event_status'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['link_to_event', 'category', 'spent', 'remaining', 'amount', 'event_status'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['link_to_event', 'category', 'spent', 'remaining', 'amount', 'event_status'])
    # SelectCol
    _cols = [c for c in ['link_to_event', 'category', 'spent', 'remaining', 'amount', 'event_status'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Count(table_name="table_1")
    # Count -> statistic_table
    _stat_row = pd.DataFrame({'operator': ['Count(table_name="table_1")'], 'statistic_name': ['count'], 'value': [len(table_1)]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['link_to_event', 'link_to_member'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['link_to_event', 'link_to_member'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['link_to_event', 'link_to_member'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['link_to_event', 'link_to_member'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['link_to_event', 'link_to_member'])
    # SelectCol
    _cols = [c for c in ['link_to_event', 'link_to_member'] if c in table_1.columns]
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
    # Stack(table_name="table_1", id_vars=['member_id'], value_vars=[], var_name="attr_id", value_name="attr_value")
    # Stack
    table_1 = table_1.melt(id_vars=['member_id'], value_vars=[], var_name='attr_id', value_name='attr_value')
    table_1 = table_1.dropna(subset=['attr_value'])

    # ---------------- Step 2 ----------------
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

prepared_table_1 = _prep_1(tables['table_5'])
prepared_table_2 = _prep_2(tables['table_4'])
prepared_budget = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_event_members = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_members = prepared_table_4

# prepared_members comes from normalizing table_4's attribute/value layout into tidy columns
# prepared_event_members is table_3 as-is
# prepared_budget is table_2 as-is (selected columns only)

# 1) Find Sacha Harrison's member_id
member_mask = (prepared_members['first_name'].str.strip().str.casefold() == 'sacha') & \
              (prepared_members['last_name'].str.strip().str.casefold() == 'harrison')
sacha = prepared_members.loc[member_mask, ['member_id']]

# 2) Get events Sacha is linked to
sacha_events = prepared_event_members.merge(sacha, left_on='link_to_member', right_on='member_id', how='inner')

# 3) Join to budget lines for those events
sacha_expenses = prepared_budget.merge(sacha_events[['link_to_event']].drop_duplicates(), on='link_to_event', how='inner')

# 4) The question asks for the kinds of expenses => distinct categories (optionally keep evidence amounts)
result = sacha_expenses[['category']].drop_duplicates().sort_values('category').reset_index(drop=True)

# If no rows, result should be empty indicating no expenses found for Sacha's events.
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
