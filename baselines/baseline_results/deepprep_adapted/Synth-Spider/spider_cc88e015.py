import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Store_ID", dtype="str")
    # CastType
    _dtype = 'str'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Store_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Store_ID']
    if _dtype == "datetime64":
        table_1['Store_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Store_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Store_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Store_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Store_ID', 'Name'])
    # SelectCol
    _cols = [c for c in ['Store_ID', 'Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Store_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Store_ID'], keep='last').reset_index(drop=True)

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
stores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
store_headphone_stock = prepared_table_2

# Assume prepared tables are dataframes: stores, store_headphone_stock
# Normalize Quantity to numeric (handles quotes) and aggregate per store
inv = store_headphone_stock.copy()
inv['Quantity'] = pd.to_numeric(inv['Quantity'], errors='coerce').fillna(0)
# A store has any headphones if total quantity across headphone SKUs > 0
has_hp = inv.groupby('Store_ID', as_index=False)['Quantity'].sum().rename(columns={'Quantity':'Total_HP_Qty'})

# Left-join stores to headphone availability
merged = stores.merge(has_hp, on='Store_ID', how='left')

# Stores with no headphone rows or zero total quantity
no_hp = merged[(merged['Total_HP_Qty'].isna()) | (merged['Total_HP_Qty'] <= 0)]

# Final answer: store names
answer = no_hp[['Name']].drop_duplicates().sort_values('Name')

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
