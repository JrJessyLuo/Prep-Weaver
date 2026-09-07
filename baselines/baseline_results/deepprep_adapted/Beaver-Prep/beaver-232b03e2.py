import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FLOOR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'FLOOR'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR_SORT_SEQUENCE", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR_SORT_SEQUENCE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR_SORT_SEQUENCE']
    if _dtype == "datetime64":
        table_1['FLOOR_SORT_SEQUENCE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR_SORT_SEQUENCE'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'FLOOR', 'FLOOR_SORT_SEQUENCE'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'FLOOR', 'FLOOR_SORT_SEQUENCE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FLOOR'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY', 'FLOOR'], keep='last').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
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
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NAME'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='first').reset_index(drop=True)

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
prepared_floors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_buildings = prepared_table_2

# prepared_floors and prepared_buildings are the synthesized per-table outputs
# Convert FLOOR_SORT_SEQUENCE to numeric if needed
pf = prepared_floors.copy()
pf['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(pf['FLOOR_SORT_SEQUENCE'], errors='coerce')

# For each building, find the maximum floor number (by sort sequence). Keep the corresponding FLOOR label.
idx = pf.groupby('FCLT_BUILDING_KEY')['FLOOR_SORT_SEQUENCE'].idxmax()
max_floor_per_bldg = pf.loc[idx, ['FCLT_BUILDING_KEY', 'FLOOR', 'FLOOR_SORT_SEQUENCE']]

# Join to building names
result = max_floor_per_bldg.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Select the building with the overall largest floor number
max_seq = result['FLOOR_SORT_SEQUENCE'].max()
final = result[result['FLOOR_SORT_SEQUENCE'] == max_seq][['BUILDING_NAME', 'FLOOR']]

# If multiple tie, list them all
answer = final.rename(columns={'BUILDING_NAME': 'name', 'FLOOR': 'floor'})

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
