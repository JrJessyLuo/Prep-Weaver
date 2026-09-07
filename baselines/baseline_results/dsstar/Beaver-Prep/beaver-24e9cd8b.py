import pandas as pd
import numpy as np

# Input tables already loaded in `tables` dict per guideline
fac_building = tables['table_2']
fac_floor = tables['table_7']
fclt_floor_hist = tables['table_5']
fac_organization = tables['table_10']  # may or may not be used

# 1) Select/rename relevant columns from FAC_BUILDING
b_cols = [
    'FAC_BUILDING_KEY',
    'BUILDING_NUMBER',
    'BUILDING_NAME_LONG',
    'SITE',
    'CAMPUS_SECTOR',
    'OWNERSHIP_TYPE',
    'ASSIGNABLE_AREA',
    'CITY',
    'STATE'
]
b_available = [c for c in b_cols if c in fac_building.columns]
fac_building_sel = fac_building[b_available].copy()

rename_map = {
    'FAC_BUILDING_KEY': 'BUILDING_KEY',
    'BUILDING_NUMBER': 'BUILDING_NUMBER',
    'BUILDING_NAME_LONG': 'BUILDING_NAME',
    'SITE': 'SITE',
    'CAMPUS_SECTOR': 'CAMPUS_SECTOR',
    'OWNERSHIP_TYPE': 'OWNERSHIP_TYPE',
    'ASSIGNABLE_AREA': 'ASSIGNABLE_AREA',
    'CITY': 'CITY',
    'STATE': 'STATE'
}
fac_building_base = fac_building_sel.rename(columns=rename_map)

# 2) Compute per-building floor counts from FAC_FLOOR
if 'BUILDING_KEY' in fac_floor.columns:
    floor_counts = (
        fac_floor
        .drop_duplicates(subset=['BUILDING_KEY', 'FLOOR'])
        .groupby('BUILDING_KEY', as_index=False)
        .agg(FLOOR_COUNT=('FLOOR', 'nunique'))
    )
else:
    key_col = 'FCLT_BUILDING_KEY' if 'FCLT_BUILDING_KEY' in fac_floor.columns else None
    floor_col = 'FLOOR' if 'FLOOR' in fac_floor.columns else None
    if key_col and floor_col:
        floor_counts = (
            fac_floor
            .drop_duplicates(subset=[key_col, floor_col])
            .groupby(key_col, as_index=False)
            .agg(FLOOR_COUNT=(floor_col, 'nunique'))
            .rename(columns={key_col: 'BUILDING_KEY'})
        )
    else:
        # If cannot determine, create empty to merge
        floor_counts = fac_building_base[['BUILDING_KEY']].copy()
        floor_counts['FLOOR_COUNT'] = pd.NA

# 3) Merge floor count into building base table
base_table = fac_building_base.merge(floor_counts, on='BUILDING_KEY', how='left')

# 4) Latest-period assignable area from FCLT_FLOOR_HIST (sum across floors)
req_cols = {'FCLT_BUILDING_KEY', 'FISCAL_PERIOD', 'FLOOR', 'ASSIGNABLE_AREA'}
if req_cols.issubset(set(fclt_floor_hist.columns)):
    latest_fp = (
        fclt_floor_hist.groupby('FCLT_BUILDING_KEY', as_index=False)['FISCAL_PERIOD']
        .max()
        .rename(columns={'FCLT_BUILDING_KEY': 'BUILDING_KEY', 'FISCAL_PERIOD': 'LATEST_FISCAL_PERIOD'})
    )

    ffh_latest = fclt_floor_hist.merge(
        latest_fp.rename(columns={'BUILDING_KEY': 'FCLT_BUILDING_KEY'}),
        on=['FCLT_BUILDING_KEY', 'FISCAL_PERIOD'],
        how='inner'
    ).rename(columns={'FCLT_BUILDING_KEY': 'BUILDING_KEY'})

    ffh_agg = (
        ffh_latest
        .drop_duplicates(subset=['BUILDING_KEY', 'FLOOR'])
        .groupby('BUILDING_KEY', as_index=False)
        .agg(
            ASSIGNABLE_AREA_LATEST_FROM_FLOORS=('ASSIGNABLE_AREA', 'sum'),
            FLOOR_COUNT_LATEST_PERIOD=('FLOOR', 'nunique')
        )
    )

    base_table = base_table.merge(ffh_agg, on='BUILDING_KEY', how='left')
    base_table = base_table.merge(latest_fp, on='BUILDING_KEY', how='left')
else:
    base_table['ASSIGNABLE_AREA_LATEST_FROM_FLOORS'] = pd.NA
    base_table['FLOOR_COUNT_LATEST_PERIOD'] = pd.NA
    base_table['LATEST_FISCAL_PERIOD'] = pd.NA

# 5) Organization counts per building - not available in given mapping; set NA
base_table['ORGANIZATION_COUNT'] = pd.NA

