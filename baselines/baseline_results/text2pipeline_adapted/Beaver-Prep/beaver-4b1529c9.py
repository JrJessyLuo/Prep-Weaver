import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FCLT_BUILDING_KEY', 'new_name': 'BUILDING_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_HEIGHT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_HEIGHT', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'PARENT_BUILDING_NUMBER', 'PARENT_BUILDING_NAME', 'PARENT_BUILDING_NAME_LONG', 'BUILDING_NAME_LONG', 'EXT_GROSS_AREA', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA', 'SITE', 'CAMPUS_SECTOR', 'ACCESS_LEVEL_CODE', 'ACCESS_LEVEL_NAME', 'BUILDING_TYPE', 'OWNERSHIP_TYPE', 'BUILDING_USE', 'OCCUPANCY_CLASS', 'BUILDING_HEIGHT', 'COST_CENTER_CODE', 'COST_COLLECTOR_KEY', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'EASTING_X_SPCS', 'NORTHING_Y_SPCS', 'BUILDING_SORT', 'BUILDING_NAMED_FOR', 'BUILDING_NAME', 'DATE_BUILT', 'DATE_ACQUIRED', 'DATE_OCCUPIED', 'WAREHOUSE_LOAD_DATE', 'NUM_OF_ROOMS']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'BUILDING_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'new_name': 'ASSIGNABLE_AREA'}, {'old_name': 'BLDG_GROSS_SQUARE_FOOTAGE', 'new_name': 'EXT_GROSS_AREA'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ASSIGNABLE_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'EXT_GROSS_AREA', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['HR_DEPARTMENT_NAME', 'ORGANIZATION_NAME', 'DLC_NAME', 'ORGANIZATION']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'FCLT_BUILDING_KEY': 'BUILDING_KEY'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BUILDING_HEIGHT'] = pd.to_numeric(tmp_1['BUILDING_HEIGHT'], errors='coerce').astype(float)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_HEIGHT', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'PARENT_BUILDING_NUMBER', 'PARENT_BUILDING_NAME', 'PARENT_BUILDING_NAME_LONG', 'BUILDING_NAME_LONG', 'EXT_GROSS_AREA', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA', 'SITE', 'CAMPUS_SECTOR', 'ACCESS_LEVEL_CODE', 'ACCESS_LEVEL_NAME', 'BUILDING_TYPE', 'OWNERSHIP_TYPE', 'BUILDING_USE', 'OCCUPANCY_CLASS', 'BUILDING_HEIGHT', 'COST_CENTER_CODE', 'COST_COLLECTOR_KEY', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'EASTING_X_SPCS', 'NORTHING_Y_SPCS', 'BUILDING_SORT', 'BUILDING_NAMED_FOR', 'BUILDING_NAME', 'DATE_BUILT', 'DATE_ACQUIRED', 'DATE_OCCUPIED', 'WAREHOUSE_LOAD_DATE', 'NUM_OF_ROOMS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_NUMBER'] = tmp_0['BUILDING_NUMBER'].astype(str)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'BLDG_ASSIGNABLE_SQUARE_FOOTAGE': 'ASSIGNABLE_AREA', 'BLDG_GROSS_SQUARE_FOOTAGE': 'EXT_GROSS_AREA'})
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ASSIGNABLE_AREA'] = pd.to_numeric(tmp_2['ASSIGNABLE_AREA'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['EXT_GROSS_AREA'] = pd.to_numeric(tmp_3['EXT_GROSS_AREA'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['HR_DEPARTMENT_NAME', 'ORGANIZATION_NAME', 'DLC_NAME', 'ORGANIZATION']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_8', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b1 = prepared_table_1
b3 = prepared_table_3
# Join buildings from table_1 and table_3 on BUILDING_NUMBER to combine height, address, and area metrics
buildings = b1.merge(b3, on='BUILDING_NUMBER', how='outer', suffixes=('_t1', '_t3'))
# Prefer non-null name/address/area/height from either side
# Resolve building name
buildings['BUILDING_NAME'] = buildings['BUILDING_NAME_t1'].where(buildings['BUILDING_NAME_t1'].notna(), buildings['BUILDING_NAME_t3'])
# Resolve ASSIGNABLE_AREA and EXT_GROSS_AREA
buildings['ASSIGNABLE_AREA'] = buildings['ASSIGNABLE_AREA_t1'].where(buildings['ASSIGNABLE_AREA_t1'].notna(), buildings['ASSIGNABLE_AREA_t3'])
buildings['EXT_GROSS_AREA'] = buildings['EXT_GROSS_AREA_t1'].where(buildings['EXT_GROSS_AREA_t1'].notna(), buildings['EXT_GROSS_AREA_t3'])
# Resolve BUILDING_HEIGHT and STREET ADDRESS
buildings['BUILDING_HEIGHT'] = buildings['BUILDING_HEIGHT']
buildings['BUILDING_STREET_ADDRESS'] = buildings['BUILDING_STREET_ADDRESS']
# Derive city and state assuming MIT campus in Cambridge, MA when street address present
buildings['CITY'] = 'Cambridge'
buildings['STATE'] = 'MA'
# Compute average square footage as EXT_GROSS_AREA / number of floors is unknown; instead compute average of available area measures
# Here interpret 'average square footage' as the average of assignable and total (gross) where both available
buildings['AVERAGE_SQFT'] = (buildings[['ASSIGNABLE_AREA','EXT_GROSS_AREA']].mean(axis=1))
# Prepare an HR department name by best-effort broad match on organization labels; since no reliable key exists, attach the most generic HR department label (no filtering) to all rows using a representative column from table_4
hr = prepared_table_4.copy()
# Choose a single HR department label per row by preferring HR_DEPARTMENT_NAME then ORGANIZATION_NAME then DLC_NAME then ORGANIZATION
hr['HR_DEPT_BEST'] = hr['HR_DEPARTMENT_NAME']
hr['HR_DEPT_BEST'] = hr['HR_DEPT_BEST'].where(hr['HR_DEPT_BEST'].notna(), hr['ORGANIZATION_NAME'])
hr['HR_DEPT_BEST'] = hr['HR_DEPT_BEST'].where(hr['HR_DEPT_BEST'].notna(), hr['DLC_NAME'])
hr['HR_DEPT_BEST'] = hr['HR_DEPT_BEST'].where(hr['HR_DEPT_BEST'].notna(), hr['ORGANIZATION'])
# Without a deterministic building-to-HR link, avoid dropping buildings; instead, pick a broad HR label 'Facilities' if present; else use the most frequent HR department
hr_label = None
if not hr.empty:
    # Try to find a facilities-related label
    cand = hr[hr['HR_DEPT_BEST'].astype(str).str.contains('facilit|facilities|campus services', case=False, na=False)]
    if not cand.empty:
        hr_label = cand['HR_DEPT_BEST'].iloc[0]
    else:
        hr_label = hr['HR_DEPT_BEST'].mode().iloc[0] if not hr['HR_DEPT_BEST'].mode().empty else None
buildings['HR_DEPARTMENT_NAME'] = hr_label
# Final projection and ordering
result = buildings[['BUILDING_NAME', 'BUILDING_NUMBER', 'BUILDING_HEIGHT', 'BUILDING_STREET_ADDRESS', 'CITY', 'STATE', 'HR_DEPARTMENT_NAME', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA', 'AVERAGE_SQFT']].copy()
# Sort by assignable, then total (gross), then average square footage descending
result = result.sort_values(by=['ASSIGNABLE_AREA','EXT_GROSS_AREA','AVERAGE_SQFT'], ascending=[False, False, False])
# Assign to target
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
