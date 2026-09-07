import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
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
    table_1["TIP_SUBJECT_OFFERED_KEY"] = table_1["TIP_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
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
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
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
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
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
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
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
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 10 ----------------
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
    # CastType(table_name="table_1", column="TIP_SUBJECT_OFFERED_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TIP_SUBJECT_OFFERED_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TIP_SUBJECT_OFFERED_KEY']
    if _dtype == "datetime64":
        table_1['TIP_SUBJECT_OFFERED_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TIP_SUBJECT_OFFERED_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TIP_SUBJECT_OFFERED_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TIP_SUBJECT_OFFERED_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if v.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return v
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        v = str(s).strip()
        if v.lower() in {"nan", "none", "null", ""}:
            return None
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_SUBJECT_OFFERED_KEY"] = table_1["TIP_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if v.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return v
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        v = str(s).strip()
        if v.lower() in {"nan", "none", "null", ""}:
            return None
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if v.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return v
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        v = str(s).strip()
        if v.lower() in {"nan", "none", "null", ""}:
            return None
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["subject_id"] = table_1["subject_id"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if v.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     # treat explicit non-material placeholder as missing for linkage to price details
    #     if v.lower().startswith("n/acourse has no materials"):
    #         return None
    #     return v
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        v = str(s).strip()
        if v.lower() in {"nan", "none", "null", ""}:
            return None
        # treat explicit non-material placeholder as missing for linkage to price details
        if v.lower().startswith("n/acourse has no materials"):
            return None
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 10 ----------------
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
    # Deduplicate(table_name="table_1", subset=['TIP_MATERIAL_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_MATERIAL_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TIP_MATERIAL_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_MATERIAL_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="RENTAL_NEW_PRICE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['RENTAL_NEW_PRICE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['RENTAL_NEW_PRICE']
    if _dtype == "datetime64":
        table_1['RENTAL_NEW_PRICE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['RENTAL_NEW_PRICE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['RENTAL_NEW_PRICE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['RENTAL_NEW_PRICE'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="RENTAL_NEW_PRICE", mode="median")
    # MissingValueImputation
    table_1["RENTAL_NEW_PRICE"] = table_1["RENTAL_NEW_PRICE"].fillna(table_1["RENTAL_NEW_PRICE"].median())

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_KEY', 'RENTAL_NEW_PRICE'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_KEY', 'RENTAL_NEW_PRICE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
subjects_by_dept = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
subject_material_links = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
material_prices = prepared_table_3

# Merge subjects with material links on TIP_SUBJECT_OFFERED_KEY (restrict to matching TERM_CODE where available)
links = subject_material_links
subs = subjects_by_dept
# If TERM_CODE exists on both, enforce equality to avoid cross-term bleed
merged_sl = subs.merge(links, on='TIP_SUBJECT_OFFERED_KEY', how='left', suffixes=('', '_lk'))
if 'TERM_CODE_lk' in merged_sl.columns:
    # In case merge created TERM_CODE_lk from links; filter rows where terms match or links missing
    term_match = (merged_sl['TERM_CODE_lk'].isna()) | (merged_sl['TERM_CODE'] == merged_sl['TERM_CODE_lk'])
    merged_sl = merged_sl.loc[term_match].drop(columns=[c for c in ['TERM_CODE_lk'] if c in merged_sl.columns])

# Bring in rental new prices
merged_full = merged_sl.merge(material_prices, on='TIP_MATERIAL_KEY', how='left')

# Clean numeric types
subs_cols = ['NUM_ENROLLED_STUDENTS']
for c in subs_cols:
    if c in merged_full.columns:
        merged_full[c] = pd.to_numeric(merged_full[c], errors='coerce')
merged_full['RENTAL_NEW_PRICE'] = pd.to_numeric(merged_full['RENTAL_NEW_PRICE'], errors='coerce')

# Compute per-department aggregates
# - department name
# - total number of types of TIP subjects (distinct SUBJECT_ID)
# - total enrolled students (sum NUM_ENROLLED_STUDENTS across offerings; then group by dept)
# - min/max rental new price (ignoring NaN/zero-only if desired; here include non-null values)

# Distinct subjects per department
distinct_subjects = merged_full[['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'SUBJECT_ID']].drop_duplicates()
subjects_count = distinct_subjects.groupby(['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], as_index=False).agg(total_tip_subject_types=('SUBJECT_ID', 'nunique'))

# Total enrolled students per department (from subject offerings)
enrollment = subs.groupby(['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], as_index=False)['NUM_ENROLLED_STUDENTS'].sum().rename(columns={'NUM_ENROLLED_STUDENTS':'total_enrolled_students'})

# Min/max rental new price per department (from materials joined to subjects)
price_agg = merged_full[['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RENTAL_NEW_PRICE']].dropna()
price_agg = price_agg.groupby(['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], as_index=False).agg(
    min_rental_new_price=('RENTAL_NEW_PRICE','min'),
    max_rental_new_price=('RENTAL_NEW_PRICE','max')
)

# Combine all
result = subjects_count.merge(enrollment, on=['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], how='outer')\
                     .merge(price_agg, on=['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], how='left')

# Final select and rename for clarity
answer = result.rename(columns={'OFFER_DEPT_NAME':'department_name'})[
    ['department_name', 'total_tip_subject_types', 'total_enrolled_students', 'min_rental_new_price', 'max_rental_new_price']
]

answer = answer.sort_values('department_name').reset_index(drop=True)

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
