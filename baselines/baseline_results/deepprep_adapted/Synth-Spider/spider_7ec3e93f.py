import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="student_address_extracted", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    #     idx_col = df.columns[0]
    # 
    #     # transpose to records
    #     t = df.set_index(idx_col).T
    # 
    #     # defensively coerce types
    #     t['student_id'] = pd.to_numeric(t.get('student_id'), errors='coerce')
    #     t['address_type_code'] = t.get('address_type_code').astype(str)
    # 
    #     return t.reset_index(drop=True)[['student_id', 'address_type_code']]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()
        idx_col = df.columns[0]

        # transpose to records
        t = df.set_index(idx_col).T

        # defensively coerce types
        t['student_id'] = pd.to_numeric(t.get('student_id'), errors='coerce')
        t['address_type_code'] = t.get('address_type_code').astype(str)

        return t.reset_index(drop=True)[['student_id', 'address_type_code']]
    student_address_extracted = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="student_address_extracted", column_name="address_type_code", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    student_address_extracted["address_type_code"] = student_address_extracted["address_type_code"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="student_address_extracted", column="student_id", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = student_address_extracted['student_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = student_address_extracted['student_id']
    if _dtype == "datetime64":
        student_address_extracted['student_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        student_address_extracted['student_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        student_address_extracted['student_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        student_address_extracted['student_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="student_address_extracted", subset=['student_id', 'address_type_code'], how="any")
    # DropNulls
    student_address_extracted = student_address_extracted.dropna(subset=['student_id', 'address_type_code'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="student_address_extracted", columns=['student_id', 'address_type_code'])
    # SelectCol
    _cols = [c for c in ['student_id', 'address_type_code'] if c in student_address_extracted.columns]
    student_address_extracted = student_address_extracted[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['student_address_extracted'])
    # Terminate
    result = {'student_address_extracted': student_address_extracted}
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
    # DropNulls(table_name="table_1", subset=['address_type_code'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['address_type_code'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="address_type_description", func="""
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
    table_1["address_type_description"] = table_1["address_type_description"].apply(_std_apply)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_student_addresses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_address_types = prepared_table_2

# prepared_student_addresses construction from table_1 (pivot-like source)
# Assume df1 is table_1 with first column as row header names and remaining columns as student-specific values.
row_names = df1.iloc[:, 0]
value_cols = df1.columns[1:]
long = (
    df1.iloc[:, 1:]
      .copy()
      .assign(_row=row_names.values)
      .melt(id_vars=['_row'], var_name='col', value_name='val')
)
# Keep only rows where _row identifies the fields we need and val is non-null
student_ids = long[long['_row'].eq('student_id')][['col', 'val']].rename(columns={'val': 'student_id'})
addr_types = long[long['_row'].eq('address_type_code')][['col', 'val']].rename(columns={'val': 'address_type_code'})
prepared_student_addresses = (
    student_ids.merge(addr_types, on='col', how='inner')
               .drop(columns=['col'])
)

# prepared_address_types from table_2
prepared_address_types = df2.copy()
prepared_address_types['address_type_description'] = prepared_address_types['address_type_description'].astype(str).str.strip()

# Integrate to compute most common address type
joined = prepared_student_addresses.merge(
    prepared_address_types,
    on='address_type_code',
    how='left'
)
counts = joined.groupby(['address_type_code', 'address_type_description'], dropna=False).size().reset_index(name='n')
# Select the most common (break ties by code lexicographically for determinism)
answer = counts.sort_values(['n', 'address_type_code'], ascending=[False, True]).head(1)
# answer has columns: address_type_code, address_type_description, n

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
