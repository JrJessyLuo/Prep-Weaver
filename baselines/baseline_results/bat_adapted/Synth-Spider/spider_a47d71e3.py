import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['sid']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df[['sid','bid']] = df['sid_bid'].str.split('_', n=1, expand=True)
    df['sid'] = df['sid'].astype(int)
    df['bid'] = df['bid'].astype(int)
    target = df[['sid','bid','day']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_sailors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_reservations = prepared_table_2

# prepared_sailors: columns [sid]
# prepared_reservations: columns [sid, bid, day]
# Decompose sid_bid during preparation (example):
# prepared_reservations[['sid','bid']] = prepared_reservations['sid_bid'].str.split('_', expand=True)
# prepared_reservations['sid'] = prepared_reservations['sid'].astype(int)

# Find sailors who have not reserved any boat
reservers = prepared_reservations[['sid']].drop_duplicates()
result = prepared_sailors.merge(reservers, on='sid', how='left', indicator=True)
answer = result.loc[result['_merge'] == 'left_only', ['sid']]
answer = answer.sort_values('sid').reset_index(drop=True)
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
