import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['SUBJECT_CODE','SUBJECT_CODE_DESC','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_CODE','SCHOOL_NAME','COURSE_NUMBER']].copy()
    prepared['COURSE_NUMBER'] = prepared['COURSE_NUMBER'].astype(str).str.strip()
    target = prepared[['SUBJECT_CODE','SUBJECT_CODE_DESC','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_CODE','SCHOOL_NAME','COURSE_NUMBER']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_CODE','SCHOOL_NAME']].copy()
    df = df.drop_duplicates(subset=['DEPARTMENT_CODE'], keep='first')
    target = df[['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_CODE','SCHOOL_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['SIS_ADMIN_DEPARTMENT_CODE','department_phone_number']].copy()
    df['department_phone_number'] = pd.to_numeric(df['department_phone_number'], errors='coerce')
    df['department_phone_number'] = df['department_phone_number'].round().astype('Int64').astype('string')
    df.loc[df['department_phone_number'].isna(), 'department_phone_number'] = pd.NA
    target = df[['SIS_ADMIN_DEPARTMENT_CODE','department_phone_number']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_departments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_dept_phones = prepared_table_3

# Start from prepared subjects (SIS subjects) and link to canonical departments/schools
subj = prepared_subjects.copy()
depts = prepared_departments.copy()
phones = prepared_dept_phones.copy()

# Normalize key columns to string and trim whitespace
for df, cols in [
    (subj, ["DEPARTMENT_CODE", "COURSE_NUMBER", "SUBJECT_CODE", "SUBJECT_CODE_DESC", "SCHOOL_CODE", "SCHOOL_NAME", "DEPARTMENT_NAME"]),
    (depts, ["DEPARTMENT_CODE", "DEPARTMENT_NAME", "SCHOOL_CODE", "SCHOOL_NAME"]),
    (phones, ["SIS_ADMIN_DEPARTMENT_CODE", "department_phone_number"])]:
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

# Join subjects to departments to get authoritative school/department names
sj = subj.merge(
    depts,
    on="DEPARTMENT_CODE",
    how="left",
    suffixes=("_from_subjects", "")
)

# Prefer department/school names from the canonical table when available
sj["DEPARTMENT_NAME_FINAL"] = sj["DEPARTMENT_NAME"].where(sj["DEPARTMENT_NAME"].notna() & (sj["DEPARTMENT_NAME"] != "nan"), sj.get("DEPARTMENT_NAME_from_subjects"))
sj["SCHOOL_NAME_FINAL"] = sj["SCHOOL_NAME"].where(sj["SCHOOL_NAME"].notna() & (sj["SCHOOL_NAME"] != "nan"), sj.get("SCHOOL_NAME_from_subjects"))
sj["SCHOOL_CODE_FINAL"] = sj["SCHOOL_CODE"].where(sj["SCHOOL_CODE"].notna() & (sj["SCHOOL_CODE"] != "nan"), sj.get("SCHOOL_CODE_from_subjects"))

# Prepare phone counts per department (count distinct non-null numbers)
phones_clean = phones[phones["department_phone_number"].notna() & (phones["department_phone_number"] != "nan")].copy()
phones_clean["department_phone_number"] = phones_clean["department_phone_number"].str.replace(".0$", "", regex=True)
phone_counts = (
    phones_clean.groupby("SIS_ADMIN_DEPARTMENT_CODE")["department_phone_number"]
    .nunique()
    .reset_index()
    .rename(columns={"SIS_ADMIN_DEPARTMENT_CODE": "DEPARTMENT_CODE", "department_phone_number": "total_phone_numbers"})
)

# Derive course level from COURSE_NUMBER (e.g., take leading digits; fallback 'Unknown')
def extract_level(cn):
    if pd.isna(cn):
        return "Unknown"
    s = str(cn).strip()
    m = re.search(r"(\d+)", s)
    if not m:
        return "Unknown"
    num = m.group(1)
    # Define level by first digit (e.g., 1xx, 2xx, etc.)
    return num[0] + "xx" if len(num) >= 1 else "Unknown"

sj["course_level"] = sj["COURSE_NUMBER"].apply(extract_level)

# For each department, determine the most common course level among its SIS subjects
level_mode = (
    sj.groupby(["SCHOOL_CODE_FINAL", "SCHOOL_NAME_FINAL", "DEPARTMENT_CODE", "DEPARTMENT_NAME_FINAL"])['course_level']
      .agg(lambda s: s.value_counts().index[0] if len(s) else "Unknown")
      .reset_index()
)

# Attach phone counts
result = level_mode.merge(phone_counts, on="DEPARTMENT_CODE", how="left")
result["total_phone_numbers"].fillna(0, inplace=True)
result["total_phone_numbers"] = result["total_phone_numbers"].astype(int)

# Final selection and rename
final = result.rename(columns={
    "SCHOOL_CODE_FINAL": "school_code",
    "SCHOOL_NAME_FINAL": "school_name",
    "DEPARTMENT_CODE": "department_code",
    "DEPARTMENT_NAME_FINAL": "department_name",
    "course_level": "most_common_course_level"
})[
    [
        "school_code",
        "school_name",
        "department_code",
        "department_name",
        "total_phone_numbers",
        "most_common_course_level"
    ]
]

# Keep only schools/departments that offer SIS courses (already ensured by starting from subj)
target = final.sort_values(["school_code", "department_code"]).reset_index(drop=True)

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
