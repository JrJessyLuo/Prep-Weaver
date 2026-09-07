import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['event_id','event_name','event_date','lx','status']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.rename(columns={'link_to_event':'event_id'})
    long = df.melt(id_vars=['event_id'], var_name='source_col', value_name='member_id')
    long['member_id'] = long['member_id'].astype('string')
    long = long[long['member_id'].notna() & (long['member_id'].str.strip() != '')]
    target = long[['event_id','member_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
events_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
attendance_prepared = prepared_table_2

# events_prepared expected columns: ['event_id','event_name','event_date','lx','status']
# attendance_prepared expected columns: ['event_id','member_id']

# Join attendance to events
att_events = attendance_prepared.merge(events_prepared[['event_id','lx']], on='event_id', how='inner')

# Count attendees per event
att_counts = att_events.groupby('event_id', as_index=False)['member_id'].nunique().rename(columns={'member_id':'attendee_count'})

# Keep only events with >10 attendees
popular_events = att_counts[att_counts['attendee_count'] > 10]

# Label events as meetings via events table
popular_with_type = popular_events.merge(events_prepared[['event_id','lx']], on='event_id', how='left')

# Count how many are meetings (case-insensitive match to 'Meeting')
answer = (popular_with_type['lx'].str.strip().str.lower() == 'meeting'.lower()).sum()

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
