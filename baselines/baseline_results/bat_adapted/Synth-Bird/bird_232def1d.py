import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','layout']].drop_duplicates(subset=['id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','sts_premodern']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[:, ['id', 'language', 'text']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
cards_base = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
formats_status = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
card_texts = prepared_table_3

# Assume prepared tables are provided as DataFrames: cards_base, formats_status, card_texts

# Join cards with Premodern status
cf = cards_base.merge(formats_status, on='id', how='inner')

# Keep only English text entries and match the exact ruling sentence
ct_en = card_texts[card_texts['language'] == 'English']
ct_match = ct_en[ct_en['text'].fillna('').str.contains(r'^This is a triggered mana ability\.$', regex=True) |
                 ct_en['text'].fillna('').str.contains(r'(^|\n)This is a triggered mana ability\.(\n|$)')]

# Join to get only cards that have the ruling text
cft = cf.merge(ct_match[['id']].drop_duplicates(), on='id', how='inner')

# Premodern format filter: keep cards with a positive/eligible status
# Treat statuses like 'Legal', 'Restricted', 'Banned' explicitly; typically 'Legal' indicates inclusion.
# The question asks for cards "with pre-modern format"; interpret as sts_premodern == 'Legal'.
cft_pm = cft[cft['sts_premodern'].fillna('') == 'Legal']

# Exclude cards with multiple faces by layout; keep only single-face layouts such as 'normal'
# Common multi-face layouts include: 'transform', 'modal_dfc', 'split', 'flip', 'meld', 'adventure', 'double_faced_token', etc.
multi_layouts = {'transform','modal_dfc','split','flip','meld','adventure','double_faced_token','reversible_card'}
single_face = cft_pm[~cft_pm['layout'].fillna('').isin(multi_layouts)]

# Count distinct cards matching criteria
answer = single_face['id'].nunique()

result = pd.DataFrame({'count': [answer]})

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
