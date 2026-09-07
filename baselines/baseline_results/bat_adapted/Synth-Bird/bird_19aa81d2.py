import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['member_id','attribute','value']].copy()
    target = target.dropna(subset=['member_id','attribute'])
    target = target.assign(member_id=target['member_id'].astype(str).str.strip(), attribute=target['attribute'].astype(str).str.strip(), value=target['value'].astype(str).where(target['value'].notna(), None))
    target = target.drop_duplicates(subset=['member_id','attribute','value']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df = df.rename(columns={df.columns[0]: 'field'})
    long = df.melt(id_vars=['field'], var_name='zip_code', value_name='value')
    wide = long.pivot(index='zip_code', columns='field', values='value').reset_index()
    wide.columns = [str(c) for c in wide.columns]
    wide['zip_code'] = wide['zip_code'].astype(str).str.replace(r'\D', '', regex=True).str.zfill(5)
    wide = wide.rename(columns={'shi': 'city', 'xian': 'county'})
    for col in ['state','city','county','type']: wide[col] = wide[col] if col in wide.columns else None
    target = wide[['zip_code','state','city','county','type']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
members_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
zip_geo_pivot = prepared_table_2

# Prepared tables assumed available: members_attributes, zip_geo_pivot
# 1) Extract members' hometown-related ZIPs from attributes (e.g., attribute in ['hometown_zip','zip','hometown']).
zip_attrs = ['hometown_zip', 'zip', 'zipcode', 'postal_code', 'hometown_zip_code']
member_zip = members_attributes[members_attributes['attribute'].str.lower().isin(zip_attrs)].copy()
# Normalize ZIP as 5-digit string
member_zip['zip_norm'] = member_zip['value'].astype(str).str.extract(r'(\d{5})', expand=False)
member_zip = member_zip.dropna(subset=['zip_norm']).rename(columns={'zip_norm':'zip_code'})[['member_id','zip_code']].drop_duplicates()

# 2) Join to ZIP geo to get state
mx = member_zip.merge(zip_geo_pivot[['zip_code','state']], on='zip_code', how='left')

# 3) Count members whose hometown is in Maryland (match 'MD' or 'Maryland')
md_mask = mx['state'].str.upper().isin(['MD','MARYLAND'])
md_members = mx.loc[md_mask, 'member_id'].drop_duplicates()
answer = len(md_members)

result = pd.DataFrame({'count_members_hometowns_in_Maryland':[answer]})

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
