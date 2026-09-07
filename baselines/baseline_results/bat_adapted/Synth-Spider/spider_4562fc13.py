import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['document_id','process_id','process_outcome_code','process_status_code']].copy()
    target['process_outcome_code'] = target['process_outcome_code'].astype('string').str.strip().str.replace(r'[!]+$', '', regex=True)
    target['process_status_code'] = target['process_status_code'].astype('string').str.strip()
    target = target.drop_duplicates(subset=['document_id','process_id','process_outcome_code','process_status_code']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = pd.DataFrame([table_1.iloc[0].to_dict()])
    target.columns = table_1.iloc[0].values
    target = target.iloc[0:0].assign(**{c: [c] for c in target.columns})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['process_status_code','attribute','value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
docs_process = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
outcome_lut = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
status_lut = prepared_table_3

# Assume prepared tables already loaded as dataframes: docs_process, outcome_lut, status_lut
# 1) Filter to the target document
doc = docs_process[docs_process['document_id'] == 0]

# 2) Resolve process outcome description using the header-mapped outcome_lut row
#    The outcome code in docs_process (e.g., 'finish!' or 'start!') may contain punctuation; normalize to match outcome_lut column names
normalize = lambda s: str(s).strip().lower().replace('!', '')

doc = doc.assign(_outcome_col=doc['process_outcome_code'].map(normalize))

# outcome_lut is single-row; extract the matching column's value
outcome_row = outcome_lut.iloc[0]
# Map each row in doc to its outcome description by indexing the outcome_lut row with the normalized column name
outcome_desc = doc['_outcome_col'].map(lambda c: outcome_row.get(c, None))

doc = doc.assign(process_outcome_description=outcome_desc).drop(columns=['_outcome_col'])

# 3) Join status description from status_lut where attribute == 'process_status_description'
status_desc = status_lut[status_lut['attribute'] == 'process_status_description'][['process_status_code', 'value']].rename(columns={'value': 'process_status_description'})

doc = doc.merge(status_desc, on='process_status_code', how='left')

# 4) Select the requested columns for the final answer
answer = doc[['process_outcome_description', 'process_status_description']]

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
