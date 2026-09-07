import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Collecrtion_Subset_Details', 'new_name': 'Collection_Subset_Details'}])
    # Rename
    table_1 = table_1.rename(columns={'Collecrtion_Subset_Details': 'Collection_Subset_Details'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Collection_Subset_Name", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # strip surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     # collapse internal whitespace
    #     s = re.sub(r'\s+', ' ', s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # strip surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        # collapse internal whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Collection_Subset_Name"] = table_1["Collection_Subset_Name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Collection_Subset_ID', 'Collection_Subset_Name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Collection_Subset_ID', 'Collection_Subset_Name'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # remove empty-string names after standardization
    #     return str(row[\"Collection_Subset_Name\"]).strip() != \"\"
    # """)
    # Filter
    def filter_func(row):
        # remove empty-string names after standardization
        return str(row[\"Collection_Subset_Name\"]).strip() != \"\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Collection_Subset_ID', 'Collection_Subset_Name'])
    # SelectCol
    _cols = [c for c in ['Collection_Subset_ID', 'Collection_Subset_Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Collection_Subset_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Collection_Subset_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Collection_Subset_ID', 'Collection_Subset_Name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Collection_Subset_ID', 'Collection_Subset_Name'], keep='first').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="subset_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['subset_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['subset_id']
    if _dtype == "datetime64":
        table_1['subset_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['subset_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['subset_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['subset_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['subset_id'])
    # SelectCol
    _cols = [c for c in ['subset_id'] if c in table_1.columns]
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
prepared_collection_subsets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_collection_subset_links = prepared_table_2

target = prepared_collection_subsets.merge(prepared_collection_subset_links, left_on='Collection_Subset_ID', right_on='subset_id', how='left'); result = target.groupby(['Collection_Subset_ID','Collection_Subset_Name'], dropna=False).size().reset_index(name='num_collections'); result = result[['Collection_Subset_ID','Collection_Subset_Name','num_collections']].sort_values(['Collection_Subset_ID'])

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
