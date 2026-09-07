import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MIT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     last = row.get('LAST_NAME')
    #     is_fac = row.get('IS_FACULTY')
    #     # Keep only faculty with last name starting with 'Y' (case-insensitive)
    #     if pd.isna(last) or pd.isna(is_fac):
    #         return False
    #     return bool(is_fac) and str(last).strip().upper().startswith('Y')
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        last = row.get('LAST_NAME')
        is_fac = row.get('IS_FACULTY')
        # Keep only faculty with last name starting with 'Y' (case-insensitive)
        if pd.isna(last) or pd.isna(is_fac):
            return False
        return bool(is_fac) and str(last).strip().upper().startswith('Y')
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'EMAIL_ADDRESS', 'IS_FACULTY'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'EMAIL_ADDRESS', 'IS_FACULTY'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # MissingValueImputation(table_name="table_1", column_name="MOIRA_LIST_MEMBER_MIT_ID", mode="mode")
    # MissingValueImputation
    table_1["MOIRA_LIST_MEMBER_MIT_ID"] = table_1["MOIRA_LIST_MEMBER_MIT_ID"].fillna(table_1["MOIRA_LIST_MEMBER_MIT_ID"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # keep as evidence, just trim surrounding whitespace and normalize internal spacing
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s if s.lower() != 'nan' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # keep as evidence, just trim surrounding whitespace and normalize internal spacing
        s = str(s).strip()
        s = " ".join(s.split())
        return s if s.lower() != 'nan' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_FULL_NAME"] = table_1["MOIRA_LIST_MEMBER_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_MIT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SUBJECT_TITLE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return None if s.lower() in {"nan", "none"} else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return None if s.lower() in {"nan", "none"} else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SUBJECT_TITLE"] = table_1["SUBJECT_TITLE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="RESPONSIBLE_FACULTY_MIT_ID", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"nan", "none", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"nan", "none", ""}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["RESPONSIBLE_FACULTY_MIT_ID"] = table_1["RESPONSIBLE_FACULTY_MIT_ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['RESPONSIBLE_FACULTY_MIT_ID', 'SUBJECT_ID', 'SUBJECT_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['RESPONSIBLE_FACULTY_MIT_ID', 'SUBJECT_ID', 'SUBJECT_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['RESPONSIBLE_FACULTY_MIT_ID', 'SUBJECT_ID', 'SUBJECT_TITLE'])
    # SelectCol
    _cols = [c for c in ['RESPONSIBLE_FACULTY_MIT_ID', 'SUBJECT_ID', 'SUBJECT_TITLE'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_moira_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_subjects = prepared_table_3

# Assume prepared_people, prepared_moira_members, prepared_subjects are the synthesized per-table targets

# Normalize ID types
prepared_people = prepared_people.copy()
prepared_people['MIT_ID'] = pd.to_numeric(prepared_people['MIT_ID'], errors='coerce')

prepared_moira_members = prepared_moira_members.copy()
prepared_moira_members['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(prepared_moira_members['MOIRA_LIST_MEMBER_MIT_ID'], errors='coerce')

prepared_subjects = prepared_subjects.copy()
prepared_subjects['RESPONSIBLE_FACULTY_MIT_ID'] = pd.to_numeric(prepared_subjects['RESPONSIBLE_FACULTY_MIT_ID'], errors='coerce')

# Join list memberships to people
m = prepared_moira_members.merge(
    prepared_people,
    left_on='MOIRA_LIST_MEMBER_MIT_ID',
    right_on='MIT_ID',
    how='inner'
)

# Filter to faculty and last names starting with 'Y'
m = m[(m['IS_FACULTY'].astype(str).str.upper().isin(['Y', 'YES', 'TRUE', '1'])) &
      (m['LAST_NAME'].astype(str).str.upper().str.startswith('Y'))]

# Join to subjects managed by those faculty
ms = m.merge(
    prepared_subjects,
    left_on='MIT_ID',
    right_on='RESPONSIBLE_FACULTY_MIT_ID',
    how='left'
)

# Aggregate: for each list, count unique faculty and total subjects managed by those faculty
# Total subjects: count distinct SUBJECT_ID across all matched faculty within the list
agg = ms.groupby('MOIRA_LIST_KEY').agg(
    num_faculty_in_list=('MIT_ID', 'nunique'),
    total_subjects_managed=('SUBJECT_ID', pd.Series.nunique)
).reset_index()

# If a list has faculty but none manage subjects in data, ensure total_subjects_managed is 0
agg['total_subjects_managed'] = agg['total_subjects_managed'].fillna(0).astype(int)

# Prepare final output columns
result = agg.rename(columns={'MOIRA_LIST_KEY': 'list_name'})

# Sort for presentation (optional)
result = result.sort_values(['num_faculty_in_list', 'total_subjects_managed', 'list_name'], ascending=[False, False, True])

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
