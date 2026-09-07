import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['last_name', 'first_name'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['last_name', 'first_name'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['member_id', 'first_name', 'last_name', 'position'])
    # SelectCol
    _cols = [c for c in ['member_id', 'first_name', 'last_name', 'position'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['member_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['member_id'], keep='first').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['event_id', 'event_name', 'event_date', 'type', 'notes', 'location', 'status'])
    # SelectCol
    _cols = [c for c in ['event_id', 'event_name', 'event_date', 'type', 'notes', 'location', 'status'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['event_id', 'event_name'])
    # SelectCol
    _cols = [c for c in ['event_id', 'event_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['event_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['event_id'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['event_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['event_id'], keep='first').reset_index(drop=True)

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
def _prep_4(table_1):
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_events = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_table_4 = _prep_4(tables['table_3'])

# Assume there exists an attendance table (prepared_attendance) with columns: member_id, event_id
# Join members to attendance to count events per member, then filter > 7 and output names.

att = prepared_attendance.merge(prepared_members, on='member_id', how='inner')

# Optionally validate event ids exist by joining to events (not required for counting):
# att = att.merge(prepared_events, on='event_id', how='inner')

counts = att.groupby('member_id').agg(event_count=('event_id', 'nunique')).reset_index()
qualified = counts[counts['event_count'] > 7]
result = qualified.merge(prepared_members[['member_id','first_name','last_name']], on='member_id', how='left')

# Final output: list of student names (first + last)
result['student_name'] = result['first_name'].astype(str) + ' ' + result['last_name'].astype(str)
answer = result[['student_name']].drop_duplicates().sort_values('student_name')

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
