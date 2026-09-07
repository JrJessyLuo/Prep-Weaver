import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Collection_Subset_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Collection_Subset_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Collection_Subset_ID']
    if _dtype == "datetime64":
        table_1['Collection_Subset_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Collection_Subset_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Collection_Subset_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Collection_Subset_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Collection_Subset_ID', 'Collection_Subset_Name'])
    # SelectCol
    _cols = [c for c in ['Collection_Subset_ID', 'Collection_Subset_Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Collection_Subset_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Collection_Subset_ID'], keep='first').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="Collection_Subset_ID", mode="mode")
    # MissingValueImputation
    table_1["Collection_Subset_ID"] = table_1["Collection_Subset_ID"].fillna(table_1["Collection_Subset_ID"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Collection_ID', 'Collection_Subset_ID'])
    # SelectCol
    _cols = [c for c in ['Collection_ID', 'Collection_Subset_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Collection_ID', 'Collection_Subset_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Collection_ID', 'Collection_Subset_ID'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Document_Object_ID', 'Collection_ID'], how="all")
    # DropNulls
    table_1 = table_1.dropna(subset=['Document_Object_ID', 'Collection_ID'], how='all').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Document_Object_ID', 'Collection_ID'])
    # SelectCol
    _cols = [c for c in ['Document_Object_ID', 'Collection_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Document_Object_ID', 'Collection_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Document_Object_ID', 'Collection_ID'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_subsets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_collection_subsets = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_documents = prepared_table_3

tmp = prepared_collection_subsets.merge(prepared_documents, on='Collection_ID', how='left')
joined = tmp.merge(prepared_subsets, on='Collection_Subset_ID', how='right')
result = joined.groupby(['Collection_Subset_ID','Collection_Subset_Name'])['Document_Object_ID'].nunique().reset_index(name='num_distinct_documents')
result = result.sort_values(['Collection_Subset_ID'])
answer = result[['Collection_Subset_ID','Collection_Subset_Name','num_distinct_documents']]

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
