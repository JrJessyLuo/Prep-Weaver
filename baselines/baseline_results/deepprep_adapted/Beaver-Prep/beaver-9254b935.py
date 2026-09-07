import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SUBJECT_TITLE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SUBJECT_TITLE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SUBJECT_TITLE']
    if _dtype == "datetime64":
        table_1['SUBJECT_TITLE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SUBJECT_TITLE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SUBJECT_TITLE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SUBJECT_TITLE'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        # remove surrounding quotes if present
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
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
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
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # collapse internal whitespace/newlines
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # collapse internal whitespace/newlines
        s = " ".join(s.split())
        return s
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
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_SCHOOL_NAME", func="""
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
    table_1["OFFER_SCHOOL_NAME"] = table_1["OFFER_SCHOOL_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     return None if t.lower() in ["nan", "none", ""] else t
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        t = str(s).strip()
        return None if t.lower() in ["nan", "none", ""] else t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TERM_CODE"] = table_1["TERM_CODE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     return None if t.lower() in ["nan", "none", ""] else t
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        t = str(s).strip()
        return None if t.lower() in ["nan", "none", ""] else t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_ID"] = table_1["SUBJECT_ID"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     return None if t.lower() in ["nan", "none", ""] else t
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        t = str(s).strip()
        return None if t.lower() in ["nan", "none", ""] else t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_SUBJECT_OFFERED_KEY"] = table_1["TIP_SUBJECT_OFFERED_KEY"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_ENROLLED_STUDENTS", dtype="float")
    # CastType
    _dtype = 'float'
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="NUM_ENROLLED_STUDENTS", mode="median")
    # MissingValueImputation
    table_1["NUM_ENROLLED_STUDENTS"] = table_1["NUM_ENROLLED_STUDENTS"].fillna(table_1["NUM_ENROLLED_STUDENTS"].median())

    # ---------------- Step 7 ----------------
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

    # ---------------- Step 8 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID', 'OFFER_SCHOOL_NAME', 'TIP_SUBJECT_OFFERED_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TERM_CODE', 'SUBJECT_ID', 'OFFER_SCHOOL_NAME', 'TIP_SUBJECT_OFFERED_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TIP_SUBJECT_OFFERED_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'OFFER_SCHOOL_NAME', 'NUM_ENROLLED_STUDENTS', 'TIP_SUBJECT_OFFERED_KEY'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'OFFER_SCHOOL_NAME', 'NUM_ENROLLED_STUDENTS', 'TIP_SUBJECT_OFFERED_KEY'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() == 'nan':
    #         return None
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() == 'nan':
            return None
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["TIP_MATERIAL_KEY"] = table_1["TIP_MATERIAL_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TIP_SUBJECT_OFFERED_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
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
    # StandardizeString(table_name="table_1", column_name="TIP_MATERIAL_STATUS_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
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
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
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
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_KEY', 'RECORD_COUNT'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_KEY', 'RECORD_COUNT'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_6'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_tip_offered = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_tip_materials = prepared_table_3

# Assume the three prepared tables already exist as dataframes with the specified columns
# prepared_subject_catalog: TERM_CODE, SUBJECT_ID, SUBJECT_TITLE
# prepared_tip_offered: TERM_CODE, SUBJECT_ID, OFFER_SCHOOL_NAME, NUM_ENROLLED_STUDENTS, TIP_SUBJECT_OFFERED_KEY
# prepared_tip_materials: TERM_CODE, TIP_SUBJECT_OFFERED_KEY, TIP_MATERIAL_STATUS_KEY, TIP_MATERIAL_KEY, RECORD_COUNT

# Join offerings to materials (left join to keep offerings with or without materials)
off_mat = prepared_tip_offered.merge(
    prepared_tip_materials.drop(columns=["TERM_CODE"]),
    on="TIP_SUBJECT_OFFERED_KEY",
    how="left"
)

# Join to catalog to bring in term description (subject title used here)
off_mat_cat = off_mat.merge(
    prepared_subject_catalog,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="left"
)

# Define helpers
# Current term flag: treat most recent TERM_CODE as current
term_order = off_mat_cat["TERM_CODE"].dropna().unique()
# If available, sort lexicographically which matches format like 2024SP/2016FA; adjust if custom order needed
current_term = pd.Series(term_order).sort_values().iloc[-1] if len(term_order) > 0 else None
off_mat_cat["IS_CURRENT_TERM"] = off_mat_cat["TERM_CODE"].eq(current_term)

# Aggregate per TERM_CODE
# - term description: choose the most frequent SUBJECT_TITLE in that term as a proxy
term_desc = (off_mat_cat
             .groupby(["TERM_CODE", "SUBJECT_TITLE"], dropna=False)
             .size()
             .reset_index(name="cnt"))
term_desc = term_desc.sort_values(["TERM_CODE", "cnt"], ascending=[True, False]).drop_duplicates(["TERM_CODE"])
term_desc = term_desc.rename(columns={"SUBJECT_TITLE": "TERM_DESCRIPTION"})[["TERM_CODE", "TERM_DESCRIPTION"]]

# Count distinct types of TIP subjects offered per term (distinct SUBJECT_ID)
subj_types = off_mat_cat.groupby("TERM_CODE")["SUBJECT_ID"].nunique().reset_index(name="TOTAL_TIP_SUBJECT_TYPES")

# Materials needed: count of offered subjects that have any material record not marked as NM (No Materials)
# If TIP_MATERIAL_STATUS_KEY == 'NM' means no materials; otherwise materials needed/present
materials_needed = (off_mat_cat.assign(has_material=lambda d: d["TIP_MATERIAL_STATUS_KEY"].notna() & d["TIP_MATERIAL_STATUS_KEY"].ne("NM"))
                    .groupby(["TERM_CODE", "SUBJECT_ID"], dropna=False)["has_material"].max()
                    .reset_index()
                    .groupby("TERM_CODE")["has_material"].sum()
                    .reset_index(name="MATERIALS_NEEDED_SUBJECTS"))

# Enrollment min/max per term
enroll_agg = off_mat_cat.groupby("TERM_CODE")["NUM_ENROLLED_STUDENTS"].agg(MIN_ENROLLED="min", MAX_ENROLLED="max").reset_index()

# Total number of schools offering subjects per term (distinct OFFER_SCHOOL_NAME)
schools = off_mat_cat.groupby("TERM_CODE")["OFFER_SCHOOL_NAME"].nunique().reset_index(name="TOTAL_SCHOOLS_OFFERING")

# Total number of records per term (row count in offerings table for that term)
# Use offered records (before exploding by materials) by counting distinct TIP_SUBJECT_OFFERED_KEY per term
offer_counts = prepared_tip_offered.groupby("TERM_CODE")["TIP_SUBJECT_OFFERED_KEY"].nunique().reset_index(name="TOTAL_RECORDS")

# Current term flag per term
current_flag = (off_mat_cat.groupby("TERM_CODE")["IS_CURRENT_TERM"].max().reset_index())

# Combine all pieces
result = (term_desc
          .merge(current_flag, on="TERM_CODE", how="left")
          .merge(subj_types, on="TERM_CODE", how="left")
          .merge(materials_needed, on="TERM_CODE", how="left")
          .merge(enroll_agg, on="TERM_CODE", how="left")
          .merge(schools, on="TERM_CODE", how="left")
          .merge(offer_counts, on="TERM_CODE", how="left")
         )

# Final columns as requested per term code
result = result[[
    "TERM_CODE",
    "TERM_DESCRIPTION",
    "IS_CURRENT_TERM",
    "TOTAL_TIP_SUBJECT_TYPES",
    "MATERIALS_NEEDED_SUBJECTS",
    "MIN_ENROLLED",
    "MAX_ENROLLED",
    "TOTAL_SCHOOLS_OFFERING",
    "TOTAL_RECORDS"
]].sort_values("TERM_CODE")

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
