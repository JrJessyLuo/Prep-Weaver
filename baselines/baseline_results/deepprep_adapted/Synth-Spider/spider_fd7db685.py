import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="artistID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['artistID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['artistID']
    if _dtype == "datetime64":
        table_1['artistID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['artistID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['artistID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['artistID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fname", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fname"] = table_1["fname"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['artistID', 'fname'])
    # SelectCol
    _cols = [c for c in ['artistID', 'fname'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['artistID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['artistID'], keep='first').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="paintingID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['paintingID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['paintingID']
    if _dtype == "datetime64":
        table_1['paintingID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['paintingID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['paintingID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['paintingID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="painterID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['painterID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['painterID']
    if _dtype == "datetime64":
        table_1['painterID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['painterID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['painterID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['painterID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['painterID', 'paintingID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['painterID', 'paintingID'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['painterID', 'paintingID'])
    # SelectCol
    _cols = [c for c in ['painterID', 'paintingID'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_paintings = prepared_table_2

# Merge artists with paintings on artistID = painterID
merged = prepared_artists.merge(prepared_paintings, left_on='artistID', right_on='painterID', how='left')
# Count number of paintings per artist
counts = merged.groupby(['artistID','fname'], dropna=False)['paintingID'].nunique().reset_index(name='num_works')
# Filter artists with at least two paintings
result = counts[counts['num_works'] >= 2][['fname','num_works']]
# If needed, sort for presentation (not required)
# result = result.sort_values(['num_works','fname'], ascending=[False, True])
answer = result

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
