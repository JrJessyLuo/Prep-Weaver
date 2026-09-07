import pandas as pd
import numpy as np

def _prep_1(table_1):
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
    # SelectCol(table_name="table_1", columns=['owner_user_id', 'property_id'])
    # SelectCol
    _cols = [c for c in ['owner_user_id', 'property_id'] if c in table_1.columns]
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
    # MissingValueImputation(table_name="table_1", column_name="first_name", mode="mode")
    # MissingValueImputation
    table_1["first_name"] = table_1["first_name"].fillna(table_1["first_name"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['user_id', 'first_name'])
    # SelectCol
    _cols = [c for c in ['user_id', 'first_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['user_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['user_id'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_properties = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_users = prepared_table_2

props_per_owner = prepared_properties.groupby('owner_user_id', as_index=False).agg(property_count=('property_id','count'))
max_count = props_per_owner['property_count'].max()
top_owners = props_per_owner[props_per_owner['property_count'] == max_count]
joined = top_owners.merge(prepared_users, left_on='owner_user_id', right_on='user_id', how='left')
# If multiple owners tie, choose one deterministically (e.g., smallest user_id)
joined = joined.sort_values('user_id').head(1)
answer = joined['first_name'].iloc[0]

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
