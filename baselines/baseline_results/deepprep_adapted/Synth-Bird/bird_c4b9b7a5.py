import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="category", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["category"] = table_1["category"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['budget_id', 'category'])
    # SelectCol
    _cols = [c for c in ['budget_id', 'category'] if c in table_1.columns]
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
    # DropNulls(table_name="table_1", subset=['expense_id', 'expense_date', 'cost'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['expense_id', 'expense_date', 'cost'], how='any').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="approved", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["approved"] = table_1["approved"].apply(_std_apply)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # keep only approved September expenses
    #     if row.get('approved') != 'true':
    #         return False
    #     dt = pd.to_datetime(row.get('expense_date'), errors='coerce')
    #     if pd.isna(dt):
    #         return False
    #     return dt.month == 9
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # keep only approved September expenses
        if row.get('approved') != 'true':
            return False
        dt = pd.to_datetime(row.get('expense_date'), errors='coerce')
        if pd.isna(dt):
            return False
        return dt.month == 9
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'link_to_member', 'link_to_budget'])
    # SelectCol
    _cols = [c for c in ['expense_id', 'expense_description', 'expense_date', 'cost', 'approved', 'link_to_member', 'link_to_budget'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="last_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["last_name"] = table_1["last_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="first_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["first_name"] = table_1["first_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="position", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["position"] = table_1["position"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'first_name', 'last_name', 'position'])
    # SelectCol
    _cols = [c for c in ['member_id', 'first_name', 'last_name', 'position'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="link_to_member", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["link_to_member"] = table_1["link_to_member"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="link_to_event", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["link_to_event"] = table_1["link_to_event"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['link_to_event', 'link_to_member'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['link_to_event', 'link_to_member'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['link_to_event', 'link_to_member'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['link_to_event', 'link_to_member'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['link_to_event', 'link_to_member'])
    # SelectCol
    _cols = [c for c in ['link_to_event', 'link_to_member'] if c in table_1.columns]
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
prepared_budget = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_expense = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_member = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
prepared_event_membership = prepared_table_4

# Assume prepared_budget, prepared_expense, prepared_member are dataframes synthesized per targets
exp_bud = prepared_expense.merge(prepared_budget, left_on='link_to_budget', right_on='budget_id', how='inner')
exp_bud_mem = exp_bud.merge(prepared_member, left_on='link_to_member', right_on='member_id', how='inner')

# Filter: approved expenses by Student_Club members with category Food in September
exp_bud_mem['expense_date'] = pd.to_datetime(exp_bud_mem['expense_date'], errors='coerce')
mask = (
    exp_bud_mem['approved'].astype(str).str.lower() == 'true'
) & (
    exp_bud_mem['category'].str.strip().str.lower() == 'food'
) & (
    (exp_bud_mem['expense_date'].dt.month == 9)
)

september_food_spend = exp_bud_mem.loc[mask, 'cost'].astype(float).sum()

answer = september_food_spend

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
