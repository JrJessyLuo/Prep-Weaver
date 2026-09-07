import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['LIBRARY_COURSE_INSTRUCTOR_KEY'] is not None and row['LIBRARY_RESERVE_CATALOG_KEY'] is not None and row['LIBRARY_MATERIAL_STATUS_KEY'] is not None
    # """)
    # Filter
    def filter_func(row):
        return row['LIBRARY_COURSE_INSTRUCTOR_KEY'] is not None and row['LIBRARY_RESERVE_CATALOG_KEY'] is not None and row['LIBRARY_MATERIAL_STATUS_KEY'] is not None
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY'], keep='first').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="COURSE_NAME", mode="mode")
    # MissingValueImputation
    table_1["COURSE_NAME"] = table_1["COURSE_NAME"].fillna(table_1["COURSE_NAME"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_COURSE_INSTRUCTOR_KEY", func="""
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
    table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"] = table_1["LIBRARY_COURSE_INSTRUCTOR_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE_NAME", func="""
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
    table_1["COURSE_NAME"] = table_1["COURSE_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME'] if c in table_1.columns]
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
    # MissingValueImputation(table_name="table_1", column_name="CATALOG_YEAR", mode="mean")
    # MissingValueImputation
    table_1["CATALOG_YEAR"] = table_1["CATALOG_YEAR"].fillna(table_1["CATALOG_YEAR"].mean())

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_catalog", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Keep only required columns
    #     df = df[['library_reserve_catalog_key', 'CATALOG_YEAR']].copy()
    # 
    #     # Normalize year to numeric; treat 0 as missing
    #     df['CATALOG_YEAR'] = pd.to_numeric(df['CATALOG_YEAR'], errors='coerce')
    #     df.loc[df['CATALOG_YEAR'] == 0, 'CATALOG_YEAR'] = np.nan
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Keep only required columns
        df = df[['library_reserve_catalog_key', 'CATALOG_YEAR']].copy()

        # Normalize year to numeric; treat 0 as missing
        df['CATALOG_YEAR'] = pd.to_numeric(df['CATALOG_YEAR'], errors='coerce')
        df.loc[df['CATALOG_YEAR'] == 0, 'CATALOG_YEAR'] = np.nan

        return df
    prepared_catalog = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="prepared_catalog", column_name="CATALOG_YEAR", mode="median")
    # MissingValueImputation
    prepared_catalog["CATALOG_YEAR"] = prepared_catalog["CATALOG_YEAR"].fillna(prepared_catalog["CATALOG_YEAR"].median())

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="prepared_catalog", column="CATALOG_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_catalog['CATALOG_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_catalog['CATALOG_YEAR']
    if _dtype == "datetime64":
        prepared_catalog['CATALOG_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_catalog['CATALOG_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_catalog['CATALOG_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_catalog['CATALOG_YEAR'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="prepared_catalog", subset=['library_reserve_catalog_key'], keep="last")
    # Deduplicate
    prepared_catalog = prepared_catalog.drop_duplicates(subset=['library_reserve_catalog_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_MATERIAL_STATUS_KEY"] = table_1["LIBRARY_MATERIAL_STATUS_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="LIBRARY_MATERIAL_STATUS", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["nan", "none", "null", ""]):
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["nan", "none", "null", ""]):
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["LIBRARY_MATERIAL_STATUS"] = table_1["LIBRARY_MATERIAL_STATUS"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="LIBRARY_MATERIAL_STATUS_CLEAN", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     # Prefer existing non-null text
    #     val = row.get("LIBRARY_MATERIAL_STATUS", None)
    #     if val is not None and not (isinstance(val, float) and pd.isna(val)):
    #         sval = str(val).strip()
    #         if sval and sval.lower() not in ["nan", "none", "null"]:
    #             return sval
    # 
    #     # Otherwise, derive from key (lookup rules)
    #     key = row.get("LIBRARY_MATERIAL_STATUS_KEY", None)
    #     key = None if key is None else str(key).strip().upper()
    # 
    #     mapping = {
    #         "U": "Unknown",
    #         "R": "Required Course Material",
    #         "N": "Non-Required Course Material",
    #         "O": "Reserve only",
    #         "X": "No Required Textbook"
    #     }
    #     return mapping.get(key, "Unknown")
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        # Prefer existing non-null text
        val = row.get("LIBRARY_MATERIAL_STATUS", None)
        if val is not None and not (isinstance(val, float) and pd.isna(val)):
            sval = str(val).strip()
            if sval and sval.lower() not in ["nan", "none", "null"]:
                return sval

        # Otherwise, derive from key (lookup rules)
        key = row.get("LIBRARY_MATERIAL_STATUS_KEY", None)
        key = None if key is None else str(key).strip().upper()

        mapping = {
            "U": "Unknown",
            "R": "Required Course Material",
            "N": "Non-Required Course Material",
            "O": "Reserve only",
            "X": "No Required Textbook"
        }
        return mapping.get(key, "Unknown")
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["LIBRARY_MATERIAL_STATUS_CLEAN"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['LIBRARY_MATERIAL_STATUS', 'LIBRARY_MATERIAL_STATUS_CODE', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['LIBRARY_MATERIAL_STATUS', 'LIBRARY_MATERIAL_STATUS_CODE', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 5 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'LIBRARY_MATERIAL_STATUS_CLEAN', 'new_name': 'LIBRARY_MATERIAL_STATUS'}])
    # Rename
    table_1 = table_1.rename(columns={'LIBRARY_MATERIAL_STATUS_CLEAN': 'LIBRARY_MATERIAL_STATUS'})

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS'])
    # SelectCol
    _cols = [c for c in ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_course_material_links = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_course_info = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_catalog = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_material_status = prepared_table_4

# Assume prepared_* DataFrames are available
links = prepared_course_material_links.copy()
course = prepared_course_info.copy()
catalog = prepared_catalog.copy()
status = prepared_material_status.copy()

# Ensure compatible dtypes for joins where numeric strings may appear
if catalog['library_reserve_catalog_key'].dtype != links['LIBRARY_RESERVE_CATALOG_KEY'].dtype:
    catalog['library_reserve_catalog_key'] = catalog['library_reserve_catalog_key'].astype(str)
    links['LIBRARY_RESERVE_CATALOG_KEY'] = links['LIBRARY_RESERVE_CATALOG_KEY'].astype(str)

# Join links -> course to get COURSE_NAME
lc = links.merge(course, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')

# Join catalog to get publication year
lc = lc.merge(catalog[['library_reserve_catalog_key','CATALOG_YEAR']], left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='left')

# Join status to get status text
lc = lc.merge(status, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')

# Clean year: treat non-positive or null as NaN for min/max
year = pd.to_numeric(lc['CATALOG_YEAR'], errors='coerce')
year = year.where(year > 0)
lc['CATALOG_YEAR_CLEAN'] = year

# Total number of library materials per course
agg_base = lc.groupby('COURSE_NAME', dropna=False).agg(
    total_materials=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    min_publication_year=('CATALOG_YEAR_CLEAN', 'min'),
    max_publication_year=('CATALOG_YEAR_CLEAN', 'max')
).reset_index()

# Count of materials per status per course
status_counts = (
    lc.groupby(['COURSE_NAME','LIBRARY_MATERIAL_STATUS'], dropna=False)
      .size()
      .reset_index(name='materials_per_status')
)

# If a single table output is desired with status counts pivoted per course, pivot:
status_pivot = status_counts.pivot_table(index='COURSE_NAME', columns='LIBRARY_MATERIAL_STATUS', values='materials_per_status', fill_value=0, aggfunc='sum')
status_pivot = status_pivot.reset_index()

# Merge totals/min/max with per-status counts
target = agg_base.merge(status_pivot, on='COURSE_NAME', how='left')

# target now has: COURSE_NAME, total_materials, min_publication_year, max_publication_year, and one column per material status with counts

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
