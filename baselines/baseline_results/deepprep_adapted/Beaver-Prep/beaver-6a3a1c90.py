import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes-like artifacts are already part of display; just trim spaces and normalize key
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # remove surrounding quotes-like artifacts are already part of display; just trim spaces and normalize key
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_KEY"] = table_1["MOIRA_LIST_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_NAME", func="""
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
    table_1["MOIRA_LIST_NAME"] = table_1["MOIRA_LIST_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_FULL_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return " ".join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_FULL_NAME"] = table_1["MOIRA_LIST_MEMBER_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # keep a consistent representation for downstream matching/classification
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # keep a consistent representation for downstream matching/classification
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
    # CastType(table_name="table_1", column="MOIRA_LIST_MEMBER_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID']
    if _dtype == "datetime64":
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_MEMBER_MIT_ID', 'MOIRA_LIST_MEMBER_FULL_NAME', 'moira_list_member'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_MEMBER_MIT_ID', 'MOIRA_LIST_MEMBER_FULL_NAME', 'moira_list_member'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_FACULTY", dtype="bool")
    # CastType
    _dtype = 'bool'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IS_FACULTY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IS_FACULTY']
    if _dtype == "datetime64":
        table_1['IS_FACULTY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IS_FACULTY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IS_FACULTY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IS_FACULTY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'IS_FACULTY', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'IS_FACULTY', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_people = prepared_table_3

# Assume prepared_lists, prepared_members, prepared_people are pre-synthesized per targets above

# Join members to people by MIT_ID to get role flags
m_with_people = prepared_members.merge(
    prepared_people, how='left', left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID'
)

# Define role flags
# Faculty: IS_FACULTY == 'Y'
# Support staff: treat non-faculty staff via personnel subarea fields when available
m_with_people['is_faculty'] = (m_with_people['IS_FACULTY'] == 'Y')
# Heuristic: support staff if not faculty and personnel subarea/code present (non-null/non-empty)
ps_present = m_with_people['PERSONNEL_SUBAREA'].notna() | m_with_people['PERSONNEL_SUBAREA_CODE'].notna()
m_with_people['is_support'] = (~m_with_people['is_faculty']) & ps_present

# Keep only members that are either support staff or faculty for list selection
eligible_lists = m_with_people.loc[m_with_people['is_faculty'] | m_with_people['is_support'], ['MOIRA_LIST_KEY']].drop_duplicates()

# Join lists to eligible list keys
lists_eligible = prepared_lists.merge(eligible_lists, on='MOIRA_LIST_KEY', how='inner')

# Now compute per-list counts of faculty and support staff using only members in those roles
role_counts = m_with_people.loc[m_with_people['MOIRA_LIST_KEY'].isin(lists_eligible['MOIRA_LIST_KEY'])]
agg = role_counts.groupby('MOIRA_LIST_KEY').agg(
    num_support_staff=('is_support', 'sum'),
    num_faculty=('is_faculty', 'sum')
).reset_index()

# Final join to get list name and active status
result = lists_eligible.merge(agg, on='MOIRA_LIST_KEY', how='left')

# Select and rename columns
result = result[['MOIRA_LIST_NAME', 'num_support_staff', 'num_faculty', 'IS_ACTIVE']].sort_values('MOIRA_LIST_NAME')

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
