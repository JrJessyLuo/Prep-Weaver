import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Code", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Code'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Code']
    if _dtype == "datetime64":
        table_1['Code'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Code'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Code'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Code'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="trc", target_columns=['MovieName', 'Rating'], func="""
    # def split(val):
    #     if val is None:
    #         return {"MovieName": None, "Rating": None}
    #     s = str(val)
    #     parts = s.split('###', 1)
    #     movie = parts[0].strip() if len(parts) > 0 else ''
    #     rating = parts[1].strip() if len(parts) > 1 else ''
    #     return {"MovieName": movie, "Rating": rating}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"MovieName": None, "Rating": None}
        s = str(val)
        parts = s.split('###', 1)
        movie = parts[0].strip() if len(parts) > 0 else ''
        rating = parts[1].strip() if len(parts) > 1 else ''
        return {"MovieName": movie, "Rating": rating}
    for _c in ['MovieName', 'Rating']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['trc']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['MovieName', 'Rating']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['trc'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Code', 'MovieName', 'Rating'])
    # SelectCol
    _cols = [c for c in ['Code', 'MovieName', 'Rating'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Transpose(table_name="table_1")
    # Transpose
    if table_1.empty or len(table_1.columns) == 0:
        table_1 = table_1.transpose()
    else:
        _t = table_1.transpose()
        _newcols = _t.iloc[0].tolist()
        _t = _t.iloc[1:]
        _first = table_1.columns[0]
        _t.insert(0, _first, _t.index)
        _t.columns = [_first] + _newcols
        table_1 = _t.reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Movie'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Movie'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Movie", dtype="str")
    # CastType
    _dtype = 'str'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Movie'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Movie']
    if _dtype == "datetime64":
        table_1['Movie'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Movie'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Movie'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Movie'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Movie", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # Convert strings like "5.0" -> "5"
    #     m = re.fullmatch(r"(-?\d+)\.0+", s)
    #     if m:
    #         return m.group(1)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # Convert strings like "5.0" -> "5"
        m = re.fullmatch(r"(-?\d+)\.0+", s)
        if m:
            return m.group(1)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Movie"] = table_1["Movie"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Name', 'new_name': 'CinemaName'}, {'old_name': 'Movie', 'new_name': 'MovieCode'}])
    # Rename
    table_1 = table_1.rename(columns={'Name': 'CinemaName', 'Movie': 'MovieCode'})

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CinemaName', 'MovieCode'])
    # SelectCol
    _cols = [c for c in ['CinemaName', 'MovieCode'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
movies = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
cinema_movie_map = prepared_table_2

# Assume prepared tables are provided as DataFrames: movies, cinema_movie_map
# Filter to the target cinemas
target_cinemas = ['Odeon', 'Imperial']
cm_filt = cinema_movie_map[cinema_movie_map['CinemaName'].isin(target_cinemas)].copy()

# Normalize types for join
cm_filt['MovieCode'] = cm_filt['MovieCode'].astype(str).str.replace('.0', '', regex=False)
movies_norm = movies.copy()
movies_norm['Code'] = movies_norm['Code'].astype(str)

# Join to get movie names
joined = cm_filt.merge(movies_norm, left_on='MovieCode', right_on='Code', how='inner')

# Select unique movie names played in either cinema
result = joined['MovieName'].dropna().drop_duplicates().sort_values().tolist()

# If a DataFrame is expected as final output
answer = pd.DataFrame({'MovieName': result})

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
