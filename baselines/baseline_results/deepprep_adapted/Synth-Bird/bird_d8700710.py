import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="event_date", date_format="%Y-%m-%dT%H:%M:%S")
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
    table_1['event_date'] = table_1['event_date'].apply(_sd_parse)
    if '%Y-%m-%dT%H:%M:%S':
        table_1['event_date'] = table_1['event_date'].dt.strftime('%Y-%m-%dT%H:%M:%S')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['event_id', 'event_date'])
    # SelectCol
    _cols = [c for c in ['event_id', 'event_date'] if c in table_1.columns]
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
    # MissingValueImputation(table_name="table_1", column_name="cost", mode="median")
    # MissingValueImputation
    table_1["cost"] = table_1["cost"].fillna(table_1["cost"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="expense_date", date_format="%Y-%m-%d")
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
    table_1['expense_date'] = table_1['expense_date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['expense_date'] = table_1['expense_date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="cost", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['cost'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['cost']
    if _dtype == "datetime64":
        table_1['cost'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['cost'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['cost'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['cost'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['expense_id', 'expense_date', 'cost', 'link_to_budget'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['expense_id', 'expense_date', 'cost', 'link_to_budget'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['expense_id', 'expense_date', 'cost', 'link_to_budget'])
    # SelectCol
    _cols = [c for c in ['expense_id', 'expense_date', 'cost', 'link_to_budget'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['budget_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['budget_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['budget_id', 'link_to_event'])
    # SelectCol
    _cols = [c for c in ['budget_id', 'link_to_event'] if c in table_1.columns]
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
prepared_events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_expenses = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_budgets = prepared_table_3

# Start from prepared tables
exp = prepared_expenses.copy()
bud = prepared_budgets.copy()
ev = prepared_events.copy()

# Join expenses -> budgets -> events
eb = exp.merge(bud, left_on='link_to_budget', right_on='budget_id', how='inner')
ebe = eb.merge(ev, left_on='link_to_event', right_on='event_id', how='inner')

# Derive event year and ensure numeric cost
ebe['event_year'] = pd.to_datetime(ebe['event_date'], errors='coerce').dt.year
ebe['cost'] = pd.to_numeric(ebe['cost'], errors='coerce')

# Sum by year for 2019 and 2020
totals = ebe.groupby('event_year', dropna=True)['cost'].sum()
spent_2019 = float(totals.get(2019, 0.0))
spent_2020 = float(totals.get(2020, 0.0))

# Difference (2019 total minus 2020 total as phrased)
answer = spent_2019 - spent_2020

result = pd.DataFrame({
    'year_2019_total': [spent_2019],
    'year_2020_total': [spent_2020],
    'difference_2019_minus_2020': [answer]
})

target = result

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
