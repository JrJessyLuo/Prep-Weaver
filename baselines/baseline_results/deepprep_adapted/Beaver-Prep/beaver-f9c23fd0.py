import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="TERM_CODE", mode="mode")
    # MissingValueImputation
    table_1["TERM_CODE"] = table_1["TERM_CODE"].fillna(table_1["TERM_CODE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="subject_material_links", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Normalize common placeholder / non-key strings to null
    #     def norm_val(x):
    #         if pd.isna(x):
    #             return np.nan
    #         s = str(x).strip()
    #         if s == "" or s.lower() in {"nan", "none", "null"}:
    #             return np.nan
    #         return s
    # 
    #     for col in ["TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY", "ISBN", "TERM_CODE", "subject_id"]:
    #         if col in df.columns:
    #             df[col] = df[col].map(norm_val)
    # 
    #     # Material placeholder that indicates "no materials" -> not a valid linking key
    #     if "TIP_MATERIAL_KEY" in df.columns:
    #         df.loc[df["TIP_MATERIAL_KEY"].str.contains("Course has no materials", case=False, na=False), "TIP_MATERIAL_KEY"] = np.nan
    #         df.loc[df["TIP_MATERIAL_KEY"].str.fullmatch(r"N/A", case=False, na=False), "TIP_MATERIAL_KEY"] = np.nan
    # 
    #     # Keep only required columns
    #     out = df[["TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY", "ISBN", "TERM_CODE", "subject_id"]].copy()
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Normalize common placeholder / non-key strings to null
        def norm_val(x):
            if pd.isna(x):
                return np.nan
            s = str(x).strip()
            if s == "" or s.lower() in {"nan", "none", "null"}:
                return np.nan
            return s

        for col in ["TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY", "ISBN", "TERM_CODE", "subject_id"]:
            if col in df.columns:
                df[col] = df[col].map(norm_val)

        # Material placeholder that indicates "no materials" -> not a valid linking key
        if "TIP_MATERIAL_KEY" in df.columns:
            df.loc[df["TIP_MATERIAL_KEY"].str.contains("Course has no materials", case=False, na=False), "TIP_MATERIAL_KEY"] = np.nan
            df.loc[df["TIP_MATERIAL_KEY"].str.fullmatch(r"N/A", case=False, na=False), "TIP_MATERIAL_KEY"] = np.nan

        # Keep only required columns
        out = df[["TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY", "ISBN", "TERM_CODE", "subject_id"]].copy()
        return out
    subject_material_links = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="subject_material_links", subset=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'ISBN'], how="any")
    # DropNulls
    subject_material_links = subject_material_links.dropna(subset=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'ISBN'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="subject_material_links", subset=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'ISBN', 'TERM_CODE', 'subject_id'], keep="first")
    # Deduplicate
    subject_material_links = subject_material_links.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'ISBN', 'TERM_CODE', 'subject_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="subject_material_links", columns=['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'ISBN', 'TERM_CODE', 'subject_id'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'ISBN', 'TERM_CODE', 'subject_id'] if c in subject_material_links.columns]
    subject_material_links = subject_material_links[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Terminate(result=['subject_material_links'])
    # Terminate
    result = {'subject_material_links': subject_material_links}
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
    # OutlierDetection(table_name="table_1", column_name="NEW_SHELF_PRICE", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['NEW_SHELF_PRICE'].quantile(0.25)
    _q3 = table_1['NEW_SHELF_PRICE'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_NEW_SHELF_PRICE_is_outlier'] = table_1['NEW_SHELF_PRICE'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_NEW_SHELF_PRICE_is_outlier'] == False]
        table_1.drop(columns=['table_1_NEW_SHELF_PRICE_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_NEW_SHELF_PRICE_is_outlier'] = table_1['table_1_NEW_SHELF_PRICE_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     # remove wrapping quotes if present and trim
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s)
        # remove wrapping quotes if present and trim
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
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
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    #     # remove wrapping quotes and whitespace; keep digits/X only
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     cleaned = ''.join(ch for ch in s if ch.isdigit() or ch in ['X','x'])
    #     return cleaned if cleaned else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "none", ""]:
            return None
        # remove wrapping quotes and whitespace; keep digits/X only
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        cleaned = ''.join(ch for ch in s if ch.isdigit() or ch in ['X','x'])
        return cleaned if cleaned else None
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
    # StandardizeString(table_name="table_1", column_name="TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     # trim and collapse repeated whitespace
    #     s = " ".join(s.strip().split())
    #     # normalize to title case for consistency
    #     return s.title() if s else s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s)
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        # trim and collapse repeated whitespace
        s = " ".join(s.strip().split())
        # normalize to title case for consistency
        return s.title() if s else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TITLE"] = table_1["TITLE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="NEW_SHELF_PRICE", mode="median")
    # MissingValueImputation
    table_1["NEW_SHELF_PRICE"] = table_1["NEW_SHELF_PRICE"].fillna(table_1["NEW_SHELF_PRICE"].median())

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'NEW_SHELF_PRICE'])
    # SelectCol
    _cols = [c for c in ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'NEW_SHELF_PRICE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['NEW_SHELF_PRICE', 'TIP_MATERIAL_KEY'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['NEW_SHELF_PRICE', 'TIP_MATERIAL_KEY'], ascending=[True, True])

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('TIP_SUBJECT_OFFERED_KEY') is not None and str(row.get('TIP_SUBJECT_OFFERED_KEY')).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        return row.get('TIP_SUBJECT_OFFERED_KEY') is not None and str(row.get('TIP_SUBJECT_OFFERED_KEY')).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TIP_SUBJECT_OFFERED_KEY', 'SUBJECT_TITLE'])
    # SelectCol
    _cols = [c for c in ['TIP_SUBJECT_OFFERED_KEY', 'SUBJECT_TITLE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SUBJECT_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SUBJECT_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # trim and collapse repeated whitespace
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # trim and collapse repeated whitespace
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     val = row.get('SUBJECT_TITLE')
    #     return val is not None and str(val).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        val = row.get('SUBJECT_TITLE')
        return val is not None and str(val).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
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
prepared_material_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_material_details = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_subjects = prepared_table_3

# Merge subject titles into assignments
sa = prepared_material_assignments.merge(
    prepared_subjects, on='TIP_SUBJECT_OFFERED_KEY', how='left'
)

# Merge material details
sam = sa.merge(
    prepared_material_details, on=['TIP_MATERIAL_KEY', 'ISBN'], how='left'
)

# Compute per-subject total cost of new materials (sum of NEW_SHELF_PRICE per subject)
# Keep individual item rows for sorting by item price
sam['NEW_SHELF_PRICE'] = pd.to_numeric(sam['NEW_SHELF_PRICE'], errors='coerce')

subject_totals = sam.groupby('SUBJECT_TITLE', dropna=False)['NEW_SHELF_PRICE'].sum(min_count=1).rename('TOTAL_NEW_MATERIAL_COST').reset_index()

# Attach totals back to each item row
result = sam.merge(subject_totals, on='SUBJECT_TITLE', how='left')

# Select and rename columns for final output
result = result[['SUBJECT_TITLE', 'TITLE', 'ISBN', 'NEW_SHELF_PRICE', 'TOTAL_NEW_MATERIAL_COST']]

# Sort by individual item price ascending
result = result.sort_values(by=['NEW_SHELF_PRICE', 'SUBJECT_TITLE', 'TITLE'], ascending=[True, True, True])

# 'result' now contains: subject title, material title, ISBN, new shelf price (item-level), and total cost per subject
answer = result

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
