import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # normalize whitespace and strip
    #     s = re.sub(r'\s+', ' ', str(s)).strip()
    #     # treat common null-like strings as missing
    #     if s.lower() in {'nan', 'none', 'null', ''}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # normalize whitespace and strip
        s = re.sub(r'\s+', ' ', str(s)).strip()
        # treat common null-like strings as missing
        if s.lower() in {'nan', 'none', 'null', ''}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["RESPONSIBLE_FACULTY_NAME"] = table_1["RESPONSIBLE_FACULTY_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="responsible_faculty_mit_id", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['responsible_faculty_mit_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['responsible_faculty_mit_id']
    if _dtype == "datetime64":
        table_1['responsible_faculty_mit_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['responsible_faculty_mit_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['responsible_faculty_mit_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['responsible_faculty_mit_id'] = _series.astype(str)

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

prepared_table_1 = _prep_1(tables['table_7'])
prepared_subject_offerings = prepared_table_1

# Start from the prepared table
subjects = prepared_subject_offerings.copy()

# Identify fall term rows. Assuming TERM_CODE encodes year+term where 'FA' or similar marks fall.
# If fall is encoded differently (e.g., '2012FA' or '2012F'), adjust the pattern accordingly.
fall_mask = subjects['TERM_CODE'].astype(str).str.contains('FA', case=False, na=False)
fall_subjects = subjects.loc[fall_mask].copy()

# Keep unique subjects by SUBJECT_ID and TERM_CODE, preserving title and instructor
fall_unique = (
    fall_subjects
    .dropna(subset=['SUBJECT_ID', 'SUBJECT_TITLE'])
    .drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'])
)

# Compute total number of unique subject types (unique SUBJECT_IDs) per instructor
counts_per_instructor = (
    fall_unique
    .dropna(subset=['RESPONSIBLE_FACULTY_NAME'])
    .groupby(['RESPONSIBLE_FACULTY_NAME'], dropna=True)['SUBJECT_ID']
    .nunique()
    .reset_index(name='total_subject_types_per_instructor')
)

# Attach counts back to each subject row
result = fall_unique.merge(counts_per_instructor, on='RESPONSIBLE_FACULTY_NAME', how='left')

# Select and rename final columns; email not available in this table, set as None
result['instructor_email'] = None
answer = result[['SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'instructor_email', 'total_subject_types_per_instructor']].drop_duplicates()

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
