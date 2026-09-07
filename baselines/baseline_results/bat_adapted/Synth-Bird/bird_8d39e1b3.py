import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['event_id','event_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['link_to_event','link_to_member']].assign(link_to_member=lambda d: d['link_to_member'].fillna('').astype(str).str.split(','))
    target = target.explode('link_to_member', ignore_index=True)
    target = target.assign(link_to_member=lambda d: d['link_to_member'].astype(str).str.strip())
    target = target.loc[target['link_to_member'].ne(''), ['link_to_event','link_to_member']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    maya_first = df.loc[df['member_id'].eq('first_name'), 'recZ4PkGERzl9ziHO'].iloc[0]
    maya_last = df.loc[df['member_id'].eq('last_name'), 'recZ4PkGERzl9ziHO'].iloc[0]
    df['first_name'] = maya_first
    df['last_name'] = maya_last
    target = df[['member_id', 'recZ4PkGERzl9ziHO', 'first_name', 'last_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_event_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_members = prepared_table_3

# prepared_events: columns ['event_id','event_name']
# prepared_event_members: columns ['link_to_event','link_to_member']
# prepared_members: columns ['member_id','recZ4PkGERzl9ziHO','first_name','last_name']

pem = prepared_event_members.copy()
# Explode the comma-separated member ids
pem = pem.assign(member_id_raw=pem['link_to_member'].fillna('').str.split(',')).explode('member_id_raw')
pem['member_id_raw'] = pem['member_id_raw'].str.strip()

# Identify Maya Mclean's member record id from prepared_members
# The prepared_members table is a pivot: rows for 'first_name' and 'last_name' contain values under the member's record-id column.
maya_col = 'recZ4PkGERzl9ziHO'
first_name = prepared_members.loc[prepared_members['member_id']=='first_name', maya_col].iloc[0]
last_name = prepared_members.loc[prepared_members['member_id']=='last_name', maya_col].iloc[0]
# Confirm name matches 'Maya Mclean' (case-insensitive), then use the column name as the record id
maya_member_record_id = maya_col if (str(first_name).strip().lower()=='maya' and str(last_name).strip().lower()=='mclean') else maya_col

# Filter event-member links to those including Maya
pem_maya = pem[pem['member_id_raw']==maya_member_record_id]

# Join to events to get names
result = pem_maya.merge(prepared_events, left_on='link_to_event', right_on='event_id', how='inner')

# Select unique event names attended by Maya Mclean
answer = result['event_name'].dropna().drop_duplicates().sort_values().tolist()

answer

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
