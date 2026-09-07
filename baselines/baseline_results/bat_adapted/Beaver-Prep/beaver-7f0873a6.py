import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_KEY','FLOOR','FLOOR_KEY','ROOM','AREA','ORGANIZATION_NAME','ACCESS_LEVEL']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    floors = table_1[['BUILDING_KEY','FLOOR','FLOOR_KEY','ACCESS_LEVEL']].copy()
    floors['ACCESS_LEVEL'] = pd.to_numeric(floors['ACCESS_LEVEL'], errors='coerce')
    target = floors.groupby(['BUILDING_KEY','FLOOR','FLOOR_KEY'], as_index=False)['ACCESS_LEVEL'].max()
    target = target[['BUILDING_KEY','FLOOR','FLOOR_KEY','ACCESS_LEVEL']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['FAC_BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','ACCESS_LEVEL_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prep_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prep_floors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prep_buildings_meta = prepared_table_3
prepared_table_4 = _prep_4(tables['table_10'])
prep_buildings_addr = prepared_table_4

# Assume the prepared tables already exist: prep_rooms, prep_floors, prep_buildings_meta, prep_buildings_addr

# 1) Filter to Facilities department rooms (e.g., ORGANIZATION_NAME == 'DOF')
rooms_fac = prep_rooms[prep_rooms['ORGANIZATION_NAME'].str.upper() == 'DOF']

# 2) Join floor metadata (if needed for corroboration; not strictly required for metrics)
rooms_fac = rooms_fac.merge(prep_floors[['FLOOR_KEY','ACCESS_LEVEL']].rename(columns={'ACCESS_LEVEL':'ACCESS_LEVEL_FLOOR'}), on='FLOOR_KEY', how='left')

# 3) Join building metadata for building name and building-level access evidence
rooms_fac = rooms_fac.merge(
    prep_buildings_meta[['BUILDING_NUMBER','BUILDING_NAME','ACCESS_LEVEL_CODE']].rename(columns={'BUILDING_NUMBER':'BUILDING_KEY_META'}),
    left_on='BUILDING_KEY', right_on='BUILDING_KEY_META', how='left'
)
# Prefer building name from meta when available, else fall back later to addr table name

# 4) Join building address table for street address (to parse ZIP and City) and alternate building name
rooms_fac = rooms_fac.merge(
    prep_buildings_addr[['BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS']].rename(columns={'BUILDING_NUMBER':'BUILDING_KEY_ADDR','BUILDING_NAME':'BUILDING_NAME_ADDR'}),
    left_on='BUILDING_KEY', right_on='BUILDING_KEY_ADDR', how='left'
)

# 5) Choose building name and access level for output
rooms_fac['BUILDING_NAME_OUT'] = rooms_fac['BUILDING_NAME'].combine_first(rooms_fac['BUILDING_NAME_ADDR'])
# Access level preference: room's ACCESS_LEVEL, else building ACCESS_LEVEL_CODE, else floor access
rooms_fac['ACCESS_LEVEL_OUT'] = rooms_fac['ACCESS_LEVEL'].fillna(rooms_fac['ACCESS_LEVEL_CODE']).fillna(rooms_fac['ACCESS_LEVEL_FLOOR'])

# 6) Parse ZIP and City from BUILDING_STREET_ADDRESS when possible
# Expect formats like "235  ALBANY ST" without city/zip in many rows; if city/zip absent, leave NaN

def parse_city_zip(addr):
    if not isinstance(addr, str):
        return pd.Series({'CITY': pd.NA, 'ZIP': pd.NA})
    # Try patterns like "City, ST 02139" or trailing ZIP 5-digits
    mzip = re.search(r'(\b\d{5})(?:-\d{4})?\b', addr)
    zipc = mzip.group(1) if mzip else pd.NA
    # crude city extraction: token(s) before state code and ZIP
    mcity = re.search(r'([^,\d]+),\s*[A-Z]{2}\s+\d{5}(?:-\d{4})?\b', addr)
    city = mcity.group(1).strip() if mcity else pd.NA
    return pd.Series({'CITY': city, 'ZIP': zipc})

addr_parsed = rooms_fac['BUILDING_STREET_ADDRESS'].apply(parse_city_zip)
rooms_fac = pd.concat([rooms_fac, addr_parsed], axis=1)

# 7) Compute per floor metrics: number of rooms and total area
# Ensure AREA numeric
rooms_fac['AREA_NUM'] = pd.to_numeric(rooms_fac['AREA'], errors='coerce')

floor_group = rooms_fac.groupby(['BUILDING_KEY','FLOOR_KEY','FLOOR'], dropna=False).agg(
    ROOMS_COUNT=('ROOM','nunique'),
    TOTAL_AREA=('AREA_NUM','sum')
).reset_index()

# Attach building name/access/zip/city to floor rows
floor_enriched = floor_group.merge(
    rooms_fac[['BUILDING_KEY','FLOOR_KEY','BUILDING_NAME_OUT','ACCESS_LEVEL_OUT','ZIP','CITY']].drop_duplicates(subset=['BUILDING_KEY','FLOOR_KEY']),
    on=['BUILDING_KEY','FLOOR_KEY'], how='left'
)

# Average area per floor at building level will be computed from building-level aggregation

# 8) Building-level subtotals
bldg_totals = floor_group.groupby('BUILDING_KEY', dropna=False).agg(
    ROOMS_COUNT=('ROOMS_COUNT','sum'),
    TOTAL_AREA=('TOTAL_AREA','sum'),
    FLOORS=('FLOOR_KEY','nunique')
).reset_index()
bldg_totals['AVG_AREA_PER_FLOOR'] = bldg_totals['TOTAL_AREA'] / bldg_totals['FLOORS']

# Attach building display info (no ZIP/CITY per requirement for subtotals)
bldg_totals = bldg_totals.merge(
    rooms_fac[['BUILDING_KEY','BUILDING_NAME_OUT','ACCESS_LEVEL_OUT']].drop_duplicates(subset=['BUILDING_KEY']),
    on='BUILDING_KEY', how='left'
)

# 9) Grand total across all buildings (no ZIP/CITY)
grand = pd.DataFrame({
    'BUILDING_KEY': ['ALL BUILDINGS'],
    'FLOOR_KEY': [pd.NA],
    'FLOOR': [pd.NA],
    'ROOMS_COUNT': [int(floor_group['ROOMS_COUNT'].sum())],
    'TOTAL_AREA': [floor_group['TOTAL_AREA'].sum()],
    'AVG_AREA_PER_FLOOR': [bldg_totals['AVG_AREA_PER_FLOOR'].mean()],
    'BUILDING_NAME_OUT': ['Grand Total'],
    'ACCESS_LEVEL_OUT': [pd.NA],
    'ZIP': [pd.NA],
    'CITY': [pd.NA],
    'ROW_TYPE': ['GRAND_TOTAL']
})

# 10) Shape floor-level rows for output
floor_out = floor_enriched.copy()
floor_out['AVG_AREA_PER_FLOOR'] = pd.NA  # only for building/grand rows per requirement
floor_out['ROW_TYPE'] = 'FLOOR'

# 11) Shape building subtotal rows for output
bldg_out = bldg_totals.copy()
bldg_out['FLOOR_KEY'] = pd.NA
bldg_out['FLOOR'] = pd.NA
bldg_out['ZIP'] = pd.NA
bldg_out['CITY'] = pd.NA
bldg_out['ROW_TYPE'] = 'BUILDING_TOTAL'

# 12) Formatting: round to integers and add commas
def fmt_int(x):
    try:
        xi = int(round(float(x)))
        return f"{xi:,}"
    except Exception:
        return ''

for df in [floor_out, bldg_out, grand]:
    df['ROOMS_COUNT'] = df['ROOMS_COUNT'].apply(fmt_int)
    df['TOTAL_AREA'] = df['TOTAL_AREA'].apply(fmt_int)
    if 'AVG_AREA_PER_FLOOR' in df.columns:
        df['AVG_AREA_PER_FLOOR'] = df['AVG_AREA_PER_FLOOR'].apply(lambda v: fmt_int(v) if pd.notna(v) else '')

# 13) Choose columns and concatenate in desired order
cols = ['BUILDING_KEY','FLOOR_KEY','FLOOR','ROOMS_COUNT','TOTAL_AREA','AVG_AREA_PER_FLOOR','BUILDING_NAME_OUT','ACCESS_LEVEL_OUT','ZIP','CITY','ROW_TYPE']
result = pd.concat([
    floor_out[cols],
    bldg_out[cols],
    grand[cols]
], ignore_index=True)

# 14) Sort: by building key, then floors; keep grand total at end
result['sort_bldg'] = result['BUILDING_KEY'].astype(str)
result['sort_floor'] = result['FLOOR'].astype(str)
result['row_rank'] = result['ROW_TYPE'].map({'FLOOR':0,'BUILDING_TOTAL':1,'GRAND_TOTAL':2})
result = result.sort_values(by=['row_rank','sort_bldg','sort_floor']).drop(columns=['sort_bldg','sort_floor','row_rank'])

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
