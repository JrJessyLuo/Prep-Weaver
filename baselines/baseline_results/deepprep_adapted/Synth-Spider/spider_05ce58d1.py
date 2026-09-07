import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Region_ID', 'Building_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Region_ID', 'Building_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Region_ID', 'Building_ID'])
    # SelectCol
    _cols = [c for c in ['Region_ID', 'Building_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Region_ID', 'Building_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Region_ID', 'Building_ID'], keep='first').reset_index(drop=True)

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
    # AddNewColumn(table_name="table_1", new_column_name="Region_Name", func="""
    # def compute(row):
    #     p1 = row.get("Name_Part1")
    #     p2 = row.get("Name_Part2")
    #     p1 = "" if p1 is None else str(p1).strip()
    #     p2 = "" if p2 is None else str(p2).strip()
    #     return (p1 + (" " + p2 if p2 else "")).strip()
    # """)
    # AddNewColumn
    def compute(row):
        p1 = row.get("Name_Part1")
        p2 = row.get("Name_Part2")
        p1 = "" if p1 is None else str(p1).strip()
        p2 = "" if p2 is None else str(p2).strip()
        return (p1 + (" " + p2 if p2 else "")).strip()
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["Region_Name"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Region_ID', 'Name_Part1', 'Name_Part2'])
    # SelectCol
    _cols = [c for c in ['Region_ID', 'Name_Part1', 'Name_Part2'] if c in table_1.columns]
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
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_regions = prepared_table_2

regions = prepared_regions.copy()
regions['Region_Name'] = regions[['Name_Part1','Name_Part2']].apply(lambda r: r['Name_Part1'] if (pd.isna(r['Name_Part2']) or str(r['Name_Part2']).lower()=='none' or str(r['Name_Part2']).strip()=='') else f"{r['Name_Part1']} {r['Name_Part2']}", axis=1)
joined = regions.merge(prepared_buildings[['Region_ID','Building_ID']].drop_duplicates(), on='Region_ID', how='left')
no_building_regions = joined[joined['Building_ID'].isna()]
answer = no_building_regions['Region_Name'].dropna().drop_duplicates().sort_values().tolist()

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
