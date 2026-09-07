import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['BUILDING_KEY', 'FLOOR'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_KEY', 'FLOOR'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'FLOOR'], keep='first').reset_index(drop=True)

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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('BUILDING_KEY') is not None and str(row.get('BUILDING_KEY')).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        return row.get('BUILDING_KEY') is not None and str(row.get('BUILDING_KEY')).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'BUILDING_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'BUILDING_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NAME'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_floors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2

# Assume prepared_floors and prepared_buildings are provided as per targets
# Count floors per building (ensure unique floors if duplicates exist)
floor_counts = (prepared_floors
                .dropna(subset=["BUILDING_KEY", "FLOOR"]) 
                .drop_duplicates(subset=["BUILDING_KEY", "FLOOR"]) 
                .groupby("BUILDING_KEY", as_index=False)["FLOOR"].count()
                .rename(columns={"FLOOR": "NUM_FLOORS"}))

# Join to building names
with_names = floor_counts.merge(prepared_buildings[["BUILDING_KEY", "BUILDING_NAME"]], on="BUILDING_KEY", how="left")

# Find max number of floors and filter
max_floors = with_names["NUM_FLOORS"].max()
result = with_names.loc[with_names["NUM_FLOORS"] == max_floors, ["BUILDING_NAME"]]

# Final output: list the names (ties included)
answer = result.sort_values(by=["BUILDING_NAME"]).reset_index(drop=True)

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
