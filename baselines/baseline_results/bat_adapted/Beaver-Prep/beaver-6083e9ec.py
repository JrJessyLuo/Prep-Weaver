import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG']].copy()
    prepared = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY'])
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_NAME_LONG']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['FCLT_BUILDING_KEY','ADDRESS_PURPOSE','STREET_NUMBER','STREET_NUMBER_SUFFIX','PRE_DIRECTIONAL','STREET_NAME','STREET_SUFFIX','POST_DIRECTIONAL','CITY','STATE','POSTAL_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_8'])
prepared_rooms_by_org = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_building_addresses = prepared_table_3

# Assume the three prepared tables exist: prepared_rooms_by_org, prepared_buildings, prepared_building_addresses
# 1) Identify rows for the History department; allow common variants
hist_mask = prepared_rooms_by_org['ORGANIZATION_NAME'].str.contains(r'\bHISTORY\b|\bHIST\b', case=False, na=False)
hist_rooms = prepared_rooms_by_org.loc[hist_mask].copy()

# 2) Get the most recent fiscal period per building to represent current occupancy
# If FISCAL_PERIOD is numeric-like string YYYYMM, coerce to int for ordering
fp = pd.to_numeric(hist_rooms['FISCAL_PERIOD'], errors='coerce')
hist_rooms = hist_rooms.assign(_FP=fp)
latest_by_bldg = hist_rooms.sort_values('_FP').groupby('FCLT_BUILDING_KEY', as_index=False).tail(1)

# 3) Join to buildings (optional metadata) and addresses
hist_with_bldg = latest_by_bldg.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Prefer STREET purpose for physical street address; if multiple, pick STREET else fallback to MAIL or E911_1
addr_pref_order = ['STREET', 'E911_1', 'MAIL']
# Rank addresses by preference within each building
addr = prepared_building_addresses.copy()
addr['_addr_rank'] = addr['ADDRESS_PURPOSE'].apply(lambda x: addr_pref_order.index(x) if isinstance(x, str) and x in addr_pref_order else len(addr_pref_order))
addr_best = addr.sort_values(['FCLT_BUILDING_KEY', '_addr_rank']).groupby('FCLT_BUILDING_KEY', as_index=False).first()

hist_with_addr = hist_with_bldg.merge(addr_best.drop(columns=['_addr_rank']), on='FCLT_BUILDING_KEY', how='left')

# 4) Build street address string
parts = [
    hist_with_addr['STREET_NUMBER'].fillna('').astype(str).str.strip(),
    hist_with_addr['STREET_NUMBER_SUFFIX'].fillna('').astype(str).str.strip(),
    hist_with_addr['PRE_DIRECTIONAL'].fillna('').astype(str).str.strip(),
    hist_with_addr['STREET_NAME'].fillna('').astype(str).str.strip(),
    hist_with_addr['STREET_SUFFIX'].fillna('').astype(str).str.strip(),
    hist_with_addr['POST_DIRECTIONAL'].fillna('').astype(str).str.strip(),
]
# Join non-empty parts with spaces and collapse multiple spaces
street = (
    pd.Series([' '.join([p for p in row if p and p.lower() != "nan"]).strip() for row in zip(*parts)])
      .str.replace(r'\s+', ' ', regex=True)
)

result = hist_with_addr.assign(
    building_key=hist_with_addr['FCLT_BUILDING_KEY'],
    street_address=street,
    city=hist_with_addr['CITY'],
    state=hist_with_addr['STATE'],
    postal_code=hist_with_addr['POSTAL_CODE']
)[['building_key', 'street_address', 'city', 'state', 'postal_code']].drop_duplicates()

# 'result' holds the current building key and address info for the History department
answer = result

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
