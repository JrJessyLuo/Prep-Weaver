import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['cds','school_name','district','county','NumTstTakr','rtype']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['CDSCode','School','District','County','MailCity','StatusType']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_scores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_directory = prepared_table_2

target = prepared_scores.merge(prepared_directory, left_on='cds', right_on='CDSCode', how='inner')
# Restrict to school rows and Fresno mailing city
mask = (target['rtype'] == 'S') & (target['MailCity'].str.strip().str.casefold() == 'fresno')
filtered = target.loc[mask]
# Sum number of test takers across matching schools
answer = int(filtered['NumTstTakr'].astype('Int64').fillna(0).sum())

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
