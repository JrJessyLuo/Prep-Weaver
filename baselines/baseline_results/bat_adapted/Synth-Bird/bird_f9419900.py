import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['id', 'availability']]
    prepared = prepared.drop_duplicates(subset=['id'], keep='first')
    target = prepared[['id', 'availability']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['id','attribute','value']].copy()
    prepared['id'] = pd.to_numeric(prepared['id'], errors='coerce').astype('Int64')
    prepared = prepared.dropna(subset=['id','attribute','value'])
    prepared = prepared.drop_duplicates(subset=['id','attribute','value']).reset_index(drop=True)
    target = prepared[['id','attribute','value']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_localizations = prepared_table_2

# prepared_cards and prepared_localizations are the synthesized per-table outputs
# Join on card id
df = prepared_cards.merge(prepared_localizations, on='id', how='left')

# Heuristic: consider a card available in Chinese Simplified if any localization row
# mentions Chinese Simplified in attribute or value. Common indicators include language tags
# like 'language', 'name', 'text', etc., with value mentioning 'Chinese Simplified', 'zh-Hans', or 'Simplified Chinese'.

def is_zh_simplified_row(attr, val):
    s_attr = ('' if pd.isna(attr) else str(attr)).lower()
    s_val = ('' if pd.isna(val) else str(val)).lower()
    indicators = [
        'chinese simplified', 'simplified chinese', 'zh-hans', 'zh_cn', 'zh-cn', 'zh-sg'
    ]
    # sometimes attribute itself can be the language name
    return any(tok in s_attr for tok in indicators) or any(tok in s_val for tok in indicators)

# Mark cards with any zh-simplified localization
zh_cards = (
    df.assign(_zh=is_zh_simplified_row(df['attribute'], df['value']))
      .groupby('id')['_zh']
      .max()
      .reset_index()
)

# Total unique cards (from cards table)
total_cards = prepared_cards['id'].nunique()

# Count cards with zh simplified
zh_count = zh_cards['_zh'].fillna(False).sum()

percentage = float(zh_count) / float(total_cards) * 100.0 if total_cards else 0.0

result = pd.DataFrame({
    'total_cards': [total_cards],
    'zh_simplified_cards': [int(zh_count)],
    'percentage_zh_simplified': [percentage]
})

target = result

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
