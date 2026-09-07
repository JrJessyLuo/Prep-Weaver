import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Capacity'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Capacity'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="NumberWithQuoteSuffix", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     digits = re.findall(r'\d+', str(s))
    #     return digits[0] if digits else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        digits = re.findall(r'\d+', str(s))
        return digits[0] if digits else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["NumberWithQuoteSuffix"] = table_1["NumberWithQuoteSuffix"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NumberWithQuoteSuffix", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NumberWithQuoteSuffix'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NumberWithQuoteSuffix']
    if _dtype == "datetime64":
        table_1['NumberWithQuoteSuffix'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NumberWithQuoteSuffix'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NumberWithQuoteSuffix'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NumberWithQuoteSuffix'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'NumberWithQuoteSuffix', 'new_name': 'wh'}, {'old_name': 'Capacity', 'new_name': 'capacity'}])
    # Rename
    table_1 = table_1.rename(columns={'NumberWithQuoteSuffix': 'wh', 'Capacity': 'capacity'})

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="capacity", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['capacity'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['capacity']
    if _dtype == "datetime64":
        table_1['capacity'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['capacity'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['capacity'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['capacity'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['wh'], agg=[{'column': 'capacity', 'agg_func': 'max'}])
    # GroupBy
    table_1 = table_1.groupby(['wh'], as_index=False).agg({'capacity': 'max'})

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['wh', 'capacity'])
    # SelectCol
    _cols = [c for c in ['wh', 'capacity'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
    # Deduplicate(table_name="table_1", subset=['Code'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Code'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Code', 'wh'])
    # SelectCol
    _cols = [c for c in ['Code', 'wh'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="wh", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['wh'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['wh']
    if _dtype == "datetime64":
        table_1['wh'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['wh'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['wh'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['wh'] = _series.astype(str)

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
prepared_warehouses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_inventory = prepared_table_2

tmp = prepared_inventory.merge(prepared_warehouses, on='wh', how='inner')
# Count items per warehouse
counts = tmp.groupby('wh', as_index=False).size().rename(columns={'size':'current_load'})
# Join back to capacities
with_cap = counts.merge(prepared_warehouses, on='wh', how='left')
# Select warehouses above capacity and return their item Codes
over = with_cap[with_cap['current_load'] > with_cap['capacity']]
result = tmp.merge(over[['wh']], on='wh', how='inner')[['Code']].drop_duplicates()
answer = result['Code'].tolist()

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
