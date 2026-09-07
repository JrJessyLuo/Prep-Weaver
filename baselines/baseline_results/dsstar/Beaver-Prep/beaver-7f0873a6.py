import pandas as pd

# Source tables from provided `tables` dict
rooms = tables['table_4']        # FCLT_ROOMS.pkl
floor  = tables['table_8']       # FCLT_FLOOR.pkl
bldg   = tables['table_7']       # FCLT_BUILDING.pkl

# Select available building columns among those requested
requested_bldg_cols = [
    'FCLT_BUILDING_KEY',
    'BUILDING_NAME_LONG',
    'ACCESS_LEVEL_NAME',
    'BUILDING_NUMBER',
    'ZIP_CODE',
    'CITY'
]
bldg_cols = [c for c in requested_bldg_cols if c in bldg.columns]

# Join rooms -> floor on FCLT_FLOOR_KEY to get building-floor linkage
rooms_floor = rooms.merge(
    floor[['FCLT_FLOOR_KEY','FCLT_BUILDING_KEY']].drop_duplicates(),
    on='FCLT_FLOOR_KEY',
    how='left',
    suffixes=('','_from_floor')
)

# Join -> building on FCLT_BUILDING_KEY to bring building attributes
merged = rooms_floor.merge(
    bldg[bldg_cols].drop_duplicates(),
    on='FCLT_BUILDING_KEY',
    how='left'
)

# Prepare base columns
base_cols = ['FCLT_BUILDING_KEY','FCLT_FLOOR_KEY','AREA']
for c in ['BUILDING_NAME_LONG','ACCESS_LEVEL_NAME','ZIP_CODE','CITY']:
    if c not in merged.columns:
        merged[c] = pd.NA

# Aggregate by building + floor
grp_cols = ['FCLT_BUILDING_KEY','FCLT_FLOOR_KEY']
agg_floor = (
    merged
    .groupby(grp_cols, dropna=False)
    .agg(
        ROOMS=('AREA','size'),
        TOTAL_AREA=('AREA','sum'),
        BUILDING_NAME_LONG=('BUILDING_NAME_LONG','first'),
        ACCESS_LEVEL_NAME=('ACCESS_LEVEL_NAME','first'),
        ZIP_CODE=('ZIP_CODE','first'),
        CITY=('CITY','first')
    )
    .reset_index()
)

# Compute average area per floor:
# Based on interpretation: average area per floor within the same building
# For each building, take mean of TOTAL_AREA across its floors
avg_per_bldg = agg_floor.groupby('FCLT_BUILDING_KEY', dropna=False)['TOTAL_AREA'].transform('mean')
agg_floor['AVG_AREA_PER_FLOOR'] = avg_per_bldg

# Building-level subtotals (exclude ZIP and CITY per requirement)
bldg_subtotals = (
    agg_floor
    .groupby('FCLT_BUILDING_KEY', dropna=False)
    .agg(
        ROOMS=('ROOMS','sum'),
        TOTAL_AREA=('TOTAL_AREA','sum'),
        BUILDING_NAME_LONG=('BUILDING_NAME_LONG','first'),
        ACCESS_LEVEL_NAME=('ACCESS_LEVEL_NAME','first')
    )
    .reset_index()
)
bldg_subtotals['FCLT_FLOOR_KEY'] = 'Subtotal'
bldg_subtotals['AVG_AREA_PER_FLOOR'] = bldg_subtotals['TOTAL_AREA'] / agg_floor.groupby('FCLT_BUILDING_KEY', dropna=False)['FCLT_FLOOR_KEY'].transform('nunique')
# Ensure ZIP and CITY excluded in subtotals
bldg_subtotals['ZIP_CODE'] = pd.NA
bldg_subtotals['CITY'] = pd.NA

# Grand total (exclude ZIP and CITY)
grand = pd.DataFrame({
    'FCLT_BUILDING_KEY': ['Grand Total'],
    'FCLT_FLOOR_KEY': ['Grand Total'],
    'ROOMS': [agg_floor['ROOMS'].sum()],
    'TOTAL_AREA': [agg_floor['TOTAL_AREA'].sum()],
    'AVG_AREA_PER_FLOOR': [agg_floor['TOTAL_AREA'].sum() / agg_floor['FCLT_FLOOR_KEY'].nunique()],
    'BUILDING_NAME_LONG': [pd.NA],
    'ACCESS_LEVEL_NAME': [pd.NA],
    'ZIP_CODE': [pd.NA],
    'CITY': [pd.NA]
})

# Combine detail + subtotals per building, then grand total
detail_cols = [
    'FCLT_BUILDING_KEY','FCLT_FLOOR_KEY','ROOMS','TOTAL_AREA','AVG_AREA_PER_FLOOR',
    'BUILDING_NAME_LONG','ACCESS_LEVEL_NAME','ZIP_CODE','CITY'
]
detail = agg_floor[detail_cols].copy()

# Order: details by building then floor, followed by each building subtotal, then grand total
# Create ordering helper
detail['_order_building'] = detail['FCLT_BUILDING_KEY'].astype(str)
detail['_order_floor'] = detail['FCLT_FLOOR_KEY'].astype(str)

bldg_sub = bldg_subtotals[detail_cols].copy()
bldg_sub['_order_building'] = bldg_sub['FCLT_BUILDING_KEY'].astype(str)
bldg_sub['_order_floor'] = 'ZZZ_Subtotal'

grand['_order_building'] = 'ZZZZ_Grand'
grand['_order_floor'] = 'ZZZZ_Grand'

combined = pd.concat([detail, bldg_sub, grand], ignore_index=True)

# Formatting numbers: round to integers and thousands separators
for col in ['ROOMS','TOTAL_AREA','AVG_AREA_PER_FLOOR']:
    combined[col] = combined[col].round(0).astype('Int64')

def fmt_int_with_commas(series):
    # Keep NA as empty, otherwise format with commas
    return series.map(lambda x: ("" if pd.isna(x) else f"{int(x):,}"))

for col in ['ROOMS','TOTAL_AREA','AVG_AREA_PER_FLOOR']:
    combined[col] = fmt_int_with_commas(combined[col])

# Final column ordering and sorting
final_cols = [
    'FCLT_BUILDING_KEY','FCLT_FLOOR_KEY','ROOMS','TOTAL_AREA','AVG_AREA_PER_FLOOR',
    'BUILDING_NAME_LONG','ACCESS_LEVEL_NAME','ZIP_CODE','CITY'
]
combined = combined.sort_values(by=['_order_building','_order_floor']).drop(columns=['_order_building','_order_floor'])
final_df = combined[final_cols].reset_index(drop=True)

# Assign to result dict as required
result = {
    'building_floor_room_area_summary': final_df
}