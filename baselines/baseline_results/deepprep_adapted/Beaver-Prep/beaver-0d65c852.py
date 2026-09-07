import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="HGN_DESC", mode="mode")
    # MissingValueImputation
    table_1["HGN_DESC"] = table_1["HGN_DESC"].fillna(table_1["HGN_DESC"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
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
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
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
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     # remove wrapping quotes if present
    #     s = s.strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     # normalize internal whitespace/newlines
    #     s = " ".join(s.split())
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s)
        # remove wrapping quotes if present
        s = s.strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        # normalize internal whitespace/newlines
        s = " ".join(s.split())
        return s.strip()
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
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return " ".join(s.split()).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return " ".join(s.split()).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HGN_DESC", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return " ".join(s.split()).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return " ".join(s.split()).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["HGN_DESC"] = table_1["HGN_DESC"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACADEMIC_YEAR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACADEMIC_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACADEMIC_YEAR']
    if _dtype == "datetime64":
        table_1['ACADEMIC_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACADEMIC_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACADEMIC_YEAR'] = _series.astype(str)

    # ---------------- Step 9 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TOTAL_UNITS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TOTAL_UNITS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TOTAL_UNITS']
    if _dtype == "datetime64":
        table_1['TOTAL_UNITS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TOTAL_UNITS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TOTAL_UNITS'] = _series.astype(str)

    # ---------------- Step 10 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TERM_CODE', 'SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 11 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 12 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'TOTAL_UNITS', 'HGN_DESC'])
    # SelectCol
    _cols = [c for c in ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'TOTAL_UNITS', 'HGN_DESC'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 13 ----------------
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
    # CastType(table_name="table_1", column="IS_LECTURE_SECTION", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_LECTURE_SECTION'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_LECTURE_SECTION']
    if _dtype == "datetime64":
        table_1['IS_LECTURE_SECTION'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_LECTURE_SECTION'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_LECTURE_SECTION'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_LECTURE_SECTION'] = _series.astype(str)

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
    # CastType(table_name="table_1", column="SUBJECT_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SUBJECT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SUBJECT_ID']
    if _dtype == "datetime64":
        table_1['SUBJECT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SUBJECT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SUBJECT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SUBJECT_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SECTION_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SECTION_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SECTION_ID']
    if _dtype == "datetime64":
        table_1['SECTION_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SECTION_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SECTION_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SECTION_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_MASTER_SECTION", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_MASTER_SECTION'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_MASTER_SECTION']
    if _dtype == "datetime64":
        table_1['IS_MASTER_SECTION'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_MASTER_SECTION'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_MASTER_SECTION'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_MASTER_SECTION'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_LAB_SECTION", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_LAB_SECTION'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_LAB_SECTION']
    if _dtype == "datetime64":
        table_1['IS_LAB_SECTION'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_LAB_SECTION'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_LAB_SECTION'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_LAB_SECTION'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_RECITATION_SECTION", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_RECITATION_SECTION'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_RECITATION_SECTION']
    if _dtype == "datetime64":
        table_1['IS_RECITATION_SECTION'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_RECITATION_SECTION'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_RECITATION_SECTION'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_RECITATION_SECTION'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
    #         return None
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in ["", "nan", "none", "null"]):
            return None
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["RESPONSIBLE_FACULTY_NAME"] = table_1["RESPONSIBLE_FACULTY_NAME"].apply(_std_apply)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'RESPONSIBLE_FACULTY_NAME', 'SECTION_ID', 'IS_MASTER_SECTION', 'IS_LECTURE_SECTION', 'IS_LAB_SECTION', 'IS_RECITATION_SECTION'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'RESPONSIBLE_FACULTY_NAME', 'SECTION_ID', 'IS_MASTER_SECTION', 'IS_LECTURE_SECTION', 'IS_LAB_SECTION', 'IS_RECITATION_SECTION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID', 'SECTION_ID', 'RESPONSIBLE_FACULTY_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID', 'SECTION_ID', 'RESPONSIBLE_FACULTY_NAME'], keep='last').reset_index(drop=True)

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
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_8'])

# Assume prepared_subject_catalog (psc) and prepared_subject_offerings (pso) are created from table_1 and table_2 respectively

# Determine current academic year from the data (latest ACADEMIC_YEAR available)
current_year = psc['ACADEMIC_YEAR'].max()

# Keep only this year's subjects in catalog
psc_year = psc[psc['ACADEMIC_YEAR'] == current_year].copy()

# Keep only Fall or Spring term offerings for this year
# Identify Fall/Spring by TERM_CODE suffixes commonly used (e.g., 'FA' for Fall, 'SP' for Spring)
pso_year = pso[pso['TERM_CODE'].str.contains(str(current_year))].copy()

# Map term label and description
def term_label(tc):
    return 'Fall' if tc.endswith('FA') else ('Spring' if tc.endswith('SP') else None)

def term_desc(tc):
    return 'Fall Term' if tc.endswith('FA') else ('Spring Term' if tc.endswith('SP') else None)

pso_year['term_label'] = pso_year['TERM_CODE'].apply(term_label)
pso_year['term_description'] = pso_year['TERM_CODE'].apply(term_desc)

# Filter to Fall/Spring only
pso_fs = pso_year[pso_year['term_label'].notna()].copy()

# Count distinct instructors by SUBJECT_ID and term_label
# Use RESPONSIBLE_FACULTY_NAME, excluding nulls
inst = pso_fs.dropna(subset=['RESPONSIBLE_FACULTY_NAME']).copy()
inst_counts = (inst.groupby(['SUBJECT_ID', 'term_label'])['RESPONSIBLE_FACULTY_NAME']
                  .nunique()
                  .reset_index(name='distinct_instructors'))

# Pivot to separate Fall and Spring counts
inst_pivot = (inst_counts.pivot(index='SUBJECT_ID', columns='term_label', values='distinct_instructors')
                          .reset_index()
                          .rename_axis(None, axis=1))
inst_pivot['Fall'] = inst_pivot.get('Fall').fillna(0).astype(int)
inst_pivot['Spring'] = inst_pivot.get('Spring').fillna(0).astype(int)

# Join catalog with offerings (to get school and per-term presence), then deduplicate per subject-term
merged = psc_year.merge(pso_fs[['SUBJECT_ID','TERM_CODE','term_label','term_description','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME']].drop_duplicates(),
                        on=['SUBJECT_ID','TERM_CODE'], how='inner')

# For subjects offered in either term this year, create output rows per (subject, term)
# Join instructor counts back by SUBJECT_ID (term counts are split into Fall/Spring columns)
result = merged.merge(inst_pivot, on='SUBJECT_ID', how='left')

# Prepare final columns
result['Fall'] = result['Fall'].fillna(0).astype(int)
result['Spring'] = result['Spring'].fillna(0).astype(int)

# Course level from catalog HGN_DESC, total units from TOTAL_UNITS
final = result[['DEPARTMENT_NAME', 'OFFER_SCHOOL_NAME', 'SUBJECT_ID', 'SUBJECT_TITLE', 'HGN_DESC', 'TOTAL_UNITS', 'term_label', 'term_description', 'Fall', 'Spring']].drop_duplicates()
final = final.rename(columns={
    'DEPARTMENT_NAME': 'department_name',
    'OFFER_SCHOOL_NAME': 'school_name',
    'SUBJECT_ID': 'subject_id',
    'SUBJECT_TITLE': 'subject_title',
    'HGN_DESC': 'course_level',
    'TOTAL_UNITS': 'total_units',
    'term_label': 'term',
    'term_description': 'term_description',
    'Fall': 'num_distinct_instructors_fall',
    'Spring': 'num_distinct_instructors_spring'
})

# Keep only terms Fall or Spring (already ensured), and only this year (ensured by filters)
answer = final.sort_values(['department_name','subject_id','term'])

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
