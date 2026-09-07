import pandas as pd
import numpy as np

def _prep_1(table_1):
    import pandas as pd
    base_cols = [c for c in ['id','isStarter','name','setCode'] if c in table_1.columns]
    legality_cols = [c for c in table_1.columns if c == 'legalities' or c.startswith('legalities.') or c.startswith('legalities_') or c.startswith('legalities ')]
    target = table_1.loc[:, base_cols].copy()
    target['legalities'] = table_1[legality_cols].apply(lambda r: {k.replace('legalities.','').replace('legalities_','').replace('legalities ',''): v for k, v in r.to_dict().items() if pd.notna(v)}, axis=1) if len(legality_cols) > 0 else [{} for _ in range(len(table_1))]
    target = target.loc[:, ['id','isStarter','legalities','name','setCode']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['code','type','name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_sets = prepared_table_2

# Assume prepared_cards has columns: id, isStarter, legalities, name, setCode
# and prepared_sets has columns: code, type, name

cards = prepared_cards.copy()
sets_ = prepared_sets.copy()

# Join cards to sets so we can optionally use set metadata if needed
cards_sets = cards.merge(sets_, left_on='setCode', right_on='code', how='left')

# Define helper to test if any legality status is 'restricted'
# legalities may be a dict-like or a JSON-serialized string; try both

def has_restricted(leg):
    if leg is None or (isinstance(leg, float) and pd.isna(leg)):
        return False
    if isinstance(leg, str):
        # try to parse JSON-like strings
        try:
            leg_dict = json.loads(leg)
        except Exception:
            return False
    elif isinstance(leg, dict):
        leg_dict = leg
    else:
        return False
    # any format with status 'restricted'
    return any((isinstance(v, dict) and v.get('status') == 'restricted') or (isinstance(v, str) and v == 'restricted') for v in leg_dict.values())

mask_starter = cards_sets['isStarter'] == 1
mask_restricted = cards_sets['legalities'].apply(has_restricted)

answer = int((cards_sets[mask_starter & mask_restricted]['id']).nunique())

answer

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
