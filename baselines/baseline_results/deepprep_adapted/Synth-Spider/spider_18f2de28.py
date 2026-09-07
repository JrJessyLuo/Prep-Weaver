import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Pivot(table_name="table_1", index="StuID", columns="Attribute", values="Value", aggfunc="first")
    # Pivot
    table_1 = table_1.pivot_table(index='StuID', columns='Attribute', values='Value', aggfunc='first').reset_index()

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['StuID', 'Fname', 'Major', 'city_code'])
    # SelectCol
    _cols = [c for c in ['StuID', 'Fname', 'Major', 'city_code'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'city_code', 'new_name': 'City'}])
    # Rename
    table_1 = table_1.rename(columns={'city_code': 'City'})

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
    # StandardizeString(table_name="table_1", column_name="city_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return s.strip().title()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return s.strip().title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["city_name"] = table_1["city_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['city_name'])
    # SelectCol
    _cols = [c for c in ['city_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['city_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['city_name'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_cities = prepared_table_2

target = prepared_students.merge(prepared_cities, left_on='City', right_on='city_name', how='inner')
answer = target[target['city_name'].str.lower() == 'baltimore'][['Fname','Major']]

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
