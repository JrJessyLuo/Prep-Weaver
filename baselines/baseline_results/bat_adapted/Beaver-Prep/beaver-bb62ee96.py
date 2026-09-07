import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TERM_CODE','RESPONSIBLE_FACULTY_NAME','responsible_faculty_mit_id','SUBJECT_KEY','SUBJECT_ID','SUBJECT_TITLE','SECTION_ID']].copy()
    prepared = prepared.drop_duplicates(subset=['TERM_CODE','SUBJECT_KEY','SECTION_ID'])
    target = prepared[['TERM_CODE','RESPONSIBLE_FACULTY_NAME','responsible_faculty_mit_id','SUBJECT_KEY','SUBJECT_ID','SUBJECT_TITLE','SECTION_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.reindex(columns=['MIT_ID','FULL_NAME','EMAIL_ADDRESS','IS_FACULTY']).copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
