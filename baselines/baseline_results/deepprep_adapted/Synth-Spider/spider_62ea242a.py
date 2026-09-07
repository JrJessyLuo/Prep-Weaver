import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Research_point", mode="median")
    # MissingValueImputation
    table_1["Research_point"] = table_1["Research_point"].fillna(table_1["Research_point"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['ID_Tens', 'ID_Units'], target_column="University_ID", func="""
    # def concat(row: pd.Series) -> str:
    #     # combine as string key, e.g., "0" + "1" -> "01"
    #     return f"{str(row['ID_Tens']).strip()}{str(row['ID_Units']).strip()}"
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        # combine as string key, e.g., "0" + "1" -> "01"
        return f"{str(row['ID_Tens']).strip()}{str(row['ID_Units']).strip()}"
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["University_ID"] = table_1[['ID_Tens', 'ID_Units']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['ID_Tens', 'ID_Units'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="University_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['University_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['University_ID']
    if _dtype == "datetime64":
        table_1['University_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['University_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['University_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['University_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['University_ID'], agg=[{'column': 'Research_point', 'agg_func': 'max'}])
    # GroupBy
    table_1 = table_1.groupby(['University_ID'], as_index=False).agg({'Research_point': 'max'})

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['University_ID', 'Research_point'])
    # SelectCol
    _cols = [c for c in ['University_ID', 'Research_point'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Uni_Name_Suffix", func="""
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
    table_1["Uni_Name_Suffix"] = table_1["Uni_Name_Suffix"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Uni_Name_Prefix", func="""
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
    table_1["Uni_Name_Prefix"] = table_1["Uni_Name_Prefix"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['University_ID', 'Uni_Name_Prefix', 'Uni_Name_Suffix'])
    # SelectCol
    _cols = [c for c in ['University_ID', 'Uni_Name_Prefix', 'Uni_Name_Suffix'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
prepared_scores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_universities = prepared_table_2

# prepared_scores: expects columns [ID_Tens, ID_Units, Research_point] from table_1
prepared_scores = table_1.copy()
prepared_scores['University_ID'] = (prepared_scores['ID_Tens'].astype(str) + prepared_scores['ID_Units'].astype(str)).astype(int)
prepared_scores = prepared_scores[['University_ID', 'Research_point']]

# prepared_universities: expects columns [University_ID, Uni_Name_Prefix, Uni_Name_Suffix] from table_2
prepared_universities = table_2[['University_ID', 'Uni_Name_Prefix', 'Uni_Name_Suffix']].copy()
prepared_universities['University_ID'] = prepared_universities['University_ID'].astype(int)

# Integrate on University_ID
merged = prepared_scores.merge(prepared_universities, on='University_ID', how='inner')

# Find university with the maximum Research_point
max_row = merged.loc[merged['Research_point'].astype(int).idxmax()]

# Construct full name (handle missing suffix/prefix gracefully)
prefix = str(max_row.get('Uni_Name_Prefix', '') or '').strip()
suffix = str(max_row.get('Uni_Name_Suffix', '') or '').strip()
full_name = (prefix + (' ' + suffix if suffix else '')).strip()

answer = full_name

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
