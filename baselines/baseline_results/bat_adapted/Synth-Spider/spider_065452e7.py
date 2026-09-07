import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Book_ID','Title','Pages']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Book_ID','rk']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
books_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
reviews_prepared = prepared_table_2

# Assume books_prepared and reviews_prepared are synthesized as specified.
# Ensure numeric types for correct comparison/join semantics.
books_prepared['Book_ID'] = pd.to_numeric(books_prepared['Book_ID'], errors='coerce')
books_prepared['Pages'] = pd.to_numeric(books_prepared['Pages'], errors='coerce')
reviews_prepared['Book_ID'] = pd.to_numeric(reviews_prepared['Book_ID'], errors='coerce')
reviews_prepared['rk'] = pd.to_numeric(reviews_prepared['rk'], errors='coerce')

# Integrate
merged = books_prepared.merge(reviews_prepared, on='Book_ID', how='left')

# Find the book with the smallest number of pages and return its rank (rk)
min_pages = merged['Pages'].min()
answer_row = merged.loc[merged['Pages'] == min_pages]
# If multiple books tie, pick the first; if rk missing, it will return NaN
answer_value = answer_row['rk'].iloc[0] if not answer_row.empty else None

result = pd.DataFrame({'answer': [answer_value]})

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
