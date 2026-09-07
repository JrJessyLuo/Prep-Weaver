import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
    #         s = s[1:-1]
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
            s = s[1:-1]
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
    #         s = s[1:-1]
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
            s = s[1:-1]
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EFFECTIVE_TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
    #         s = s[1:-1]
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
            s = s[1:-1]
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EFFECTIVE_TERM_CODE"] = table_1["EFFECTIVE_TERM_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TERM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TERM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TERM_CODE']
    if _dtype == "datetime64":
        table_1['TERM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TERM_CODE'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SUBJECT_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SUBJECT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SUBJECT_ID']
    if _dtype == "datetime64":
        table_1['SUBJECT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SUBJECT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SUBJECT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SUBJECT_ID'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="EFFECTIVE_TERM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['EFFECTIVE_TERM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['EFFECTIVE_TERM_CODE']
    if _dtype == "datetime64":
        table_1['EFFECTIVE_TERM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['EFFECTIVE_TERM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['EFFECTIVE_TERM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['EFFECTIVE_TERM_CODE'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'EFFECTIVE_TERM_CODE'])
    # SelectCol
    _cols = [c for c in ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'EFFECTIVE_TERM_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'EFFECTIVE_TERM_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'EFFECTIVE_TERM_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 11 ----------------
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
prepared_subject_offerings = prepared_table_1

# Start from prepared_subject_offerings (synthesized from table_1 with the listed columns)
df = prepared_subject_offerings.copy()

# Define a helper to compute the term ordering so we can identify prior terms
# Assumes TERM_CODE and EFFECTIVE_TERM_CODE follow patterns like 'YYYYFA', 'YYYYSP', 'YYYYSU', 'YYYYWI'
term_order_map = {'WI': 1, 'SP': 2, 'SU': 3, 'FA': 4}

def parse_term_code(tc):
    if pd.isna(tc):
        return (None, None)
    s = str(tc)
    year = int(s[:4])
    suf = s[4:]
    # Map suffix
    # Default unknown suffix goes to 5 to ensure it sorts after known terms
    order = term_order_map.get(suf, 5)
    return (year, order)

for col in ['TERM_CODE', 'EFFECTIVE_TERM_CODE']:
    yrs, ords = zip(*df[col].map(parse_term_code))
    df[f'{col}_YEAR'] = yrs
    df[f'{col}_ORD'] = ords

# Determine if the subject is newly introduced in this term: first effective term equals the offering term
# Some rows may have EFFECTIVE_TERM_CODE that is later than TERM_CODE if catalog updated mid-year; we consider new if exact match
is_new_mask = (
    (df['TERM_CODE_YEAR'] == df['EFFECTIVE_TERM_CODE_YEAR']) &
    (df['TERM_CODE_ORD'] == df['EFFECTIVE_TERM_CODE_ORD'])
)

# Count distinct subjects newly introduced per term
new_per_term = (
    df.loc[is_new_mask]
      .groupby(['ACADEMIC_YEAR', 'TERM_CODE'], as_index=False)
      .agg(new_subjects=('SUBJECT_ID', 'nunique'))
)

# Sort by academic year then by term order for display sequencing
term_sort_keys = (
    new_per_term['TERM_CODE'].map(lambda tc: parse_term_code(tc)[1])
)
new_per_term = new_per_term.assign(_term_ord=term_sort_keys).sort_values(['ACADEMIC_YEAR', '_term_ord']).drop(columns=['_term_ord'])

# Prepare display column for academic year where it only shows when different from previous
new_per_term = new_per_term.sort_values(['ACADEMIC_YEAR', 'TERM_CODE'])
new_per_term['display_academic_year'] = new_per_term['ACADEMIC_YEAR'].astype(str)
new_per_term.loc[new_per_term['ACADEMIC_YEAR'].astype(str).eq(new_per_term['ACADEMIC_YEAR'].astype(str).shift(1)), 'display_academic_year'] = ''

# Compute grand total across all years
grand_total = pd.DataFrame([
    {
        'display_academic_year': 'TOTAL',
        'TERM_CODE': '',
        'new_subjects': int(new_per_term['new_subjects'].sum())
    }
])

# Final result: list each row with display_academic_year, term code, and count, plus TOTAL row
answer = new_per_term[['display_academic_year', 'TERM_CODE', 'new_subjects']]
answer = pd.concat([answer, grand_total], ignore_index=True)

target = answer

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
