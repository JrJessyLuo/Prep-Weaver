import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="SUBJECT_TITLE_FALLBACK", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     title = row.get('SUBJECT_TITLE')
    #     short = row.get('SUBJECT_SHORT_TITLE')
    #     if pd.isna(title) or str(title).strip()=="":
    #         return None if pd.isna(short) else str(short).strip()
    #     return str(title).strip()
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        title = row.get('SUBJECT_TITLE')
        short = row.get('SUBJECT_SHORT_TITLE')
        if pd.isna(title) or str(title).strip()=="":
            return None if pd.isna(short) else str(short).strip()
        return str(title).strip()
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["SUBJECT_TITLE_FALLBACK"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_course_offerings", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     def pick_title(row):
    #         title = row.get("SUBJECT_TITLE")
    #         short = row.get("SUBJECT_SHORT_TITLE")
    #         # Normalize blanks to NA
    #         title_s = None if pd.isna(title) else str(title).strip()
    #         short_s = None if pd.isna(short) else str(short).strip()
    # 
    #         if title_s is None or title_s == "":
    #             return short_s
    #         return title_s
    # 
    #     df["SUBJECT_TITLE"] = df.apply(pick_title, axis=1)
    # 
    #     out = df[["ACADEMIC_YEAR", "TERM_CODE", "SUBJECT_ID", "SUBJECT_TITLE", "SUBJECT_SHORT_TITLE"]].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        def pick_title(row):
            title = row.get("SUBJECT_TITLE")
            short = row.get("SUBJECT_SHORT_TITLE")
            # Normalize blanks to NA
            title_s = None if pd.isna(title) else str(title).strip()
            short_s = None if pd.isna(short) else str(short).strip()

            if title_s is None or title_s == "":
                return short_s
            return title_s

        df["SUBJECT_TITLE"] = df.apply(pick_title, axis=1)

        out = df[["ACADEMIC_YEAR", "TERM_CODE", "SUBJECT_ID", "SUBJECT_TITLE", "SUBJECT_SHORT_TITLE"]].copy()
        return out
    prepared_course_offerings = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="prepared_course_offerings", subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID'], keep="first")
    # Deduplicate
    prepared_course_offerings = prepared_course_offerings.drop_duplicates(subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="prepared_course_offerings", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_course_offerings['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_course_offerings['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        prepared_course_offerings['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_course_offerings['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_course_offerings['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_course_offerings['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['prepared_course_offerings'])
    # Terminate
    result = {'prepared_course_offerings': prepared_course_offerings}
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
    # Sort(table_name="table_1", by=['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'], ascending=[True, False])
    # Sort
    table_1 = table_1.sort_values(by=['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'], ascending=[True, False])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="FIRST_DAY_OF_CLASSES", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['FIRST_DAY_OF_CLASSES'] = table_1['FIRST_DAY_OF_CLASSES'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['FIRST_DAY_OF_CLASSES'] = table_1['FIRST_DAY_OF_CLASSES'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        table_1['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'])
    # SelectCol
    _cols = [c for c in ['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['term_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES'], ascending=[True, True])

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

prepared_table_1 = _prep_1(tables['table_6'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_terms = prepared_table_2

# Merge courses with term calendar to get start dates and ensure academic year alignment
merged = prepared_courses.merge(prepared_terms, left_on='TERM_CODE', right_on='term_code', how='left', suffixes=('', '_term'))

# Choose course name, prefer SUBJECT_TITLE then fallback to SUBJECT_SHORT_TITLE
merged['course_name'] = merged['SUBJECT_TITLE'].fillna(merged['SUBJECT_SHORT_TITLE'])

# Parse FIRST_DAY_OF_CLASSES to datetime for ordering
merged['start_date'] = pd.to_datetime(merged['FIRST_DAY_OF_CLASSES'], errors='coerce', dayfirst=False, infer_datetime_format=True)

# Within each academic year, sort by start date ascending and compute cumulative count
merged = merged.sort_values(['ACADEMIC_YEAR', 'start_date', 'TERM_CODE', 'SUBJECT_ID'])
merged['cumulative_courses_in_year_and_prior'] = merged.groupby('ACADEMIC_YEAR').cumcount() + 1

# Select final columns: course name, building name placeholder (not available in selected tables), cumulative count
# Building name of the course location is not present in the provided tables; leave as None/NaN
result = merged[['course_name', 'ACADEMIC_YEAR', 'start_date', 'cumulative_courses_in_year_and_prior']].copy()
result['building_name'] = pd.NA

# Reorder as requested: course name, building name, cumulative number (partitioned by academic year, ordered by start date)
final_answer = result.sort_values(['ACADEMIC_YEAR', 'start_date'])[['course_name', 'building_name', 'cumulative_courses_in_year_and_prior']]

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
