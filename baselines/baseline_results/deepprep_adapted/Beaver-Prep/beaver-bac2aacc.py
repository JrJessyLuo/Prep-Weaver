import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="SUBJECT_ID", func="""
    # def is_valid_email(val):
    #     return True
    # def is_valid_subject_id(val):
    #     if val is None:
    #         return False
    #     return len(str(val).strip()) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_email(val):
        return True
    def is_valid_subject_id(val):
        if val is None:
            return False
        return len(str(val).strip()) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_email(val))
        except Exception:
            return False
    table_1 = table_1[table_1['SUBJECT_ID'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'MEET_PLACE'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'MEET_PLACE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
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
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_CODE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_CODE"] = table_1["OFFER_DEPT_CODE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFER_DEPT_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFER_DEPT_NAME"] = table_1["OFFER_DEPT_NAME"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
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
    # StandardizeString(table_name="table_1", column_name="responsible_faculty_mit_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["responsible_faculty_mit_id"] = table_1["responsible_faculty_mit_id"].apply(_std_apply)

    # ---------------- Step 10 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MEET_PLACE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s2 = str(s).strip()
    #     return None if s2.lower() in ("nan", "none", "") else s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s2 = str(s).strip()
        return None if s2.lower() in ("nan", "none", "") else s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MEET_PLACE"] = table_1["MEET_PLACE"].apply(_std_apply)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="TERM_CODE", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     # remove wrapping quotes
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        # remove wrapping quotes
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
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
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
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
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
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
    # StandardizeString(table_name="table_1", column_name="SUBJECT_DESCRIPTION", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     # collapse excessive whitespace
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # collapse excessive whitespace
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_DESCRIPTION"] = table_1["SUBJECT_DESCRIPTION"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_CODE", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_CODE"] = table_1["DEPARTMENT_CODE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)):
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)):
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['TERM_CODE', 'SUBJECT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'SUBJECT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'SUBJECT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 10 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_DESCRIPTION', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME'] if c in table_1.columns]
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
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_subjects = prepared_table_2

# Merge offerings with subject metadata on SUBJECT_ID and TERM_CODE
merged = prepared_offerings.merge(prepared_subjects, on=["SUBJECT_ID", "TERM_CODE"], how="inner")

# Derive building, room, and floor from MEET_PLACE if possible (schema not provided; basic parsing example)
# Expected MEET_PLACE format examples could be like "Bldg 32-141 (1st Fl)"; adjust parsing rules as needed.
meet = merged["MEET_PLACE"].fillna("")
# Simple heuristics:
merged["BUILDING_NAME"] = meet.str.extract(r"^(.*?)(?=\s*\d|$)").fillna("").str.strip()
merged["ROOM_NAME"] = meet.str.extract(r"(\d[\w-]*)").fillna("")
merged["FLOOR_LEVEL"] = meet.str.extract(r"(\b\d+(?:st|nd|rd|th)\s*Fl\b|Floor\s*\d+)").fillna("")
merged["BUILDING_STREET_ADDRESS"] = ""  # Not present in selected tables; left blank.

# Compute total number of types of courses per department.
# Interpret "types of courses" as distinct SUBJECT_CODE (prefix before dot) or FORM_TYPE if available.
# Given available columns, use subject code prefix from SUBJECT_ID (e.g., '6' from '6.003').
merged["COURSE_TYPE"] = merged["SUBJECT_ID"].str.split(".").str[0]
course_type_counts = merged.groupby("DEPARTMENT_CODE")["COURSE_TYPE"].nunique().reset_index(name="TOTAL_COURSE_TYPES_PER_DEPT")

# Attach counts back to merged data (align by department code from prepared_subjects)
merged = merged.merge(course_type_counts, on="DEPARTMENT_CODE", how="left")

# Filter to summer term codes (assuming codes containing 'SU' denote summer, e.g., '2016SU')
summer = merged[merged["TERM_CODE"].str.contains("SU", na=False)]

# Select and rename final answer columns
answer = summer[[
    "SUBJECT_TITLE_x",            # from offerings (title as scheduled)
    "SUBJECT_DESCRIPTION",        # from subjects
    "RESPONSIBLE_FACULTY_NAME",
    "responsible_faculty_mit_id", # as proxy for email not present; email unavailable in selected tables
    "BUILDING_NAME",
    "ROOM_NAME",
    "FLOOR_LEVEL",
    "BUILDING_STREET_ADDRESS",
    "TOTAL_COURSE_TYPES_PER_DEPT"
]].rename(columns={
    "SUBJECT_TITLE_x": "subject_title",
    "SUBJECT_DESCRIPTION": "subject_description",
    "RESPONSIBLE_FACULTY_NAME": "responsible_faculty_name",
    "responsible_faculty_mit_id": "faculty_email_or_id",  # email not available; keep ID present
    "BUILDING_NAME": "building_name",
    "ROOM_NAME": "room_name",
    "FLOOR_LEVEL": "floor_level",
    "BUILDING_STREET_ADDRESS": "building_street_address",
    "TOTAL_COURSE_TYPES_PER_DEPT": "total_course_types_per_department"
})

# Drop duplicates to list each subject once per offering context
answer = answer.drop_duplicates()

target = answer

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
