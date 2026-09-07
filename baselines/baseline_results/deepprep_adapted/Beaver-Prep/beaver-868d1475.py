import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row.get('IS_ACTIVE','')).strip().upper() == 'Y' and str(row.get('IS_MOIRA_MAILING_LIST','')).strip().upper() == 'Y'
    # """)
    # Filter
    def filter_func(row):
        return str(row.get('IS_ACTIVE','')).strip().upper() == 'Y' and str(row.get('IS_MOIRA_MAILING_LIST','')).strip().upper() == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
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
    table_1["MOIRA_LIST_NAME"] = table_1["MOIRA_LIST_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_ACTIVE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_ACTIVE"] = table_1["IS_ACTIVE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_MOIRA_MAILING_LIST"] = table_1["IS_MOIRA_MAILING_LIST"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'OFFICE_LOCATION', 'OFFICE_PHONE', 'DEPARTMENT', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'FULL_NAME', 'OFFICE_LOCATION', 'OFFICE_PHONE', 'DEPARTMENT', 'FULL_NAME_UPPERCASE', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().lower()
    #     return s if s not in ["nan", "none", ""] else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().lower()
        return s if s not in ["nan", "none", ""] else None
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
    # DropNulls(table_name="table_1", subset=['EMAIL_ADDRESS', 'DEPARTMENT_NAME', 'STUDENT_YEAR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['EMAIL_ADDRESS', 'DEPARTMENT_NAME', 'STUDENT_YEAR'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # Keep only students: STUDENT_YEAR must be non-null/non-empty
    #     val = row.get(\"STUDENT_YEAR\", None)
    #     if val is None:
    #         return False
    #     v = str(val).strip()
    #     return v != \"\" and v.lower() not in [\"nan\", \"none\"]
    # """)
    # Filter
    def filter_func(row):
        # Keep only students: STUDENT_YEAR must be non-null/non-empty
        val = row.get(\"STUDENT_YEAR\", None)
        if val is None:
            return False
        v = str(val).strip()
        return v != \"\" and v.lower() not in [\"nan\", \"none\"]
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

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
def _prep_3(table_1):
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_people = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])

# Assumptions for integration: membership expansion from the mailing list to individual emails is required but not present in the selected tables.
# Therefore, derive membership solely from people whose email addresses match the mailing list name via conventional list-address pattern (not available),
# which is insufficient. To correctly answer, a list-membership table mapping list names to member email addresses is needed.

# Placeholder to show intended logic if a membership mapping were available as `prepared_members` with columns: MOIRA_LIST_NAME, EMAIL_ADDRESS
# prepared_members = ...  # synthesized from the actual membership table

# Filter to the requested list (and active Moira mailing lists)
lists_f = prepared_lists.copy()
lists_f['MOIRA_LIST_NAME'] = lists_f['MOIRA_LIST_NAME'].str.strip()
list_name = 'kangaroo-inspire-yearn'
lists_f = lists_f[(lists_f['MOIRA_LIST_NAME'] == list_name) & (lists_f['IS_ACTIVE'] == 'Y') & (lists_f['IS_MOIRA_MAILING_LIST'] == 'Y')]

# Join members to people to bring department and student status
# members_in_list = prepared_members.merge(lists_f[['MOIRA_LIST_NAME']], on='MOIRA_LIST_NAME', how='inner')
# people_in_list = members_in_list.merge(prepared_people, on='EMAIL_ADDRESS', how='left')

# Keep only students (STUDENT_YEAR not null/empty)
# students = people_in_list[people_in_list['STUDENT_YEAR'].notna() & (people_in_list['STUDENT_YEAR'].astype(str).str.strip() != '')]

# Aggregate by department name
# dept_counts = students.groupby('DEPARTMENT_NAME', dropna=False).size().reset_index(name='student_count')
# total = dept_counts['student_count'].sum()
# dept_counts['percentage'] = (dept_counts['student_count'] / total * 100).round(2)
# result = dept_counts.rename(columns={'DEPARTMENT_NAME': 'department_name'})[['department_name', 'student_count', 'percentage']]

# result

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
