import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # import re
    # def is_valid_email(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', s) is not None
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_email(val):
        if val is None:
            return False
        s = str(val).strip()
        return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', s) is not None
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_email(val))
        except Exception:
            return False
    table_1 = table_1[table_1['EMAIL_ADDRESS'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().lower()
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().lower()
        return s if s != '' and s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMAIL_ADDRESS"] = table_1["EMAIL_ADDRESS"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s if s != '' and s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s if s != '' and s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import re
    # def filter_func(row):
    #     email = row.get('EMAIL_ADDRESS', None)
    #     dept = row.get('DEPARTMENT_NAME', None)
    #     if email is None or dept is None:
    #         return False
    #     return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', str(email).strip()) is not None
    # """)
    # Filter
    def filter_func(row):
        email = row.get('EMAIL_ADDRESS', None)
        dept = row.get('DEPARTMENT_NAME', None)
        if email is None or dept is None:
            return False
        return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', str(email).strip()) is not None
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['EMAIL_ADDRESS', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['EMAIL_ADDRESS', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='first').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="DEPARTMENT_NAME", mode="mode")
    # MissingValueImputation
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].fillna(table_1["DEPARTMENT_NAME"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)              # collapse whitespace
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)              # collapse whitespace
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_FULL_NAME", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)              # collapse whitespace
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)              # collapse whitespace
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_FULL_NAME"] = table_1["DEPARTMENT_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME'], how="all")
    # DropNulls
    table_1 = table_1.dropna(subset=['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME'], how='all').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_departments = prepared_table_2

# Inputs: prepared_people, prepared_departments, and an emails table representing lists (not among selected tables).
# Since only people and departments are provided, assume another process selects people by list name 'date-destiny'.
# Here, demonstrate logic assuming a DataFrame `emails_in_list` with EMAIL_ADDRESS for the list.

# 1) Filter people to those in the email list 'date-destiny'
# emails_in_list should have a column EMAIL_ADDRESS for members of the list
people_in_list = prepared_people.merge(emails_in_list[["EMAIL_ADDRESS"]].drop_duplicates(), on="EMAIL_ADDRESS", how="inner")

# 2) Optionally integrate department reference (kept simple here)
people_in_list = people_in_list.merge(prepared_departments, on="DEPARTMENT_NAME", how="left")

# 3) Compute counts
total_students = len(people_in_list)
mgmt_count = (people_in_list["DEPARTMENT_NAME"].str.strip().str.lower() == "management").sum()
percentage = round((mgmt_count / total_students) * 100, 2) if total_students > 0 else 0.0

# 4) Produce final answer row
answer = pd.DataFrame([
    {
        "list_name": "date-destiny",
        "department_name": "Management",
        "management_student_count": int(mgmt_count),
        "management_percentage": percentage
    }
])

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
