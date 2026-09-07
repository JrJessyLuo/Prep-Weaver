import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="TERM_CODE", func="""
    # import re
    # def is_valid_email(val):
    #     # placeholder name in template; implement term-code validation
    #     if val is None:
    #         return False
    #     return bool(re.match(r"^\d{4}[A-Z]{2}$", str(val).strip()))
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_email(val):
        # placeholder name in template; implement term-code validation
        if val is None:
            return False
        return bool(re.match(r"^\d{4}[A-Z]{2}$", str(val).strip()))
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_email(val))
        except Exception:
            return False
    table_1 = table_1[table_1['TERM_CODE'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id'], how="all")
    # DropNulls
    table_1 = table_1.dropna(subset=['RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id'], how='all').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'SUBJECT_KEY', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SECTION_ID'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'SUBJECT_KEY', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SECTION_ID'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="EMAIL_ADDRESS", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['EMAIL_ADDRESS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['EMAIL_ADDRESS']
    if _dtype == "datetime64":
        table_1['EMAIL_ADDRESS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['EMAIL_ADDRESS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['EMAIL_ADDRESS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['EMAIL_ADDRESS'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MIT_ID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MIT_ID']
    if _dtype == "datetime64":
        table_1['MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MIT_ID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FULL_NAME", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FULL_NAME'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FULL_NAME']
    if _dtype == "datetime64":
        table_1['FULL_NAME'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FULL_NAME'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FULL_NAME'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FULL_NAME'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IS_FACULTY", dtype="string")
    # CastType
    _dtype = 'string'
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().lower()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().lower()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMAIL_ADDRESS"] = table_1["EMAIL_ADDRESS"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'FULL_NAME', 'EMAIL_ADDRESS', 'IS_FACULTY'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'FULL_NAME', 'EMAIL_ADDRESS', 'IS_FACULTY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MIT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_people = prepared_table_2

# Assume BAT produced prepared tables
courses = prepared_courses.copy()
people = prepared_people.copy()

# 1) Filter to 2023 fall term in courses. Depending on coding, TERM_CODE like '2023FA' or '2023SP'. We'll treat fall codes as containing '2023FA' or '2023F'.
fall_mask = courses['TERM_CODE'].astype(str).str.contains('2023FA|2023F', case=False, regex=True)
courses_2023_fall = courses[fall_mask].copy()

# Keep only rows with a responsible faculty MIT ID
courses_2023_fall = courses_2023_fall.dropna(subset=['responsible_faculty_mit_id'])

# 2) Link faculty identities (optional if we only need MIT IDs)
fac_courses = courses_2023_fall.merge(
    people.rename(columns={'MIT_ID':'responsible_faculty_mit_id'}),
    on='responsible_faculty_mit_id', how='left'
)

# 3) Load/assume mailing list data frames exist:
# - mailing_list_members: columns ['list_name','member_mit_id'] with one row per member in a list
# - mailing_list_subscriptions: columns ['list_name','subscriber_mit_id'] with one row per subscriber/list pair
# These are not part of selected tables but needed to answer the question.

# Keep only lists that have exactly 10 members
list_sizes = mailing_list_members.groupby('list_name')['member_mit_id'].nunique().rename('member_count').reset_index()
lists_10 = list_sizes[list_sizes['member_count'] == 10]

# 4) Faculty who subscribe to those lists (restrict subscribers to responsible faculty for 2023 fall courses)
responsible_faculty_ids = fac_courses['responsible_faculty_mit_id'].dropna().astype(str).unique()

subs_faculty = mailing_list_subscriptions[
    mailing_list_subscriptions['subscriber_mit_id'].astype(str).isin(responsible_faculty_ids)
]

subs_faculty_10 = subs_faculty.merge(lists_10, on='list_name', how='inner')

# 5) For each such list, compute:
# - number of faculty in these lists (faculty count among members)
# Determine which members are faculty by joining to people
members_with_flag = mailing_list_members.merge(
    people[['MIT_ID','IS_FACULTY']].rename(columns={'MIT_ID':'member_mit_id'}),
    on='member_mit_id', how='left'
)

faculty_members_per_list = (
    members_with_flag[members_with_flag['IS_FACULTY'].astype(str).str.upper().eq('Y')]
    .groupby('list_name')['member_mit_id'].nunique()
    .rename('faculty_in_list')
    .reset_index()
)

# - number of courses associated with those faculty (unique SUBJECT_KEY among responsible faculty who subscribe to the list)
subs_faculty_unique = subs_faculty_10[['list_name','subscriber_mit_id']].drop_duplicates()

subs_with_courses = subs_faculty_unique.merge(
    fac_courses[['responsible_faculty_mit_id','SUBJECT_KEY']].rename(columns={'responsible_faculty_mit_id':'subscriber_mit_id'}),
    on='subscriber_mit_id', how='left'
)

courses_per_list = (
    subs_with_courses.dropna(subset=['SUBJECT_KEY'])
    .groupby('list_name')['SUBJECT_KEY'].nunique()
    .rename('num_courses_for_subscribing_faculty')
    .reset_index()
)

# 6) Assemble final answer: list name, number of faculty in list, number of courses for those faculty
answer = (
    subs_faculty_10[['list_name','member_count']].drop_duplicates()
    .merge(faculty_members_per_list, on='list_name', how='left')
    .merge(courses_per_list, on='list_name', how='left')
    .fillna({'faculty_in_list':0, 'num_courses_for_subscribing_faculty':0})
    .rename(columns={'member_count':'list_member_count'})
)

# The question requests: the name of mailing lists with ten members that they subscribe to, the number of faculty in these lists, and the number of courses associated with those faculty.
# Return columns: ['list_name','faculty_in_list','num_courses_for_subscribing_faculty']
final_answer = answer[['list_name','faculty_in_list','num_courses_for_subscribing_faculty']]

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
