import pandas as pd

# Source tables from the provided `tables` dict
space_detail = tables['table_3']
fac_rooms = tables['table_4']
buildings = tables['table_6']

# ============= STEP 1: Merge SPACE_DETAIL with BUILDINGS for names =============
left = space_detail[['BUILDING_KEY', 'FLOOR_KEY', 'BUILDING_COMPONENT', 'BUILDING_ROOM', 'ROOM_SQUARE_FOOTAGE']].copy()
right = buildings[['BUILDING_KEY', 'BUILDING_NAME']].copy()

left['BUILDING_KEY'] = left['BUILDING_KEY'].astype(str)
right['BUILDING_KEY'] = right['BUILDING_KEY'].astype(str)

sd_merged = left.merge(right, on='BUILDING_KEY', how='left')

# Safety: ensure numeric room sqft for aggregations
sd_merged['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(sd_merged['ROOM_SQUARE_FOOTAGE'], errors='coerce')

# ============= STEP 2: Aggregate by BUILDING_COMPONENT & BUILDING_NAME =========
# Compute per-room sqft (sum in case of duplicate rows for a room)
room_sqft_per_room = (
    sd_merged.groupby(['BUILDING_COMPONENT', 'BUILDING_NAME', 'BUILDING_ROOM'], dropna=False)['ROOM_SQUARE_FOOTAGE']
    .sum(min_count=1)
    .reset_index(name='ROOM_SQFT_SUM')
)

# Aggregate to component/building_name level
agg_sd = (
    room_sqft_per_room.groupby(['BUILDING_COMPONENT', 'BUILDING_NAME'], dropna=False)
    .agg(
        TOTAL_ROOM_SQFT=('ROOM_SQFT_SUM', 'sum'),
        TOTAL_ROOMS=('BUILDING_ROOM', 'nunique')
    )
    .reset_index()
)

# Floors: nunique FLOOR_KEY per component/name
floors_agg = (
    sd_merged.groupby(['BUILDING_COMPONENT', 'BUILDING_NAME'], dropna=False)['FLOOR_KEY']
    .nunique()
    .reset_index(name='TOTAL_FLOORS')
)

sd_summary = (
    agg_sd.merge(floors_agg, on=['BUILDING_COMPONENT', 'BUILDING_NAME'], how='left')
)

# ============= STEP 3: FAC_ROOMS org counts by BUILDING_COMPONENT/KEY ==========
# Prepare SPACE_DETAIL key-component mapping
key_comp = (
    space_detail[['BUILDING_KEY', 'BUILDING_COMPONENT']]
    .drop_duplicates()
    .copy()
)
key_comp['BUILDING_KEY'] = key_comp['BUILDING_KEY'].astype(str)

# Prepare FAC_ROOMS with BUILDING_KEY and ORGANIZATION_KEY
fac_rooms_small = fac_rooms[['BUILDING_KEY', 'ORGANIZATION_KEY']].copy()
fac_rooms_small['BUILDING_KEY'] = fac_rooms_small['BUILDING_KEY'].astype(str)

# Join to get component for each FAC_ROOMS row
fac_with_comp = fac_rooms_small.merge(key_comp, on='BUILDING_KEY', how='left')

# Count unique organizations per BUILDING_COMPONENT and BUILDING_KEY, then roll up by component only
org_counts_component_building = (
    fac_with_comp.groupby(['BUILDING_COMPONENT', 'BUILDING_KEY'], dropna=False)['ORGANIZATION_KEY']
    .nunique()
    .reset_index(name='UNIQUE_ORGS_PER_BUILDING_IN_COMPONENT')
)

org_counts_component = (
    org_counts_component_building.groupby(['BUILDING_COMPONENT'], dropna=False)['UNIQUE_ORGS_PER_BUILDING_IN_COMPONENT']
    .sum()
    .reset_index(name='TOTAL_FAC_ORGANIZATIONS')
)

# Attach org counts (component-level) to each (component, building_name) row
sd_summary_with_orgs = sd_summary.merge(org_counts_component, on='BUILDING_COMPONENT', how='left')

# ============= STEP 4: Supervisors via SPACE_SUPERVISOR_USAGE ================
# Skipped due to lack of reliable mapping SPACE_UNIT_KEY -> MIT_ID in provided data.
sd_summary_with_orgs['TOTAL_SUPERVISORS'] = pd.NA
sd_summary_with_orgs['TOTAL_SUPERVISEES'] = pd.NA

# ============= Final output dataframe ========================================
result_df = sd_summary_with_orgs[
    [
        'BUILDING_COMPONENT',
        'BUILDING_NAME',
        'TOTAL_FLOORS',
        'TOTAL_ROOMS',
        'TOTAL_ROOM_SQFT',
        'TOTAL_FAC_ORGANIZATIONS',
        'TOTAL_SUPERVISORS',
        'TOTAL_SUPERVISEES'
    ]
].sort_values(['BUILDING_COMPONENT', 'BUILDING_NAME'], kind='stable').reset_index(drop=True)

# Assign to expected result mapping
result = {"building_component_summary": result_df}