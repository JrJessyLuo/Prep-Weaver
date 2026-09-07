import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['expense_id', 'expense_date', 'cost', 'items', 'link_to_budget'])
    # SelectCol
    _cols = [c for c in ['expense_id', 'expense_date', 'cost', 'items', 'link_to_budget'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # Deduplicate(table_name="table_1", subset=['budget_id_prefix', 'budget_id_suffix', 'link_to_event'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['budget_id_prefix', 'budget_id_suffix', 'link_to_event'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['budget_id_prefix', 'budget_id_suffix', 'link_to_event'])
    # SelectCol
    _cols = [c for c in ['budget_id_prefix', 'budget_id_suffix', 'link_to_event'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_expenses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_budgets = prepared_table_2

# prepared_expenses and prepared_budgets are assumed to be synthesized from table_1 and table_2 per targets

# Construct full budget_id on the budgets table to match link_to_budget
prepared_budgets = prepared_budgets.copy()
prepared_budgets['budget_id'] = prepared_budgets['budget_id_prefix'].astype(str) + prepared_budgets['budget_id_suffix'].astype(str)

# Join expenses to budgets via budget_id
merged = prepared_expenses.merge(prepared_budgets[['budget_id', 'link_to_event']], left_on='link_to_budget', right_on='budget_id', how='inner')

# Filter for pizza expenses with cost between 50 and 100 (exclusive of 100 per phrasing "less than a hundred")
mask_pizza = merged['items'].str.contains('pizza', case=False, na=False)
mask_cost = (merged['cost'] > 50) & (merged['cost'] < 100)
filtered = merged[mask_pizza & mask_cost]

# Select required output columns: event name (if available) and date. If event names require another table, fallback to event ID.
# Here we only have link_to_event; return that as event identifier along with expense_date.
result = filtered[['link_to_event', 'expense_date']].drop_duplicates().rename(columns={'link_to_event': 'event_id', 'expense_date': 'date'})

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
