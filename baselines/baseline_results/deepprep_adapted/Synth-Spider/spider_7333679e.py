import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['transcript_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['transcript_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date_of_transcript", date_format="%Y-%m-%d")
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
    table_1['date_of_transcript'] = table_1['date_of_transcript'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date_of_transcript'] = table_1['date_of_transcript'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['transcript_id', 'student_id', 'date_of_transcript'])
    # SelectCol
    _cols = [c for c in ['transcript_id', 'student_id', 'date_of_transcript'] if c in table_1.columns]
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
    # ErrorDetection(table_name="table_1", column_name="class_id", func="""
    # def is_valid(val):
    #     try:
    #         return val is not None and str(val).strip() != "" and int(val) > 0
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        try:
            return val is not None and str(val).strip() != "" and int(val) > 0
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['class_id'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="cd", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize internal whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["cd"] = table_1["cd"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="class_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['class_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['class_id']
    if _dtype == "datetime64":
        table_1['class_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['class_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['class_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['class_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="student_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['student_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['student_id']
    if _dtype == "datetime64":
        table_1['student_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['student_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['student_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['student_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="tid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['tid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['tid']
    if _dtype == "datetime64":
        table_1['tid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['tid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['tid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['tid'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['class_id', 'student_id', 'tid'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['class_id', 'student_id', 'tid'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['class_id', 'student_id', 'tid', 'cd'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['class_id', 'student_id', 'tid', 'cd'], keep='first').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['student_id', 'tid', 'class_id', 'cd'])
    # SelectCol
    _cols = [c for c in ['student_id', 'tid', 'class_id', 'cd'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Count(table_name="table_1")
    # Count -> statistic_table
    _stat_row = pd.DataFrame({'operator': ['Count(table_name="table_1")'], 'statistic_name': ['count'], 'value': [len(table_1)]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['teacher_id', 'detail_value', 'prefix', 'suffix'])
    # SelectCol
    _cols = [c for c in ['teacher_id', 'detail_value', 'prefix', 'suffix'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="teacher_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['teacher_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['teacher_id']
    if _dtype == "datetime64":
        table_1['teacher_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['teacher_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['teacher_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['teacher_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['teacher_id', 'detail_value'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['teacher_id', 'detail_value'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['teacher_id', 'prefix', 'suffix'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['teacher_id', 'prefix', 'suffix'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_transcripts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_enrollments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_teachers = prepared_table_3

# Assume prepared_transcripts, prepared_enrollments, prepared_teachers are dataframes
# 1) Find student(s) with earliest transcript issuance
earliest_date = prepared_transcripts['date_of_transcript']
if not pd.api.types.is_datetime64_any_dtype(earliest_date):
    prepared_transcripts = prepared_transcripts.assign(date_of_transcript=pd.to_datetime(prepared_transcripts['date_of_transcript'], errors='coerce'))
earliest_dt = prepared_transcripts['date_of_transcript'].min()
earliest_students = prepared_transcripts.loc[prepared_transcripts['date_of_transcript'] == earliest_dt, ['student_id']].drop_duplicates()

# 2) Join to enrollments to get teacher ids for those students
stu_enroll = earliest_students.merge(prepared_enrollments, on='student_id', how='inner')

# 3) Join to teachers on teacher_id (tid)
stu_teachers = stu_enroll.merge(prepared_teachers, left_on='tid', right_on='teacher_id', how='inner')

# 4) Deduplicate teachers and select teacher details
target = stu_teachers[['teacher_id', 'detail_value', 'prefix', 'suffix']].drop_duplicates().reset_index(drop=True)

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
