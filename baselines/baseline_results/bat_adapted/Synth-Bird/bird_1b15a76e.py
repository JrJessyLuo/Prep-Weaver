import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1.copy()
    source = source.rename(columns={'printRarity': 'rarity'})
    target = source[['id', 'rarity']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','rq','nr']].copy()
    target['rq'] = pd.to_datetime(target['rq'], errors='coerce').dt.strftime('%Y-%m-%d')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_rulings = prepared_table_2

# Assume prepared_cards and prepared_rulings are dataframes produced per targets above.
# Normalize date strings to a common format and match 01/02/2007 in either MM/DD/YYYY or DD/MM/YYYY inputs.

def parse_date_mdy_dmy(s):
    # try ISO first
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%m-%d-%Y", "%d-%m-%Y"):
        try:
            return pd.to_datetime(s, format=fmt, errors='raise')
        except Exception:
            continue
    return pd.NaT

rul = prepared_rulings.copy()
rul['rq_dt'] = rul['rq'].apply(parse_date_mdy_dmy)

cards = prepared_cards.copy()
# Filter to print rarity exactly 'print' (case-insensitive, trims spaces)
cards['rarity_norm'] = cards['rarity'].astype(str).str.strip().str.lower()
cards_print = cards[cards['rarity_norm'] == 'print'][['id']]

merged = cards_print.merge(rul[['id','rq_dt','nr']], on='id', how='inner')

# Target date is 01/02/2007; interpret as exact calendar day regardless of locale after parsing
target_day = pd.Timestamp(year=2007, month=2, day=1)
result_count = merged[merged['rq_dt'] == target_day].shape[0]

answer = result_count

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
