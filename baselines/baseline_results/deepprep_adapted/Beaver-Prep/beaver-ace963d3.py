import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'MEET_PLACE', 'RESPONSIBLE_FACULTY_NAME'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'MEET_PLACE', 'RESPONSIBLE_FACULTY_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MEET_PLACE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s)
    #     if s.strip().lower() in {"nan", "none", ""}:
    #         return None
    #     # normalize whitespace and separators commonly found in building/room strings
    #     s = re.sub(r"\s+", " ", s).strip()
    #     s = s.replace(" - ", "-")
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s)
        if s.strip().lower() in {"nan", "none", ""}:
            return None
        # normalize whitespace and separators commonly found in building/room strings
        s = re.sub(r"\s+", " ", s).strip()
        s = s.replace(" - ", "-")
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MEET_PLACE"] = table_1["MEET_PLACE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_NAME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s)
    #     if s.strip().lower() in {"nan", "none", ""}:
    #         return None
    #     # normalize spaces; keep original capitalization for name matching
    #     s = re.sub(r"\s+", " ", s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s)
        if s.strip().lower() in {"nan", "none", ""}:
            return None
        # normalize spaces; keep original capitalization for name matching
        s = re.sub(r"\s+", " ", s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["RESPONSIBLE_FACULTY_NAME"] = table_1["RESPONSIBLE_FACULTY_NAME"].apply(_std_apply)

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
    # Deduplicate(table_name="table_1", subset=['COURSE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['COURSE'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="COURSE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # collapse multiple spaces to single space (e.g., '10  A' -> '10 A')
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # collapse multiple spaces to single space (e.g., '10  A' -> '10 A')
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["COURSE"] = table_1["COURSE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # keep only valid mappings
    #     return (row.get('COURSE') is not None) and (row.get('COURSE_LEVEL') in ['U','G'])
    # """)
    # Filter
    def filter_func(row):
        # keep only valid mappings
        return (row.get('COURSE') is not None) and (row.get('COURSE_LEVEL') in ['U','G'])
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['COURSE', 'COURSE_LEVEL'])
    # SelectCol
    _cols = [c for c in ['COURSE', 'COURSE_LEVEL'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['COURSE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['COURSE'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_course_levels = prepared_table_2

# Assume the two prepared tables exist as dataframes: prepared_offerings, prepared_course_levels

# 1) Filter to classes that take place in MIT buildings and extract building name
# Heuristic: MEET_PLACE often like '32-141', 'E51-145', 'Room 34-101', or 'Building 4, 149'.
# Extract the leading building designator (alphanumeric prefix before first space or hyphen),
# then map common MIT codes to canonical building names if desired. Keep the raw code as the building name.

off = prepared_offerings.copy()

# Keep only rows with a non-null meeting place
off = off[off['MEET_PLACE'].notna()]

# Extract a building code/name from MEET_PLACE
def extract_building(meet_place: str):
    s = str(meet_place).strip()
    # Normalize common prefixes like 'Room ' or 'Bldg ' or 'Building '
    for pref in ['Room ', 'Rm ', 'Bldg ', 'Building ']:
        if s.startswith(pref):
            s = s[len(pref):].strip()
            break
    # Split on common separators and take the first token as building identifier
    for sep in ['-', ' ', ',']:
        if sep in s:
            token = s.split(sep)[0]
            return token
    return s

off['BUILDING'] = off['MEET_PLACE'].astype(str).map(extract_building)

# Filter out clearly non-MIT or missing building indicators (heuristic: keep alphanumeric building codes)
off = off[off['BUILDING'].str.len() > 0]

# 2) Join to course levels
levels = prepared_course_levels[['COURSE', 'COURSE_LEVEL']].drop_duplicates()
merged = off.merge(levels, left_on='COURSE_NUMBER', right_on='COURSE', how='left')

# Map level codes to labels
level_map = {'U': 'Undergraduate', 'G': 'Graduate'}
merged['COURSE_LEVEL_LABEL'] = merged['COURSE_LEVEL'].map(level_map)

# 3) Aggregate: unique courses and total instructors per building x level
# Unique courses: count distinct SUBJECT_ID within each group
# Total instructors: count distinct RESPONSIBLE_FACULTY_NAME within each group (dropna)

merged['RESPONSIBLE_FACULTY_NAME'] = merged['RESPONSIBLE_FACULTY_NAME'].fillna('')

group_cols = ['BUILDING', 'COURSE_LEVEL_LABEL']
agg = merged.groupby(group_cols).agg(
    unique_courses=('SUBJECT_ID', pd.Series.nunique),
    total_instructors=('RESPONSIBLE_FACULTY_NAME', lambda s: s.replace('', pd.NA).dropna().nunique())
).reset_index()

# 4) Subtotals per building and per course level, plus grand total

# Subtotal per building (all levels combined)
building_sub = merged.groupby(['BUILDING']).agg(
    unique_courses=('SUBJECT_ID', pd.Series.nunique),
    total_instructors=('RESPONSIBLE_FACULTY_NAME', lambda s: s.replace('', pd.NA).dropna().nunique())
).reset_index()
building_sub['COURSE_LEVEL_LABEL'] = 'All levels'

# Subtotal per level (all buildings combined)
level_sub = merged.groupby(['COURSE_LEVEL_LABEL']).agg(
    unique_courses=('SUBJECT_ID', pd.Series.nunique),
    total_instructors=('RESPONSIBLE_FACULTY_NAME', lambda s: s.replace('', pd.NA).dropna().nunique())
).reset_index()
level_sub['BUILDING'] = 'All buildings'

# Grand total
grand_total = pd.DataFrame({
    'BUILDING': ['All buildings'],
    'COURSE_LEVEL_LABEL': ['All levels'],
    'unique_courses': [merged['SUBJECT_ID'].nunique()],
    'total_instructors': [merged['RESPONSIBLE_FACULTY_NAME'].replace('', pd.NA).dropna().nunique()]
})

# Combine
result = pd.concat([
    agg,
    building_sub[['BUILDING', 'COURSE_LEVEL_LABEL', 'unique_courses', 'total_instructors']],
    level_sub[['BUILDING', 'COURSE_LEVEL_LABEL', 'unique_courses', 'total_instructors']],
    grand_total
], ignore_index=True)

# Optional: sort for readability
result = result.sort_values(['BUILDING', 'COURSE_LEVEL_LABEL']).reset_index(drop=True)

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
