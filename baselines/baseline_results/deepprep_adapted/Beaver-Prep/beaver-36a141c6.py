import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TIP_MATERIAL_STATUS_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_MATERIAL_STATUS_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="subject_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["subject_id"] = table_1["subject_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        if s.lower() == 'nan' or s == '':
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        if s.lower() == 'nan' or s == '':
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_STATUS_KEY"] = table_1["TIP_MATERIAL_STATUS_KEY"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="RECORD_COUNT", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['RECORD_COUNT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['RECORD_COUNT']
    if _dtype == "datetime64":
        table_1['RECORD_COUNT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['RECORD_COUNT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['RECORD_COUNT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['RECORD_COUNT'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['subject_id', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['subject_id', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['subject_id', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['subject_id', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY'], keep='last').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ISBN", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ISBN'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ISBN']
    if _dtype == "datetime64":
        table_1['ISBN'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ISBN'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ISBN'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ISBN'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        return s if s != "" else None
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
    # import pandas as pd
    # def transform_func(s):
    #     # ISBN was cast to string earlier; normalize placeholders to null and trim
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        # ISBN was cast to string earlier; normalize placeholders to null and trim
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in {"nan", "none", "null", ""}:
            return None
        return s
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
    # Deduplicate(table_name="table_1", subset=['TIP_MATERIAL_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_MATERIAL_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_KEY', 'ISBN', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_KEY', 'ISBN', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="tip_material_status_key", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return s != "" and s.lower() != "nan"
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return s != "" and s.lower() != "nan"
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['tip_material_status_key'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="tip_material_status_key", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if v == "" or v.lower() == "nan":
    #         return None
    #     return v.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if v == "" or v.lower() == "nan":
            return None
        return v.upper()
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
    #     v = str(s).strip()
    #     if v == "" or v.lower() == "nan":
    #         return None
    #     return v.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if v == "" or v.lower() == "nan":
            return None
        return v.upper()
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
    #     v = str(s).strip()
    #     if v == "" or v.lower() == "nan":
    #         return None
    #     return v
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if v == "" or v.lower() == "nan":
            return None
        return v
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['tip_material_status_key'] is not None and row['TIP_MATERIAL_STATUS_CODE'] is not None
    # """)
    # Filter
    def filter_func(row):
        return row['tip_material_status_key'] is not None and row['TIP_MATERIAL_STATUS_CODE'] is not None
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="TIP_MATERIAL_STATUS", mode="mode")
    # MissingValueImputation
    table_1["TIP_MATERIAL_STATUS"] = table_1["TIP_MATERIAL_STATUS"].fillna(table_1["TIP_MATERIAL_STATUS"].mode().iloc[0])

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SCHOOL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SCHOOL_NAME"] = table_1["SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # trim and collapse internal whitespace, and standardize to uppercase for reliable matching
    #     return " ".join(str(s).strip().split()).upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # trim and collapse internal whitespace, and standardize to uppercase for reliable matching
        return " ".join(str(s).strip().split()).upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_CODE"] = table_1["SUBJECT_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # trim and collapse internal whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # trim and collapse internal whitespace
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['SUBJECT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'])
    # SelectCol
    _cols = [c for c in ['SUBJECT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['SUBJECT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['SUBJECT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME'], keep='first').reset_index(drop=True)

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
prepared_material_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_materials = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_material_status = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
prepared_subject_org = prepared_table_4

# Start from prepared tables
assign = prepared_material_assignments.copy()
mat = prepared_materials.copy()
status = prepared_material_status.copy()
org = prepared_subject_org.copy()

# Join assignments -> materials (for pricing)
assign_mat = assign.merge(mat, how='left', on='TIP_MATERIAL_KEY')

# Join assignments -> status (for status description/code)
assign_mat_stat = assign_mat.merge(status, how='left', left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key')

# Join to org via subject/subject_code (assumes compatible coding; coerce to string/strip for robustness)
assign_mat_stat['subject_id'] = assign_mat_stat['subject_id'].astype(str).str.strip()
org['SUBJECT_CODE'] = org['SUBJECT_CODE'].astype(str).str.strip()
joined = assign_mat_stat.merge(org, how='left', left_on='subject_id', right_on='SUBJECT_CODE')

# Define helper columns
# Treat material records as those with a non-null/non-empty TIP_MATERIAL_KEY excluding explicit 'Course has no materials' markers
invalid_keys = set([None, float('nan')])
joined['has_material'] = (~joined['TIP_MATERIAL_KEY'].astype(str).str.contains('Course has no materials', case=False, na=False)) & (joined['TIP_MATERIAL_KEY'].astype(str).str.strip() != '')

# Numeric cast for prices
for c in ['NEW_SHELF_PRICE','USED_SHELF_PRICE']:
    joined[c] = pd.to_numeric(joined[c], errors='coerce')

# Group by department and school
grp_cols = ['DEPARTMENT_NAME','SCHOOL_NAME']

# Unique material count: count distinct TIP_MATERIAL_KEY among rows with has_material
def agg_frame(df):
    df_mat = df[df['has_material']]
    out = {
        'unique_course_materials': df_mat['TIP_MATERIAL_KEY'].nunique(dropna=True),
        'number_of_courses': df['subject_id'].nunique(dropna=True),
        'avg_new_shelf_price': df_mat['NEW_SHELF_PRICE'].mean(skipna=True),
        'avg_used_shelf_price': df_mat['USED_SHELF_PRICE'].mean(skipna=True),
        'total_material_records': int(df_mat.shape[0]),
        'distinct_material_statuses': df['TIP_MATERIAL_STATUS_KEY'].nunique(dropna=True)
    }
    return pd.Series(out)

by_org = joined.groupby(grp_cols, dropna=False).apply(agg_frame).reset_index()

# Grand total across all schools and departments: null dept/school
grand = agg_frame(joined).to_frame().T
grand['DEPARTMENT_NAME'] = pd.NA
grand['SCHOOL_NAME'] = pd.NA

# Reorder columns
cols = ['DEPARTMENT_NAME','SCHOOL_NAME','unique_course_materials','number_of_courses','avg_new_shelf_price','avg_used_shelf_price','total_material_records','distinct_material_statuses']
result = pd.concat([by_org[cols], grand[cols]], ignore_index=True)

target = result

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
