import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Headphone_ID', 'new_name': 'headphone_id'}, {'old_name': 'Model', 'new_name': 'model'}])
    # Rename
    table_1 = table_1.rename(columns={'Headphone_ID': 'headphone_id', 'Model': 'model'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'headphone_id', 'new_name': 'Headphone_ID'}, {'old_name': 'model', 'new_name': 'Model'}])
    # Rename
    table_1 = table_1.rename(columns={'headphone_id': 'Headphone_ID', 'model': 'Model'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Headphone_ID', 'Model'])
    # SelectCol
    _cols = [c for c in ['Headphone_ID', 'Model'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Headphone_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Headphone_ID'], keep='first').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="Quantity", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Quantity'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Quantity']
    if _dtype == "datetime64":
        table_1['Quantity'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Quantity'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Quantity'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Quantity'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Store_ID", dtype="int")
    # CastType
    _dtype = 'int'
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Headphone_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Headphone_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Headphone_ID']
    if _dtype == "datetime64":
        table_1['Headphone_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Headphone_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Headphone_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Headphone_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Headphone_ID', 'Store_ID', 'Quantity'])
    # SelectCol
    _cols = [c for c in ['Headphone_ID', 'Store_ID', 'Quantity'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Headphone_ID', 'Store_ID', 'Quantity'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Headphone_ID', 'Store_ID', 'Quantity'], how='any').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_headphones = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_inventory = prepared_table_2

# prepared_headphones and prepared_inventory are the synthesized per-table outputs
# Ensure numeric quantity for stock checks
inv = prepared_inventory.copy()
if 'Quantity' in inv.columns:
    inv['Quantity_num'] = pd.to_numeric(inv['Quantity'].astype(str).str.replace('"',''), errors='coerce').fillna(0)
else:
    inv['Quantity_num'] = 0

# Aggregate to know which Headphone_ID has any stock across stores
inv_any_stock = (
    inv.groupby('Headphone_ID', as_index=False)['Quantity_num']
       .sum()
       .rename(columns={'Quantity_num': 'total_qty'})
)

# Left-join headphones to aggregated inventory
merged = prepared_headphones.merge(inv_any_stock, on='Headphone_ID', how='left')

# Models not in stock in any store: total_qty is NaN or 0
result = merged.loc[merged['total_qty'].fillna(0) <= 0, ['Model']].drop_duplicates().reset_index(drop=True)

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
