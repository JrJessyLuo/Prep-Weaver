import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="LIBRARY_RESERVE_CATALOG_KEY", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['LIBRARY_RESERVE_CATALOG_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['LIBRARY_RESERVE_CATALOG_KEY']
    if _dtype == "datetime64":
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['LIBRARY_RESERVE_CATALOG_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'SUBJECT_ID', 'TERM_CODE'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'SUBJECT_ID', 'TERM_CODE'] if c in table_1.columns]
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
    # DropColumn(table_name="table_1", drop_columns=['CATALOG_AUTHOR_NAME', 'CATALOG_PUBLISHER', 'CATALOG_CALL_NUMBER', 'CATALOG_ISBN', 'CATALOG_SYSTEM_NUMBER', 'CATALOG_RECORD_CREATE_DATE', 'CATALOG_RECORD_UPDATE_DATE', 'RECORD_COUNTER', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['CATALOG_AUTHOR_NAME', 'CATALOG_PUBLISHER', 'CATALOG_CALL_NUMBER', 'CATALOG_ISBN', 'CATALOG_SYSTEM_NUMBER', 'CATALOG_RECORD_CREATE_DATE', 'CATALOG_RECORD_UPDATE_DATE', 'RECORD_COUNTER', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_catalog", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Clean title: keep nulls, strip whitespace, remove wrapping quotes if present
    #     def clean_title(x):
    #         if pd.isna(x):
    #             return pd.NA
    #         s = str(x).strip()
    #         if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #             s = s[1:-1].strip()
    #         return s
    # 
    #     df["CATALOG_TITLE"] = df["CATALOG_TITLE"].apply(clean_title)
    # 
    #     # Treat year=0 as missing
    #     df["CATALOG_YEAR"] = pd.to_numeric(df["CATALOG_YEAR"], errors="coerce")
    #     df.loc[df["CATALOG_YEAR"] == 0, "CATALOG_YEAR"] = pd.NA
    #     df["CATALOG_YEAR"] = df["CATALOG_YEAR"].astype("Int64")
    # 
    #     return df[["library_reserve_catalog_key", "CATALOG_TITLE", "CATALOG_YEAR"]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Clean title: keep nulls, strip whitespace, remove wrapping quotes if present
        def clean_title(x):
            if pd.isna(x):
                return pd.NA
            s = str(x).strip()
            if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
                s = s[1:-1].strip()
            return s

        df["CATALOG_TITLE"] = df["CATALOG_TITLE"].apply(clean_title)

        # Treat year=0 as missing
        df["CATALOG_YEAR"] = pd.to_numeric(df["CATALOG_YEAR"], errors="coerce")
        df.loc[df["CATALOG_YEAR"] == 0, "CATALOG_YEAR"] = pd.NA
        df["CATALOG_YEAR"] = df["CATALOG_YEAR"].astype("Int64")

        return df[["library_reserve_catalog_key", "CATALOG_TITLE", "CATALOG_YEAR"]]
    prepared_catalog = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['prepared_catalog'])
    # Terminate
    result = {'prepared_catalog': prepared_catalog}
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
    # StandardizeString(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return None if s.lower() in {"nan", "none", ""} else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return None if s.lower() in {"nan", "none", ""} else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_MATERIAL_STATUS"] = table_1["LIBRARY_MATERIAL_STATUS"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS", mode="mode")
    # MissingValueImputation
    table_1["LIBRARY_MATERIAL_STATUS"] = table_1["LIBRARY_MATERIAL_STATUS"].fillna(table_1["LIBRARY_MATERIAL_STATUS"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_reserve_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_catalog = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_status_dim = prepared_table_3

# Assume prepared_reserve_assignments, prepared_catalog, prepared_status_dim are dataframes created per targets
# 1) Join reserves to catalog on catalog key
joined = prepared_reserve_assignments.merge(
    prepared_catalog,
    left_on='LIBRARY_RESERVE_CATALOG_KEY',
    right_on='library_reserve_catalog_key',
    how='inner'
)

# 2) Optionally join status descriptions (not required for counts but keeps evidence available)
joined = joined.merge(
    prepared_status_dim,
    on='LIBRARY_MATERIAL_STATUS_KEY',
    how='left'
)

# 3) Prepare features
# Compute title length (treat missing as empty string)
joined['title_len'] = joined['CATALOG_TITLE'].fillna('').astype(str).str.len()

# Normalize year: keep as integer where > 0; drop 0 or null years for grouping if considered unknown
# If 0 represents unknown, exclude from year-based aggregation
joined['CATALOG_YEAR'] = pd.to_numeric(joined['CATALOG_YEAR'], errors='coerce')
joined_valid = joined[joined['CATALOG_YEAR'].notna() & (joined['CATALOG_YEAR'] > 0)]

# 4) Derive a course identifier to count distinct courses; SUBJECT_ID alone may represent a course, optionally include TERM_CODE if courses are term-specific
joined_valid['course_id'] = joined_valid['SUBJECT_ID']

# 5) Aggregate by publication year
agg = joined_valid.groupby('CATALOG_YEAR').agg(
    total_reserved=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    avg_title_length=('title_len', 'mean'),
    distinct_status=('LIBRARY_MATERIAL_STATUS_KEY', 'nunique'),
    num_courses=('course_id', 'nunique')
).reset_index()

# 6) Sort by year descending and select columns
result = agg.sort_values('CATALOG_YEAR', ascending=False)
result = result.rename(columns={'CATALOG_YEAR': 'publication_year'})

# Final output dataframe: columns [publication_year, total_reserved, avg_title_length, distinct_status, num_courses]
output = result[['publication_year', 'total_reserved', 'avg_title_length', 'distinct_status', 'num_courses']]

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
