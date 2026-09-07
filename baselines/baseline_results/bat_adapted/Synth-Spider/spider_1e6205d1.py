import pandas as pd
import numpy as np

def _prep_1(table_1):
    names_row = table_1.loc[table_1['University_ID'].eq('University_Name')].iloc[0]
    wide = names_row.drop(labels=['University_ID'])
    target = wide.reset_index()
    target.columns = ['uni_id', 'University_Name']
    target['uni_id'] = target['uni_id'].astype(int)
    target = target[['uni_id', 'University_Name']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['uni_id','Reputation_point','cit_p']].copy()
    target[['uni_id','Reputation_point','cit_p']] = target[['uni_id','Reputation_point','cit_p']].astype('int64')
    target = target[['uni_id','Reputation_point','cit_p']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
universities = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
uni_scores = prepared_table_2

# Assume prepared tables are provided as DataFrames: universities, uni_scores
# Join scores to names
joined = uni_scores.merge(universities, on='uni_id', how='inner')

# Ensure numeric types
joined['Reputation_point'] = pd.to_numeric(joined['Reputation_point'], errors='coerce')
joined['cit_p'] = pd.to_numeric(joined['cit_p'], errors='coerce')

# Get top 3 by reputation (breaking ties by higher cit_p, then by uni_id for determinism)
result = (
    joined.sort_values(by=['Reputation_point', 'cit_p', 'uni_id'], ascending=[False, False, True])
          .loc[:, ['University_Name', 'cit_p']]
          .head(3)
)

target = result.rename(columns={'University_Name': 'name', 'cit_p': 'citation_point'})

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
