import pandas as pd
import numpy as np

def _prep_1(table_1):
    cards = table_1.loc[:, ['id', 'borderColor']]
    target = cards.drop_duplicates(subset=['id', 'borderColor']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import pandas as pd
    import ast
    import json
    df = table_1.copy()
    df['id_list'] = df['id'].apply(lambda x: x if isinstance(x, list) else (ast.literal_eval(x) if isinstance(x, str) else []))
    df['value_list'] = df['value'].apply(lambda x: x if isinstance(x, list) else (ast.literal_eval(x) if isinstance(x, str) else []))
    df.loc[df['id_list'].apply(lambda v: not isinstance(v, list)), 'id_list'] = df.loc[df['id_list'].apply(lambda v: not isinstance(v, list)), 'id'].apply(lambda s: json.loads(s.replace("'", '"')) if isinstance(s, str) else [])
    df.loc[df['value_list'].apply(lambda v: not isinstance(v, list)), 'value_list'] = df.loc[df['value_list'].apply(lambda v: not isinstance(v, list)), 'value'].apply(lambda s: json.loads(s.replace("'", '"')) if isinstance(s, str) else [])
    df = df[['type','id_list','value_list']].explode(['id_list','value_list'], ignore_index=True)
    df = df.rename(columns={'id_list':'id','value_list':'value'})
    df['id'] = df['id'].astype(str).str.strip().str.strip('"').str.strip("'")
    df = df[df['value'].astype(str).str.split('|').str[1].eq('Banned')]
    target = df[['id','type','value']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
format_status = prepared_table_2

# Prepared inputs: cards, format_status
# 1) Expand the long list columns in format_status into a normalized dataframe of (id, format, status)
ids_list = ast.literal_eval(format_status.loc[0, 'id'])
vals_list = ast.literal_eval(format_status.loc[0, 'value'])

fmt_rows = []
for cid, val in zip(ids_list, vals_list):
    # strip surrounding quotes if present
    cid_clean = cid.strip('"\' )
    # val is like 'format|Status|uuid'
    parts = val.split('|')
    if len(parts) >= 2:
        fmt_rows.append({'id': int(cid_clean) if cid_clean.isdigit() else cid_clean, 'format': parts[0], 'status': parts[1]})
fmt_df = pd.DataFrame(fmt_rows)

# 2) Determine banned cards (any format with status == 'Banned')
banned_ids = fmt_df.loc[fmt_df['status'].str.lower() == 'banned', 'id'].drop_duplicates()

# 3) Join with cards to get borderColor, then count white border
banned_cards = cards.merge(banned_ids.to_frame(name='id'), on='id', how='inner')
answer = int((banned_cards['borderColor'].str.lower() == 'white').sum())

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