# 6) Prepare fields for final grouping output
# Choose assignable area to rank/sum:
# Prefer latest-from-floors if available; fallback to building-level ASSIGNABLE_AREA
area_col = 'ASSIGNABLE_AREA_LATEST_FROM_FLOORS' if 'ASSIGNABLE_AREA_LATEST_FROM_FLOORS' in base_table.columns else 'ASSIGNABLE_AREA'
base_table['ASSIGNABLE_AREA_EFFECTIVE'] = base_table[area_col]
base_table['ASSIGNABLE_AREA_EFFECTIVE'] = pd.to_numeric(base_table['ASSIGNABLE_AREA_EFFECTIVE'], errors='coerce')

# Floor count effective: prefer computed FLOOR_COUNT
base_table['FLOOR_COUNT_EFFECTIVE'] = pd.to_numeric(base_table['FLOOR_COUNT'], errors='coerce')

# 7) Build detail rows
detail_cols = [
    'CAMPUS_SECTOR',
    'BUILDING_NAME',
    'CITY',
    'STATE',
    'FLOOR_COUNT_EFFECTIVE',
    'ASSIGNABLE_AREA_EFFECTIVE',
    'ORGANIZATION_COUNT',
    'OWNERSHIP_TYPE'
]
for c in detail_cols:
    if c not in base_table.columns:
        base_table[c] = pd.NA

details = base_table[detail_cols].copy()

# Rank within sector by descending assignable area (ties: stable order)
details['RANK_IN_SECTOR'] = (
    details
    .groupby('CAMPUS_SECTOR')['ASSIGNABLE_AREA_EFFECTIVE']
    .rank(method='first', ascending=False)
    .astype('Int64')
)

# 8) Sector subtotals (only floors and area)
sector_sub = (
    details
    .groupby('CAMPUS_SECTOR', as_index=False)
    .agg(
        FLOOR_COUNT_EFFECTIVE=('FLOOR_COUNT_EFFECTIVE', 'sum'),
        ASSIGNABLE_AREA_EFFECTIVE=('ASSIGNABLE_AREA_EFFECTIVE', 'sum')
    )
)
sector_sub['BUILDING_NAME'] = 'Subtotal'
sector_sub['CITY'] = pd.NA
sector_sub['STATE'] = pd.NA
sector_sub['ORGANIZATION_COUNT'] = pd.NA
sector_sub['OWNERSHIP_TYPE'] = pd.NA
sector_sub['RANK_IN_SECTOR'] = pd.NA

# 9) Grand total
grand_total = pd.DataFrame({
    'CAMPUS_SECTOR': ['Grand Total'],
    'BUILDING_NAME': ['Grand Total'],
    'CITY': [pd.NA],
    'STATE': [pd.NA],
    'FLOOR_COUNT_EFFECTIVE': [details['FLOOR_COUNT_EFFECTIVE'].sum()],
    'ASSIGNABLE_AREA_EFFECTIVE': [details['ASSIGNABLE_AREA_EFFECTIVE'].sum()],
    'ORGANIZATION_COUNT': [pd.NA],
    'OWNERSHIP_TYPE': [pd.NA],
    'RANK_IN_SECTOR': [pd.NA]
})

# 10) Combine detail rows with sector subtotals and grand total
# We want details ordered within each sector by rank, followed by subtotal, then overall grand total at end
# Sort details by sector and rank
ordered_details = details.sort_values(by=['CAMPUS_SECTOR', 'RANK_IN_SECTOR'], kind='stable')

# Interleave sector subtotals after each sector
# Merge to get an order key per sector
sectors_order = ordered_details[['CAMPUS_SECTOR']].drop_duplicates().reset_index(drop=True)
sectors_order['__order__'] = range(len(sectors_order))

ordered_details = ordered_details.merge(sectors_order, on='CAMPUS_SECTOR', how='left')
sector_sub = sector_sub.merge(sectors_order, on='CAMPUS_SECTOR', how='left')

# Concatenate details and sector subtotal, then sort to put subtotal after details in each sector
combined = pd.concat([ordered_details.assign(__is_subtotal__=False), sector_sub.assign(__is_subtotal__=True)], ignore_index=True)

# Sort by sector order, then by subtotal flag (False before True), then by rank
combined = combined.sort_values(by=['__order__', '__is_subtotal__', 'RANK_IN_SECTOR'], kind='stable')

# Append grand total at the end
final_df = pd.concat([combined.drop(columns=['__order__', '__is_subtotal__']), grand_total], ignore_index=True)

# 11) Rename columns to match requested wording
final_df = final_df.rename(columns={
    'CAMPUS_SECTOR': 'Campus Sector',
    'BUILDING_NAME': 'Building Name',
    'CITY': 'City',
    'STATE': 'State',
    'FLOOR_COUNT_EFFECTIVE': 'Total Number of Floors',
    'ASSIGNABLE_AREA_EFFECTIVE': 'Total Assignable Area',
    'ORGANIZATION_COUNT': 'Total Number of Organizations',
    'OWNERSHIP_TYPE': 'Ownership Type',
    'RANK_IN_SECTOR': 'Rank in Sector'
})

# Ensure column order
final_cols = [
    'Campus Sector',
    'Building Name',
    'City',
    'State',
    'Total Number of Floors',
    'Total Assignable Area',
    'Total Number of Organizations',
    'Ownership Type',
    'Rank in Sector'
]
final_df = final_df[final_cols]

# Assign final answer to `result`
result = {"buildings_by_sector_with_totals": final_df}