import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['Id','OwnerDisplayName','ViewCount']].copy()
    prepared['Id'] = pd.to_numeric(prepared['Id'], errors='coerce').astype('Int64')
    prepared['ViewCount'] = pd.to_numeric(prepared['ViewCount'], errors='coerce')
    target = prepared[['Id','OwnerDisplayName','ViewCount']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['DisplayName']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_posts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_users = prepared_table_2

# prepared_posts has columns: Id (int), OwnerDisplayName (str), ViewCount (float)
# Ensure ViewCount numeric and handle missing
pp = prepared_posts.copy()
pp['ViewCount'] = pd.to_numeric(pp['ViewCount'], errors='coerce').fillna(0)
pp['OwnerDisplayName'] = pp['OwnerDisplayName'].astype(str)

mornington_views = pp.loc[pp['OwnerDisplayName'].str.strip().str.casefold() == 'mornington', 'ViewCount'].sum()amos_views = pp.loc[pp['OwnerDisplayName'].str.strip().str.casefold() == 'amos', 'ViewCount'].sum()

target = pd.DataFrame({
    'author': ['Mornington', 'Amos'],
    'total_views': [mornington_views, amos_views]
})

difference = mornington_views - amos_views
final_answer = difference

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
