import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    t = df.set_index('member_id').T.reset_index().rename(columns={'index':'member_id'})
    t = t.rename(columns={t.columns[1]:'attribute', t.columns[2]:'value'})
    wide = t.pivot_table(index='member_id', columns='attribute', values='value', aggfunc='first').reset_index()
    wide.columns = [c if isinstance(c, str) else c for c in wide.columns]
    target = wide[['member_id','position','t_shirt_size','link_to_major']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['major_id','value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_majors = prepared_table_2

# prepared_members and prepared_majors are the synthesized per-table outputs
# Join members to majors using the semantic key
joined = prepared_members.merge(prepared_majors, how='left', left_on='link_to_major', right_on='major_id')

# Determine Business affiliation: either position indicates Business or major value mentions Business
# Normalize text for robust matching
pos = joined['position'].astype(str).str.lower()
val = joined['value'].astype(str).str.lower()

is_business = pos.str.contains('business', na=False) | val.str.contains('business', na=False)

# Count members with Medium t-shirt size among Business-affiliated members
answer = int(joined[is_business & (joined['t_shirt_size'].astype(str).str.strip().str.lower() == 'medium')].shape[0])

result = {'answer': answer}

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
