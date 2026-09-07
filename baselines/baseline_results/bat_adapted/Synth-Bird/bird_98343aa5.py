import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['member_id','first_name','last_name','position']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['event_id','event_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_events = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_table_4 = _prep_4(tables['table_3'])

# No attendance table was provided among the selected tables, so we cannot compute attendance counts.
# Expected integration (if an attendance/RSVP table existed):
# 1) prepared_attendance (member_id, event_id) would be prepared from the attendance source.
# 2) Join prepared_attendance to prepared_members on member_id to get student names.
# 3) Optionally validate event_ids against prepared_events.
# 4) Group by member_id (and name), count distinct event_id, filter > 7, and return names.

# Pseudocode example (requires an attendance table):
# target = prepared_attendance.merge(prepared_members, on='member_id', how='inner')
# counts = target.groupby(['member_id','first_name','last_name'])['event_id'].nunique().reset_index(name='events_attended')
# answer = counts[counts['events_attended'] > 7][['first_name','last_name']]
# answer

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
