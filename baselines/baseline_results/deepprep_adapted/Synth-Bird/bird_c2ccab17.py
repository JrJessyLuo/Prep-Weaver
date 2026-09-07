import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['CustomerID_Segment'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['CustomerID_Segment'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="CustomerID_Segment", target_columns=['CustomerID', 'Segment'], func="""
    # import re
    # def split(val):
    #     s = str(val).strip()
    #     # expected pattern like "38144-KAM"
    #     m = re.match(r'^\s*(\d+)\s*[-_\s]+\s*([A-Za-z]+)\s*$', s)
    #     if m:
    #         return {"CustomerID": m.group(1), "Segment": m.group(2)}
    #     # fallback: split on first hyphen if present
    #     if '-' in s:
    #         left, right = s.split('-', 1)
    #         return {"CustomerID": left.strip(), "Segment": right.strip()}
    #     return {"CustomerID": None, "Segment": None}
    # """)
    # SplitColumn
    def split(val):
        s = str(val).strip()
        # expected pattern like "38144-KAM"
        m = re.match(r'^\s*(\d+)\s*[-_\s]+\s*([A-Za-z]+)\s*$', s)
        if m:
            return {"CustomerID": m.group(1), "Segment": m.group(2)}
        # fallback: split on first hyphen if present
        if '-' in s:
            left, right = s.split('-', 1)
            return {"CustomerID": left.strip(), "Segment": right.strip()}
        return {"CustomerID": None, "Segment": None}
    for _c in ['CustomerID', 'Segment']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['CustomerID_Segment']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['CustomerID', 'Segment']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['CustomerID_Segment'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CustomerID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CustomerID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CustomerID']
    if _dtype == "datetime64":
        table_1['CustomerID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CustomerID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CustomerID', 'Segment', 'Currency', 'CustomerID_Segment'])
    # SelectCol
    _cols = [c for c in ['CustomerID', 'Segment', 'Currency', 'CustomerID_Segment'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CustomerID', 'Consumption', 'Year', 'Month'])
    # SelectCol
    _cols = [c for c in ['CustomerID', 'Consumption', 'Year', 'Month'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
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
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_consumption = prepared_table_2

# prepared_clients: split composite key
clients = prepared_clients.copy()
# Ensure types
clients['CustomerID'] = pd.to_numeric(clients['CustomerID'], errors='coerce')

# prepared_consumption: ensure types and filter September 2013
cons = prepared_consumption.copy()
cons['CustomerID'] = pd.to_numeric(cons['CustomerID'], errors='coerce')
cons['Year'] = cons['Year'].astype(str)
cons['Month'] = cons['Month'].astype(str).str.zfill(2)

# Join on CustomerID to attach Segment
joined = cons.merge(clients[['CustomerID', 'Segment', 'Currency', 'CustomerID_Segment']], on='CustomerID', how='inner')

# Filter to September 2013
sept13 = joined[(joined['Year'] == '2013') & (joined['Month'] == '09')]

# Aggregate consumption by segment
seg_sum = sept13.groupby('Segment', dropna=False, as_index=False)['Consumption'].sum()

# Find segment with least consumption
least_row = seg_sum.sort_values('Consumption', ascending=True).head(1)

# Prepare final answer output (segment name and value)
answer = {
    'segment': None if least_row.empty else least_row.iloc[0]['Segment'],
    'consumption': None if least_row.empty else float(least_row.iloc[0]['Consumption'])
}

answer

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
