import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TERM_CODE','COURSE_NUMBER','SUBJECT_ID','SUBJECT_TITLE','MEET_PLACE','RESPONSIBLE_FACULTY_NAME']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TERM_CODE','COURSE_NUMBER','SUBJECT_ID','SUBJECT_TITLE','MEET_PLACE','RESPONSIBLE_FACULTY_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['COURSE','COURSE_LEVEL']].copy()
    df['COURSE_LEVEL'] = df['COURSE_LEVEL'].astype(str).str.strip().str.upper()
    df = df[df['COURSE_LEVEL'].isin(['U','G'])].copy()
    counts = df.groupby(['COURSE','COURSE_LEVEL'], as_index=False).size()
    counts['level_rank'] = counts['COURSE_LEVEL'].map({'U': 0, 'G': 1})
    counts = counts.sort_values(['COURSE','size','level_rank'], ascending=[True, False, True])
    target = counts.drop_duplicates(subset=['COURSE'], keep='first')[['COURSE','COURSE_LEVEL']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
