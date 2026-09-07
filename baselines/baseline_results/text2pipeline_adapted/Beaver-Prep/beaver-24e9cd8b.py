import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'BUILDING_NAME', 'new_name': 'building_name'}, {'old_name': 'BUILDING_NAME_LONG', 'new_name': 'building_name_long'}, {'old_name': 'CAMPUS_SECTOR', 'new_name': 'campus_sector'}, {'old_name': 'ASSIGNABLE_AREA', 'new_name': 'assignable_area'}, {'old_name': 'NUM_OF_ROOMS', 'new_name': 'num_rooms'}, {'old_name': 'OWNERSHIP_TYPE', 'new_name': 'ownership_type'}, {'old_name': 'BUILDING_NUMBER', 'new_name': 'building_number'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'assignable_area', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'num_rooms', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_HEIGHT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'campus_sector', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ownership_type', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'building_name', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'building_name_long', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SITE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SITE', 'new_name': 'site'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['building_number', 'building_name', 'building_name_long', 'site', 'campus_sector', 'EXT_GROSS_AREA', 'assignable_area', 'num_rooms', 'ownership_type']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'BUILDING_NAME': 'building_name', 'BUILDING_NAME_LONG': 'building_name_long', 'CAMPUS_SECTOR': 'campus_sector', 'ASSIGNABLE_AREA': 'assignable_area', 'NUM_OF_ROOMS': 'num_rooms', 'OWNERSHIP_TYPE': 'ownership_type', 'BUILDING_NUMBER': 'building_number'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['assignable_area'] = pd.to_numeric(tmp_1['assignable_area'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['EXT_GROSS_AREA'] = pd.to_numeric(tmp_2['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['num_rooms'] = pd.to_numeric(tmp_3['num_rooms'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['BUILDING_HEIGHT'] = pd.to_numeric(tmp_4['BUILDING_HEIGHT'], errors='coerce').astype(float)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['campus_sector'] = tmp_5['campus_sector'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_6['ownership_type'] = tmp_6['ownership_type'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_7['building_name'] = tmp_7['building_name'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_8['building_name_long'] = tmp_8['building_name_long'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_9['SITE'] = tmp_9['SITE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 11: Rename
    tmp_10 = tmp_9.rename(columns={'SITE': 'site'})
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['building_number', 'building_name', 'building_name_long', 'site', 'campus_sector', 'EXT_GROSS_AREA', 'assignable_area', 'num_rooms', 'ownership_type']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()

# Prefer short name; fallback to long name
name_series = df['building_name'].where(df['building_name'].notna() & (df['building_name'].astype(str).str.strip() != ''), df['building_name_long'])

# Derive city/state from site when possible (broadened, case-insensitive contains match for 'mit')
site_str = df['site'].astype(str).str.strip()
site_lower = site_str.str.lower()
city = site_lower.apply(lambda x: 'Cambridge' if 'mit' in x else None)
state = site_lower.apply(lambda x: 'MA' if 'mit' in x else None)

# Build detail rows
result = df.assign(
    building_name=name_series,
    city=city,
    state=state,
    total_floors=None,  # not available in source
    total_assignable_area=df['assignable_area'],
    total_rooms=df['num_rooms'],
    total_organizations=None  # not available in source
)[[
    'campus_sector', 'building_name', 'city', 'state', 'total_floors', 'total_assignable_area', 'total_rooms', 'total_organizations', 'ownership_type'
]]

# Rank within sector by descending assignable area (1-indexed)
result['rank_in_sector'] = result.groupby('campus_sector')['total_assignable_area'].rank(ascending=False, method='first').astype(int)

# Subtotals per sector (only floors and assignable area required). Floors unavailable -> NaN subtotal for floors.
sector_subtotals = result.groupby('campus_sector', as_index=False).agg({
    'total_floors': 'sum',
    'total_assignable_area': 'sum'
})
sector_subtotals['building_name'] = 'Subtotal'
sector_subtotals['city'] = None
sector_subtotals['state'] = None
sector_subtotals['total_rooms'] = None
sector_subtotals['total_organizations'] = None
sector_subtotals['ownership_type'] = None
sector_subtotals['rank_in_sector'] = None
sector_subtotals = sector_subtotals[[
    'campus_sector','building_name','city','state','total_floors','total_assignable_area','total_rooms','total_organizations','ownership_type','rank_in_sector'
]]

# Grand total across all sectors (only floors and assignable area required)
grand_totals_vals = sector_subtotals.agg({'total_floors': 'sum', 'total_assignable_area': 'sum'})
grand_df = pd.DataFrame([
    {
        'campus_sector': 'Grand Total',
        'building_name': 'Grand Total',
        'city': None,
        'state': None,
        'total_floors': grand_totals_vals['total_floors'],
        'total_assignable_area': grand_totals_vals['total_assignable_area'],
        'total_rooms': None,
        'total_organizations': None,
        'ownership_type': None,
        'rank_in_sector': None
    }
])[[
    'campus_sector','building_name','city','state','total_floors','total_assignable_area','total_rooms','total_organizations','ownership_type','rank_in_sector'
]]

# Interleave sector details and subtotals, ordered by campus_sector
sectors = result['campus_sector'].dropna().astype(str).unique().tolist()
sectors.sort()
parts = []
for s in sectors:
    sect_rows = result[result['campus_sector'] == s].sort_values(['total_assignable_area'], ascending=[False])
    parts.append(sect_rows)
    parts.append(sector_subtotals[sector_subtotals['campus_sector'] == s])

final_with_totals = pd.concat(parts, ignore_index=True) if parts else result.head(0)

# Append grand total
target = pd.concat([final_with_totals, grand_df], ignore_index=True)[[
    'campus_sector', 'building_name', 'city', 'state', 'total_floors', 'total_assignable_area', 'total_rooms', 'total_organizations', 'ownership_type', 'rank_in_sector'
]]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
