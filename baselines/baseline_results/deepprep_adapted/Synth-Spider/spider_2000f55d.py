import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['artistID', 'birthYear'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['artistID', 'birthYear'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="birthYear", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['birthYear'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['birthYear']
    if _dtype == "datetime64":
        table_1['birthYear'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['birthYear'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['birthYear'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['birthYear'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return row['birthYear'] < 1850
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return row['birthYear'] < 1850
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['artistID', 'birthYear', 'fname', 'prefix', 'last_name'])
    # SelectCol
    _cols = [c for c in ['artistID', 'birthYear', 'fname', 'prefix', 'last_name'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['paintingID', 'title', 'year', 'w_mm', 'painterID'])
    # SelectCol
    _cols = [c for c in ['paintingID', 'title', 'year', 'w_mm', 'painterID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="w_mm", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['w_mm'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['w_mm']
    if _dtype == "datetime64":
        table_1['w_mm'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['w_mm'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['w_mm'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['w_mm'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['paintingID', 'title', 'w_mm', 'painterID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['paintingID', 'title', 'w_mm', 'painterID'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['year'])
    # DropColumn
    table_1 = table_1.drop(columns=['year'], errors='ignore')

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

# prepared_artists and prepared_paintings are the synthesized per-table targets
merged = prepared_paintings.merge(prepared_artists, left_on='painterID', right_on='artistID', how='inner')
# Filter artists born prior to 1850
merged = merged[pd.to_numeric(merged['birthYear'], errors='coerce') < 1850]
# Select painting widths (and optional identifiers/evidence)
result = merged[['paintingID', 'title', 'w_mm']]
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
