import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize common null tokens
    #     if s.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize common null tokens
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
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     if s.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
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
    table_1["TIP_MATERIAL_STATUS_KEY"] = table_1["TIP_MATERIAL_STATUS_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
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
    # CastType(table_name="table_1", column="TIP_MATERIAL_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TIP_MATERIAL_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TIP_MATERIAL_KEY']
    if _dtype == "datetime64":
        table_1['TIP_MATERIAL_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TIP_MATERIAL_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TIP_MATERIAL_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TIP_MATERIAL_KEY'] = _series.astype(str)

    # ---------------- Step 7 ----------------
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

    # ---------------- Step 8 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY'], agg=[{'column': 'RECORD_COUNT', 'agg_func': 'sum'}])
    # GroupBy
    table_1 = table_1.groupby(['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY'], as_index=False).agg({'RECORD_COUNT': 'sum'})

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="tip_material_status_key", func="""
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
    table_1["tip_material_status_key"] = table_1["tip_material_status_key"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS_CODE", func="""
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
    table_1["TIP_MATERIAL_STATUS_CODE"] = table_1["TIP_MATERIAL_STATUS_CODE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS", func="""
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
    table_1["TIP_MATERIAL_STATUS"] = table_1["TIP_MATERIAL_STATUS"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="material_status_dim", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Treat empty/whitespace-only strings as missing
    #     for c in ["tip_material_status_key", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]:
    #         df[c] = df[c].replace(r"^\s*$", np.nan, regex=True)
    # 
    #     # If human-readable status is missing, fall back to code (better than leaving null)
    #     df["TIP_MATERIAL_STATUS"] = df["TIP_MATERIAL_STATUS"].fillna(df["TIP_MATERIAL_STATUS_CODE"])
    # 
    #     # Keep only required columns
    #     df = df[["tip_material_status_key", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]]
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Treat empty/whitespace-only strings as missing
        for c in ["tip_material_status_key", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]:
            df[c] = df[c].replace(r"^\s*$", np.nan, regex=True)

        # If human-readable status is missing, fall back to code (better than leaving null)
        df["TIP_MATERIAL_STATUS"] = df["TIP_MATERIAL_STATUS"].fillna(df["TIP_MATERIAL_STATUS_CODE"])

        # Keep only required columns
        df = df[["tip_material_status_key", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]]
        return df
    material_status_dim = process_tables(table_1)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="material_status_dim", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], how="any")
    # DropNulls
    material_status_dim = material_status_dim.dropna(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="material_status_dim", subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'], keep="first")
    # Deduplicate
    material_status_dim = material_status_dim.drop_duplicates(subset=['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS'], keep='first').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Terminate(result=['material_status_dim'])
    # Terminate
    result = {'material_status_dim': material_status_dim}
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
    # MissingValueImputation(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", mode="median")
    # MissingValueImputation
    table_1["NUM_ENROLLED_STUDENTS"] = table_1["NUM_ENROLLED_STUDENTS"].fillna(table_1["NUM_ENROLLED_STUDENTS"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'NUM_ENROLLED_STUDENTS'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'NUM_ENROLLED_STUDENTS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

prepared_table_1 = _prep_1(tables['table_1'])
prep_material_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prep_material_status_dim = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prep_enrollment = prepared_table_3

# Assume prepared tables exist: prep_material_assignments, prep_material_status_dim, prep_enrollment

# Join material assignments to status dim for label
assign_with_status = prep_material_assignments.merge(
    prep_material_status_dim,
    how='left',
    left_on='TIP_MATERIAL_STATUS_KEY',
    right_on='tip_material_status_key'
)

# Normalize status label: treat null/blank as 'No material status'
status_label = assign_with_status['TIP_MATERIAL_STATUS'].where(
    assign_with_status['TIP_MATERIAL_STATUS'].notna() & (assign_with_status['TIP_MATERIAL_STATUS'].astype(str).str.strip() != ''),
    'No material status'
)
assign_with_status['material_status_label'] = status_label

# Join to enrollment by subject offering and term
assign_with_enroll = assign_with_status.merge(
    prep_enrollment,
    how='left',
    on=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE']
)

# Coerce numeric fields
assign_with_enroll['RECORD_COUNT'] = pd.to_numeric(assign_with_enroll['RECORD_COUNT'], errors='coerce').fillna(0)
assign_with_enroll['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(assign_with_enroll['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0)

# Aggregate per material status label
per_status = assign_with_enroll.groupby('material_status_label').agg(
    total_unique_materials=('TIP_MATERIAL_KEY', lambda s: s.astype(str).nunique()),
    total_records=('RECORD_COUNT', 'sum'),
    total_student_enrollment=('NUM_ENROLLED_STUDENTS', 'sum')
).reset_index()

# Grand total row across all statuses
grand = pd.DataFrame({
    'material_status_label': ['Grand Total'],
    'total_unique_materials': [assign_with_enroll['TIP_MATERIAL_KEY'].astype(str).nunique()],
    'total_records': [assign_with_enroll['RECORD_COUNT'].sum()],
    'total_student_enrollment': [assign_with_enroll['NUM_ENROLLED_STUDENTS'].sum()]
})

# Combine
result = pd.concat([per_status, grand], ignore_index=True)

# Final output
target = result[['material_status_label', 'total_unique_materials', 'total_records', 'total_student_enrollment']]

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
