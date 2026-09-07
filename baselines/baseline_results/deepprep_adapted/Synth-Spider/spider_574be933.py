import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['artistID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['artistID'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fname", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
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
    # StandardizeString(table_name="table_1", column_name="lname", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["lname"] = table_1["lname"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="birth_year", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["birth_year"] = table_1["birth_year"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['quote_start', 'quote_end'])
    # DropColumn
    table_1 = table_1.drop(columns=['quote_start', 'quote_end'], errors='ignore')

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="birth_year", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['birth_year'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['birth_year']
    if _dtype == "datetime64":
        table_1['birth_year'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['birth_year'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['birth_year'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['birth_year'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="deathYear", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['deathYear'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['deathYear']
    if _dtype == "datetime64":
        table_1['deathYear'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['deathYear'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['deathYear'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['deathYear'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['artistID', 'fname', 'lname', 'birth_year', 'deathYear'])
    # SelectCol
    _cols = [c for c in ['artistID', 'fname', 'lname', 'birth_year', 'deathYear'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="sculptorID", mode="mean")
    # MissingValueImputation
    table_1["sculptorID"] = table_1["sculptorID"].fillna(table_1["sculptorID"].mean())

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="year", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['year'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['year']
    if _dtype == "datetime64":
        table_1['year'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['year'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['year'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['year'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="medium", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["medium"] = table_1["medium"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="location", mode="mode")
    # MissingValueImputation
    table_1["location"] = table_1["location"].fillna(table_1["location"].mode().iloc[0])

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # keep only pre-1900 sculptures
    #     return row['year'] is not None and int(row['year']) < 1900
    # """)
    # Filter
    def filter_func(row):
        # keep only pre-1900 sculptures
        return row['year'] is not None and int(row['year']) < 1900
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['sculptureID', 'title', 'year', 'medium', 'sculptorID', 'location'])
    # SelectCol
    _cols = [c for c in ['sculptureID', 'title', 'year', 'medium', 'sculptorID', 'location'] if c in table_1.columns]
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
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sculptures = prepared_table_2

# prepared_artists and prepared_sculptures are assumed to be synthesized per the target schemas
merged = prepared_sculptures.merge(prepared_artists, left_on='sculptorID', right_on='artistID', how='inner')
# Filter to sculptures made before 1900
merged['year'] = pd.to_numeric(merged['year'], errors='coerce')
pre1900 = merged[merged['year'] < 1900]
# Get distinct artists who made such sculptures
result = pre1900[['fname', 'lname', 'artistID']].dropna(subset=['fname','lname']).drop_duplicates(subset=['artistID'])
# Final projection: first and last names of each distinct artist
answer = result[['fname', 'lname']]

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
