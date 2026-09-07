import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_RESERVE_CATALOG_KEY'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_RESERVE_CATALOG_KEY'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # OutlierDetection(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.25)
    _q3 = table_1['NUM_ENROLLED_STUDENTS'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['NUM_ENROLLED_STUDENTS'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] == False]
        table_1.drop(columns=['table_1_NUM_ENROLLED_STUDENTS_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'] = table_1['table_1_NUM_ENROLLED_STUDENTS_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_SUBJECT_OFFERED_KEY"] = table_1["LIBRARY_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="term_code", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["term_code"] = table_1["term_code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
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

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
prepared_reserve_links = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_course_offerings = prepared_table_2

# prepared_reserve_links and prepared_course_offerings are the synthesized per-table outputs
links = prepared_reserve_links.copy()
courses = prepared_course_offerings.copy()

# Normalize course key whitespace if needed
for df, col in [(links, 'LIBRARY_SUBJECT_OFFERED_KEY'), (courses, 'LIBRARY_SUBJECT_OFFERED_KEY')]:
    df[col] = df[col].astype(str).str.strip()

# Join reserves to course metadata
joined = links.merge(
    courses,
    how='inner',
    left_on='LIBRARY_SUBJECT_OFFERED_KEY',
    right_on='LIBRARY_SUBJECT_OFFERED_KEY'
)

# Compute per-course metrics first
# - courses_using_materials: count distinct course keys that appear in reserves (will be 1 per course in this per-course table)
# - catalog_items_per_course: count distinct catalog item keys per course
per_course = (
    joined.groupby(['LIBRARY_SUBJECT_OFFERED_KEY', 'OFFER_DEPT_NAME'], as_index=False)
          .agg(
              catalog_items_per_course=('LIBRARY_RESERVE_CATALOG_KEY', 'nunique'),
              avg_enrollment_course=('NUM_ENROLLED_STUDENTS', 'first')
          )
)
# Mark each course that uses materials (presence in joined implies usage)
per_course['courses_using_materials'] = 1

# Aggregate to department level
by_dept = (
    per_course.groupby('OFFER_DEPT_NAME', as_index=False)
              .agg(
                  total_courses_using_materials=('courses_using_materials', 'sum'),
                  total_catalog_items=('catalog_items_per_course', 'sum'),
                  avg_enrollment_per_course=('avg_enrollment_course', 'mean')
              )
)
by_dept = by_dept.rename(columns={'OFFER_DEPT_NAME': 'Department'})

# Compute grand total across all departments
grand = pd.DataFrame({
    'Department': ['Grand Total'],
    'total_courses_using_materials': [per_course['courses_using_materials'].sum()],
    'total_catalog_items': [per_course['catalog_items_per_course'].sum()],
    'avg_enrollment_per_course': [per_course['avg_enrollment_course'].mean()]
})

# Final result with department rows plus grand total
target = pd.concat([by_dept, grand], ignore_index=True)

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
