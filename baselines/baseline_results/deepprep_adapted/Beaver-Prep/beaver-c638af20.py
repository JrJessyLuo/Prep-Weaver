import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # OutlierDetection(table_name="table_1", column_name="RECORD_COUNT", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['RECORD_COUNT'].quantile(0.25)
    _q3 = table_1['RECORD_COUNT'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_RECORD_COUNT_is_outlier'] = table_1['RECORD_COUNT'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_RECORD_COUNT_is_outlier'] == False]
        table_1.drop(columns=['table_1_RECORD_COUNT_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_RECORD_COUNT_is_outlier'] = table_1['table_1_RECORD_COUNT_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # DropColumn(table_name="table_1", drop_columns=['WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
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
    # ErrorDetection(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def is_valid_dept_name(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_dept_name(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_dept_name(val))
        except Exception:
            return False
    table_1 = table_1[table_1['OFFER_DEPT_NAME'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
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
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
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
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
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
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
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
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
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
    # DropNulls(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_MATERIAL_STATUS_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_MATERIAL_STATUS_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_MATERIAL_STATUS_KEY'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_MATERIAL_STATUS_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_MATERIAL_STATUS_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'LIBRARY_MATERIAL_STATUS_KEY'], keep='first').reset_index(drop=True)

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
def _prep_5(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="library_material_status_dim", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Fill missing readable status names using a deterministic mapping by key/code
    #     mapping = {
    #         "R": "Required Course Material"
    #     }
    # 
    #     # Normalize nulls and fill
    #     df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].replace({pd.NA: None})
    #     df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].fillna(df["LIBRARY_MATERIAL_STATUS_KEY"].map(mapping))
    #     df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].fillna(df["LIBRARY_MATERIAL_STATUS_CODE"].map(mapping))
    # 
    #     # Keep only columns required by downstream integration
    #     return df[["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS_CODE", "LIBRARY_MATERIAL_STATUS"]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Fill missing readable status names using a deterministic mapping by key/code
        mapping = {
            "R": "Required Course Material"
        }

        # Normalize nulls and fill
        df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].replace({pd.NA: None})
        df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].fillna(df["LIBRARY_MATERIAL_STATUS_KEY"].map(mapping))
        df["LIBRARY_MATERIAL_STATUS"] = df["LIBRARY_MATERIAL_STATUS"].fillna(df["LIBRARY_MATERIAL_STATUS_CODE"].map(mapping))

        # Keep only columns required by downstream integration
        return df[["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS_CODE", "LIBRARY_MATERIAL_STATUS"]]
    library_material_status_dim = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="library_material_status_dim", subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep="last")
    # Deduplicate
    library_material_status_dim = library_material_status_dim.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="library_material_status_dim", subset=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'LIBRARY_MATERIAL_STATUS'], how="any")
    # DropNulls
    library_material_status_dim = library_material_status_dim.dropna(subset=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'LIBRARY_MATERIAL_STATUS'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['library_material_status_dim'])
    # Terminate
    result = {'library_material_status_dim': library_material_status_dim}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_6(table_1):
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_tip_materials = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_tip_status_dim = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_offerings = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_library_materials = prepared_table_4
prepared_table_5 = _prep_5(tables['table_3'])
prepared_library_status_dim = prepared_table_5
prepared_table_6 = _prep_6(tables['table_7'])

## Assumes the prepared_* DataFrames are already materialized as per table_targets.
# Join TIP to offerings to get department
_tip = prepared_tip_materials.merge(prepared_offerings[['TIP_SUBJECT_OFFERED_KEY','OFFER_DEPT_NAME']], on='TIP_SUBJECT_OFFERED_KEY', how='left')
# Attach readable TIP status
_tip = _tip.merge(prepared_tip_status_dim[['tip_material_status_key','TIP_MATERIAL_STATUS']], left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key', how='left')
_tip['material_status'] = _tip['TIP_MATERIAL_STATUS_KEY']
# Count TIP materials per department and status (RECORD_COUNT treated as weight if present numeric)
if 'RECORD_COUNT' in _tip.columns and _tip['RECORD_COUNT'].notna().all():
    _tip_counts = _tip.groupby(['OFFER_DEPT_NAME','material_status'], dropna=False)['RECORD_COUNT'].sum().reset_index(name='tip_count')
else:
    _tip_counts = _tip.groupby(['OFFER_DEPT_NAME','material_status'], dropna=False).size().reset_index(name='tip_count')

# Join Library to offerings to get department (via subject offered key)
_lib = prepared_library_materials.merge(prepared_offerings[['TIP_SUBJECT_OFFERED_KEY','OFFER_DEPT_NAME']], left_on='LIBRARY_SUBJECT_OFFERED_KEY', right_on='TIP_SUBJECT_OFFERED_KEY', how='left')
# Attach readable Library status
_lib = _lib.merge(prepared_library_status_dim[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']], on='LIBRARY_MATERIAL_STATUS_KEY', how='left')
_lib['material_status'] = _lib['LIBRARY_MATERIAL_STATUS_KEY']
# Count Library materials per department and status
_lib_counts = _lib.groupby(['OFFER_DEPT_NAME','material_status'], dropna=False).size().reset_index(name='library_count')

# Combine TIP and Library counts by department and material status
_counts = merge(_tip_counts, _lib_counts, on=['OFFER_DEPT_NAME','material_status'], how='outer').fillna(0)
_counts['tip_count'] = _counts['tip_count'].astype(int)
_counts['library_count'] = _counts['library_count'].astype(int)
_counts['total_count'] = _counts['tip_count'] + _counts['library_count']
_counts = _counts.rename(columns={'OFFER_DEPT_NAME':'department_name'})

# Build subtotals per department
_dept_subtotals = _counts.groupby('department_name', dropna=False)[['tip_count','library_count','total_count']].sum().reset_index()
_dept_subtotals.insert(1, 'material_status', 'Subtotal')

# Grand total across all departments
_grand_total = _counts[['tip_count','library_count','total_count']].sum().to_frame().T
_grand_total.insert(0, 'department_name', 'Grand Total')
_grand_total.insert(1, 'material_status', '')

# Final result: detail rows + department subtotals + grand total
result = (
    _counts[['department_name','material_status','tip_count','library_count','total_count']]
    .sort_values(['department_name','material_status'])
)
result = (
    pandas.concat([result, _dept_subtotals[['department_name','material_status','tip_count','library_count','total_count']], _grand_total[['department_name','material_status','tip_count','library_count','total_count']]], ignore_index=True)
)

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
