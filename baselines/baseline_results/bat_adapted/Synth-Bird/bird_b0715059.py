import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','superhero_name','publisher_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_superheroes = prepared_table_1

target = prepared_superheroes
# If a separate publishers lookup exists elsewhere, join to it by publisher_id to resolve 'Dark Horse Comics'.
# For this single-table setup, assume publisher_id values map to publishers externally and count rows matching that publisher.
# Example with a hypothetical prepared_publishers table:
# target = prepared_superheroes.merge(prepared_publishers, left_on='publisher_id', right_on='publisher_id', how='left')
# answer = (target.publisher_name == 'Dark Horse Comics').sum()

# If no lookup table is available in the selection, and publisher names are not present here,
# BAT should defer name-to-id resolution to cross-table integration. The per-table prep remains as above.

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
