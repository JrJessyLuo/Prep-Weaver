import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="day", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['day'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['day']
    if _dtype == "datetime64":
        table_1['day'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['day'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['day'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['day'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['income_id', 'link_to_member', 'year', 'month', 'day', 'amount', 'source', 'notes'])
    # SelectCol
    _cols = [c for c in ['income_id', 'link_to_member', 'year', 'month', 'day', 'amount', 'source', 'notes'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="position", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().title()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["position"] = table_1["position"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major'])
    # SelectCol
    _cols = [c for c in ['member_id', 'first_name', 'last_name', 'email', 'position', 't_shirt_size', 'phone', 'zip', 'link_to_major'] if c in table_1.columns]
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
prepared_income = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_members = prepared_table_2

target = prepared_income.merge(prepared_members, left_on='link_to_member', right_on='member_id', how='inner')
# Filter for the specific member name
mask = (target['first_name'].str.strip().str.casefold() == 'casey') & (target['last_name'].str.strip().str.casefold() == 'mason')
ans = target.loc[mask].copy()
# Construct received date as YYYY-MM-DD (zero-pad month/day)
ans['received_date'] = ans['year'].astype(str).str.zfill(4) + '-' + ans['month'].astype(str).str.zfill(2) + '-' + ans['day'].astype(str).str.zfill(2)
# Select evidence columns
answer = ans[['first_name','last_name','received_date','amount','source','income_id']]

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
