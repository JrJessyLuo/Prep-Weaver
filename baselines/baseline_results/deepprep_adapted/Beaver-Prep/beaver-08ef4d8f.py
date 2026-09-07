import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TIP_MATERIAL_STATUS_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TIP_MATERIAL_STATUS_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TIP_MATERIAL_STATUS_KEY']
    if _dtype == "datetime64":
        table_1['TIP_MATERIAL_STATUS_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TIP_MATERIAL_STATUS_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TIP_MATERIAL_STATUS_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TIP_MATERIAL_STATUS_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN', 'RECORD_COUNT'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    # StandardizeString(table_name="table_1", column_name="COURSE_NUMBER", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["COURSE_NUMBER"] = table_1["COURSE_NUMBER"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_SCHOOL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["OFFER_SCHOOL_NAME"] = table_1["OFFER_SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_SUBJECT_OFFERED_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_SCHOOL_NAME'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # keep only non-negative prices and non-null key
    #     if pd.isna(row.get(\"TIP_MATERIAL_KEY\")):
    #         return False
    #     n = row.get(\"NEW_SHELF_PRICE\")
    #     u = row.get(\"USED_SHELF_PRICE\")
    #     if pd.notna(n) and n < 0:
    #         return False
    #     if pd.notna(u) and u < 0:
    #         return False
    #     return True
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # keep only non-negative prices and non-null key
        if pd.isna(row.get(\"TIP_MATERIAL_KEY\")):
            return False
        n = row.get(\"NEW_SHELF_PRICE\")
        u = row.get(\"USED_SHELF_PRICE\")
        if pd.notna(n) and n < 0:
            return False
        if pd.notna(u) and u < 0:
            return False
        return True
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ISBN", func="""
    # import re
    # def transform_func(s: str):
    #     # keep only digits/X (ISBN-10 may end with X), remove hyphens/spaces, treat empty as null-like
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     s = re.sub(r'[^0-9Xx]', '', s)
    #     s = s.upper()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        # keep only digits/X (ISBN-10 may end with X), remove hyphens/spaces, treat empty as null-like
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        s = re.sub(r'[^0-9Xx]', '', s)
        s = s.upper()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ISBN"] = table_1["ISBN"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NEW_SHELF_PRICE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NEW_SHELF_PRICE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NEW_SHELF_PRICE']
    if _dtype == "datetime64":
        table_1['NEW_SHELF_PRICE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NEW_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NEW_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NEW_SHELF_PRICE'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="USED_SHELF_PRICE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['USED_SHELF_PRICE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['USED_SHELF_PRICE']
    if _dtype == "datetime64":
        table_1['USED_SHELF_PRICE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['USED_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['USED_SHELF_PRICE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['USED_SHELF_PRICE'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_KEY', 'ISBN', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_KEY', 'ISBN', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_MATERIAL_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_MATERIAL_KEY'], keep='last').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="tip_material_status_key", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['tip_material_status_key'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['tip_material_status_key']
    if _dtype == "datetime64":
        table_1['tip_material_status_key'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['tip_material_status_key'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['tip_material_status_key'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['tip_material_status_key'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="tip_material_status_key", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return s2 if s2 != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return s2 if s2 != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["tip_material_status_key"] = table_1["tip_material_status_key"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return s2 if s2 != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return s2 if s2 != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_STATUS_CODE"] = table_1["TIP_MATERIAL_STATUS_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return s2 if s2 != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return s2 if s2 != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_STATUS"] = table_1["TIP_MATERIAL_STATUS"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="TIP_MATERIAL_STATUS_filled", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     val = row.get('TIP_MATERIAL_STATUS', None)
    #     if val is None or (isinstance(val, float) and pd.isna(val)):
    #         return "Unknown"
    #     sval = str(val).strip()
    #     return sval if sval != "" else "Unknown"
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        val = row.get('TIP_MATERIAL_STATUS', None)
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return "Unknown"
        sval = str(val).strip()
        return sval if sval != "" else "Unknown"
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["TIP_MATERIAL_STATUS_filled"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['TIP_MATERIAL_STATUS', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['TIP_MATERIAL_STATUS', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 8 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'TIP_MATERIAL_STATUS_filled', 'new_name': 'TIP_MATERIAL_STATUS'}])
    # Rename
    table_1 = table_1.rename(columns={'TIP_MATERIAL_STATUS_filled': 'TIP_MATERIAL_STATUS'})

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subject_material_facts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_materials = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_material_status = prepared_table_4

# Merge facts with subject offerings
m1 = prepared_subject_material_facts.merge(
    prepared_subject_offerings,
    on=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE'],
    how='left'
)

# Merge facts with materials for pricing
m2 = m1.merge(
    prepared_materials,
    on='TIP_MATERIAL_KEY',
    how='left'
)

# Decode material status
m3 = m2.merge(
    prepared_material_status,
    left_on='TIP_MATERIAL_STATUS_KEY',
    right_on='tip_material_status_key',
    how='left'
)

# Ensure numeric types for aggregation
for col in ['NEW_SHELF_PRICE','USED_SHELF_PRICE']:
    m3[col] = pd.to_numeric(m3[col], errors='coerce')

# Define group keys: TIP subject (by SUBJECT_ID/TITLE) and material status
group_cols = ['COURSE_NUMBER','SUBJECT_TITLE','TIP_MATERIAL_STATUS']

agg_df = m3.groupby(group_cols).agg(
    total_new_shelf_price = ('NEW_SHELF_PRICE','sum'),
    min_new_shelf_price   = ('NEW_SHELF_PRICE','min'),
    max_new_shelf_price   = ('NEW_SHELF_PRICE','max'),
    total_used_shelf_price= ('USED_SHELF_PRICE','sum'),
    min_used_shelf_price  = ('USED_SHELF_PRICE','min'),
    max_used_shelf_price  = ('USED_SHELF_PRICE','max'),
    total_materials       = ('TIP_MATERIAL_KEY','nunique'),
    total_schools         = ('OFFER_SCHOOL_NAME','nunique')
).reset_index()

# Final result per TIP subject and material status with requested fields
target = agg_df[['COURSE_NUMBER','SUBJECT_TITLE','TIP_MATERIAL_STATUS',
                 'total_new_shelf_price','min_new_shelf_price','max_new_shelf_price',
                 'total_used_shelf_price','min_used_shelf_price','max_used_shelf_price',
                 'total_schools','total_materials']]

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
