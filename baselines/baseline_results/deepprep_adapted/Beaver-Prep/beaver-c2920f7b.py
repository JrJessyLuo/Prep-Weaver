import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="LIBRARY_SUBJECT_OFFERED_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['LIBRARY_SUBJECT_OFFERED_KEY']
    if _dtype == "datetime64":
        table_1['LIBRARY_SUBJECT_OFFERED_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['LIBRARY_SUBJECT_OFFERED_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['LIBRARY_SUBJECT_OFFERED_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['LIBRARY_SUBJECT_OFFERED_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY'], keep='first').reset_index(drop=True)

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
    # DropColumn(table_name="table_1", drop_columns=['COURSE_NAME', 'DEPARTMENT', 'DATE_FROM', 'DATE_TO', 'UNIT_CODE', 'UNIT', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['COURSE_NAME', 'DEPARTMENT', 'DATE_FROM', 'DATE_TO', 'UNIT_CODE', 'UNIT', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_COURSE_INSTRUCTOR_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # collapse internal whitespace
    #     s = ' '.join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # collapse internal whitespace
        s = ' '.join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"] = table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="INSTRUCTOR_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # collapse internal whitespace
    #     s = ' '.join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # collapse internal whitespace
        s = ' '.join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["INSTRUCTOR_NAME"] = table_1["INSTRUCTOR_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep='last').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="CATALOG_YEAR", func="""
    # def is_valid_year(val):
    #     try:
    #         if val is None:
    #             return False
    #         y = float(val)
    #         return y >= 1000 and y <= 2100
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_year(val):
        try:
            if val is None:
                return False
            y = float(val)
            return y >= 1000 and y <= 2100
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_year(val))
        except Exception:
            return False
    table_1 = table_1[table_1['CATALOG_YEAR'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_catalog_year", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Coerce to numeric; invalid parses become NaN
    #     y = pd.to_numeric(df["CATALOG_YEAR"], errors="coerce")
    # 
    #     # Keep only plausible publication years; others -> NaN
    #     y = y.where((y >= 1000) & (y <= 2100), np.nan)
    # 
    #     # Store as integer-like (nullable) for downstream min/max
    #     df["CATALOG_YEAR"] = y.round().astype("Int64")
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Coerce to numeric; invalid parses become NaN
        y = pd.to_numeric(df["CATALOG_YEAR"], errors="coerce")

        # Keep only plausible publication years; others -> NaN
        y = y.where((y >= 1000) & (y <= 2100), np.nan)

        # Store as integer-like (nullable) for downstream min/max
        df["CATALOG_YEAR"] = y.round().astype("Int64")

        return df
    prepared_catalog_year = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="prepared_catalog_year", subset=['library_reserve_catalog_key', 'CATALOG_YEAR'], how="any")
    # DropNulls
    prepared_catalog_year = prepared_catalog_year.dropna(subset=['library_reserve_catalog_key', 'CATALOG_YEAR'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="prepared_catalog_year", columns=['library_reserve_catalog_key', 'CATALOG_YEAR'])
    # SelectCol
    _cols = [c for c in ['library_reserve_catalog_key', 'CATALOG_YEAR'] if c in prepared_catalog_year.columns]
    prepared_catalog_year = prepared_catalog_year[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="prepared_catalog_year", subset=['library_reserve_catalog_key'], keep="last")
    # Deduplicate
    prepared_catalog_year = prepared_catalog_year.drop_duplicates(subset=['library_reserve_catalog_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['prepared_catalog_year'])
    # Terminate
    result = {'prepared_catalog_year': prepared_catalog_year}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["LIBRARY_SUBJECT_OFFERED_KEY"] = table_1["LIBRARY_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_ENROLLED_STUDENTS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_ENROLLED_STUDENTS']
    if _dtype == "datetime64":
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_ENROLLED_STUDENTS'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", mode="mean")
    # MissingValueImputation
    table_1["NUM_ENROLLED_STUDENTS"] = table_1["NUM_ENROLLED_STUDENTS"].fillna(table_1["NUM_ENROLLED_STUDENTS"].mean())

    # ---------------- Step 4 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['LIBRARY_SUBJECT_OFFERED_KEY'], agg=[{'column': 'NUM_ENROLLED_STUDENTS', 'agg_func': 'sum'}])
    # GroupBy
    table_1 = table_1.groupby(['LIBRARY_SUBJECT_OFFERED_KEY'], as_index=False).agg({'NUM_ENROLLED_STUDENTS': 'sum'})

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_ENROLLED_STUDENTS", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_ENROLLED_STUDENTS']
    if _dtype == "datetime64":
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_ENROLLED_STUDENTS'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
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
reserves_by_instructor = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
instructor_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
catalog_metadata = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
subject_offerings = prepared_table_4

# Start from prepared tables
r = reserves_by_instructor.copy()
i = instructor_lookup.copy()
c = catalog_metadata.copy()
s = subject_offerings.copy()

# Join reserves to instructor names
ri = r.merge(i, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')

# Join catalog years to each reserve item
ric = ri.merge(c, left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='left')

# Join enrollment via subject offering key
rics = ric.merge(s, on='LIBRARY_SUBJECT_OFFERED_KEY', how='left')

# Compute aggregates per instructor
# Treat CATALOG_YEAR==0 or null as missing for min/max calculations
years = rics['CATALOG_YEAR'].where(rics['CATALOG_YEAR'].notna() & (rics['CATALOG_YEAR'] != 0))
rics = rics.assign(_year=years)

# Enrollment may repeat across multiple reserve rows for the same offering; to sum students per instructor
# we first compute total enrolled per instructor by distinct subject offering keys, then combine with reserves count and year stats
# 1) total reserves and year stats per instructor
agg_reserves = rics.groupby(['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME'], dropna=False).agg(
    total_reserve_materials=('LIBRARY_RESERVE_CATALOG_KEY','count'),
    min_publication_year=('_year','min'),
    max_publication_year=('_year','max')
).reset_index()

# 2) total enrolled students per instructor = sum of NUM_ENROLLED_STUDENTS over distinct subject offerings for that instructor
distinct_offerings = rics[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME','LIBRARY_SUBJECT_OFFERED_KEY','NUM_ENROLLED_STUDENTS']].drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY'])
agg_enroll = distinct_offerings.groupby(['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME'], dropna=False).agg(
    total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum')
).reset_index()

# Final result per instructor
target = agg_reserves.merge(agg_enroll, on=['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME'], how='left')

# Optional: sort by instructor name
target = target.sort_values(['INSTRUCTOR_NAME']).reset_index(drop=True)

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
