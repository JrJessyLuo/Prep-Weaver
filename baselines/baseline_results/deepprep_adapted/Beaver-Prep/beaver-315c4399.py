import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace/newlines
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize internal whitespace/newlines
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE'])
    # SelectCol
    _cols = [c for c in ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="FIRST_DAY_OF_CLASSES", date_format="%d-%b-%y")
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
    if '%d-%b-%y':
        table_1['FIRST_DAY_OF_CLASSES'] = table_1['FIRST_DAY_OF_CLASSES'].dt.strftime('%d-%b-%y')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="LAST_DAY_OF_CLASSES", date_format="%d-%b-%y")
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
    table_1['LAST_DAY_OF_CLASSES'] = table_1['LAST_DAY_OF_CLASSES'].apply(_sd_parse)
    if '%d-%b-%y':
        table_1['LAST_DAY_OF_CLASSES'] = table_1['LAST_DAY_OF_CLASSES'].dt.strftime('%d-%b-%y')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES', 'LAST_DAY_OF_CLASSES'])
    # SelectCol
    _cols = [c for c in ['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES', 'LAST_DAY_OF_CLASSES'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_7'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_terms = prepared_table_2

# Assume prepared_courses and prepared_terms are provided as per the target schemas
# 1) Join courses to terms on term code
joined = prepared_courses.merge(prepared_terms, left_on='TERM_CODE', right_on='term_code', how='inner', suffixes=('', '_term'))

# 2) Parse dates and compute duration in days (inclusive of both endpoints if desired; here use difference in days + 1)
for col in ['FIRST_DAY_OF_CLASSES', 'LAST_DAY_OF_CLASSES']:
    joined[col] = pd.to_datetime(joined[col], errors='coerce')

joined['duration_days'] = (joined['LAST_DAY_OF_CLASSES'] - joined['FIRST_DAY_OF_CLASSES']).dt.days + 1

# 3) Compute running average over window of 2 preceding and 2 following courses within academic year ordered by course start date
joined = joined.sort_values(['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES', 'SUBJECT_ID'])
rolling_avg = (
    joined
    .groupby('ACADEMIC_YEAR', group_keys=False)['duration_days']
    .apply(lambda s: s.rolling(window=5, min_periods=1, center=True).mean())
)
joined['running_avg_duration_days'] = rolling_avg

# 4) Select required output columns
result = joined[['SUBJECT_TITLE', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES', 'duration_days', 'running_avg_duration_days']]
result = result.rename(columns={
    'SUBJECT_TITLE': 'course_title',
    'FIRST_DAY_OF_CLASSES': 'course_start_date'
})

# The final answer expects: for each course: title, building of the course location, duration (days), and running average.
# Note: The selected tables do not include a building/location column. If building info exists in other tables, it must be joined there.
# For now, produce without building, or fill as NaN to indicate missing from provided sources.
result['building_name'] = pd.NA
result = result[['course_title', 'building_name', 'duration_days', 'running_avg_duration_days', 'ACADEMIC_YEAR', 'course_start_date']]

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
