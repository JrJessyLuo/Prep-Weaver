import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['id', 'hasContentWarning']].drop_duplicates(subset=['id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','fmt','sts']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_formats = prepared_table_2

# prepared_cards and prepared_formats are produced from table_1 and table_2 respectively
merged = prepared_cards.merge(prepared_formats, on='id', how='inner')

# Filter to format == 'commander' and legal status
subset = merged[(merged['fmt'].str.lower() == 'commander') & (merged['sts'].str.lower() == 'legal')]

# Compute percentage of those without a content warning (assuming 1=yes, 0=no)
if len(subset) == 0:
    result = 0.0
else:
    no_warning = (subset['hasContentWarning'] == 0).sum()
    result = 100.0 * no_warning / len(subset)

answer = result

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
