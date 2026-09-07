import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['age_category_code', 'user_category_code', 'is_buyer', 'is_seller', 'login_name', 'password', 'date_registered', 'middle_name', 'other_user_details'])
    # DropColumn
    table_1 = table_1.drop(columns=['age_category_code', 'user_category_code', 'is_buyer', 'is_seller', 'login_name', 'password', 'date_registered', 'middle_name', 'other_user_details'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['user_id', 'first_name', 'last_name', 'user_address_id'])
    # SelectCol
    _cols = [c for c in ['user_id', 'first_name', 'last_name', 'user_address_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['user_id', 'first_name', 'last_name', 'user_address_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['user_id', 'first_name', 'last_name', 'user_address_id'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['user_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['user_id'], keep='last').reset_index(drop=True)

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
    # Sort(table_name="table_1", by=['address_id'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['address_id'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['address_id', 'country'])
    # SelectCol
    _cols = [c for c in ['address_id', 'country'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_users = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_addresses = prepared_table_2

target = prepared_users.merge(prepared_addresses, left_on='user_address_id', right_on='address_id', how='inner')
answer = target.loc[target['first_name'] == 'Robbie', ['country']]

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
