import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Name_Part2", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Name_Part2"] = table_1["Name_Part2"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Name_Part1", func="""
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return s
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return s
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Name_Part1"] = table_1["Name_Part1"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['Name_Part1', 'Name_Part2'], target_column="Theater_Name", func="""
    # import pandas as pd
    # def concat(row: pd.Series) -> str:
    #     p1 = row.get('Name_Part1')
    #     p2 = row.get('Name_Part2')
    #     p1 = '' if p1 is None or (isinstance(p1, float) and pd.isna(p1)) else str(p1)
    #     p2 = '' if p2 is None or (isinstance(p2, float) and pd.isna(p2)) else str(p2)
    #     return (p1 + p2).strip()
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        p1 = row.get('Name_Part1')
        p2 = row.get('Name_Part2')
        p1 = '' if p1 is None or (isinstance(p1, float) and pd.isna(p1)) else str(p1)
        p2 = '' if p2 is None or (isinstance(p2, float) and pd.isna(p2)) else str(p2)
        return (p1 + p2).strip()
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["Theater_Name"] = table_1[['Name_Part1', 'Name_Part2']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['Name_Part1', 'Name_Part2'])

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Movie", dtype="float")
    # CastType
    _dtype = 'float'
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Code', 'Movie', 'Theater_Name'])
    # SelectCol
    _cols = [c for c in ['Code', 'Movie', 'Theater_Name'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['movie_title'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['movie_title'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Code', 'movie_title'])
    # SelectCol
    _cols = [c for c in ['Code', 'movie_title'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_theaters = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_movies = prepared_table_2

# Assume prepared_theaters and prepared_movies are already synthesized per targets
# Filter for Odeon or Imperial theaters, then join to get movie titles and select unique titles
filtered = prepared_theaters[prepared_theaters['Theater_Name'].str.strip().str.lower().isin(['odeon','imperial'])]
merged = filtered.merge(prepared_movies, left_on='Movie', right_on='Code', how='inner')
# Extract distinct movie titles
answer = merged['movie_title'].dropna().drop_duplicates().sort_values().reset_index(drop=True)

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
