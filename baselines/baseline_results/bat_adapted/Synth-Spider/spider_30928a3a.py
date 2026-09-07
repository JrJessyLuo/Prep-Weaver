import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    id_vars = ['artistID']
    value_vars = [c for c in df.columns if c not in id_vars]
    long = df.melt(id_vars='artistID', value_vars=value_vars, var_name='artistID_col', value_name='value')
    long['artistID'] = long['artistID_col'].astype(str)
    wide = long.pivot(index='artistID', columns='artistID', values='value')
    wide = wide.reset_index()
    wide = wide.rename(columns={'fname': 'first_name', 'lname': 'last_name'})
    wide['last_name'] = wide['last_name'] if 'last_name' in wide.columns else pd.NA
    target = wide[['artistID', 'first_name', 'last_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_paintings = prepared_table_2

# prepared_artists: columns [artistID, first_name, last_name]
# prepared_paintings: columns [paintingID, painterID, medium]

# Join artists to their paintings
ap = prepared_artists.merge(prepared_paintings, left_on='artistID', right_on='painterID', how='inner')

# Normalize medium text for robust matching
m = ap.copy()
m['medium_norm'] = m['medium'].astype(str).str.strip().str.lower()

# Identify artists with at least one oil painting and at least one lithographic work
has_oil = m[m['medium_norm'].str.contains('\boil\b', na=False)].groupby('artistID').size().rename('oil_cnt')
has_litho = m[m['medium_norm'].str.contains('lithograph|lithographic|lithography', na=False)].groupby('artistID').size().rename('litho_cnt')

both = (pd.concat([has_oil, has_litho], axis=1).fillna(0))
both = both[(both['oil_cnt'] > 0) & (both['litho_cnt'] > 0)].reset_index()[['artistID']]

# Return first and last names of matched artists
result = both.merge(prepared_artists[['artistID','first_name','last_name']], on='artistID', how='left')
answer = result[['first_name','last_name']].drop_duplicates().reset_index(drop=True)

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
