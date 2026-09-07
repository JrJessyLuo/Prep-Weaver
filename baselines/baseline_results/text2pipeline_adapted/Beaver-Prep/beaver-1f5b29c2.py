import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FCLT_BUILDING_KEY', 'new_name': 'building_key'}, {'old_name': 'FLOOR', 'new_name': 'floor'}, {'old_name': 'ROOM', 'new_name': 'room_number'}, {'old_name': 'ORGANIZATION_NAME', 'new_name': 'organization_name'}, {'old_name': 'AREA', 'new_name': 'area'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'building_key', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'floor', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'room_number', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'organization_name', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'area', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['building_key', 'floor', 'room_number', 'organization_name', 'area']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FCLT_BUILDING_KEY', 'new_name': 'building_key'}, {'old_name': 'BUILDING_NAME', 'new_name': 'building_name'}, {'old_name': 'OWNERSHIP_TYPE', 'new_name': 'ownership_type'}, {'old_name': 'NUM_OF_ROOMS', 'new_name': 'num_of_rooms'}, {'old_name': 'ASSIGNABLE_AREA', 'new_name': 'building_assignable_area'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'building_assignable_area', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'num_of_rooms', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'building_key', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'building_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ownership_type', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['building_key', 'building_name', 'ownership_type', 'num_of_rooms', 'building_assignable_area']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'FCLT_BUILDING_KEY': 'building_key', 'FLOOR': 'floor', 'ROOM': 'room_number', 'ORGANIZATION_NAME': 'organization_name', 'AREA': 'area'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['building_key'] = tmp_1['building_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['floor'] = tmp_2['floor'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['room_number'] = tmp_3['room_number'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['organization_name'] = tmp_4['organization_name'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['area'] = pd.to_numeric(tmp_5['area'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['building_key', 'floor', 'room_number', 'organization_name', 'area']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'FCLT_BUILDING_KEY': 'building_key', 'BUILDING_NAME': 'building_name', 'OWNERSHIP_TYPE': 'ownership_type', 'NUM_OF_ROOMS': 'num_of_rooms', 'ASSIGNABLE_AREA': 'building_assignable_area'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['building_assignable_area'] = pd.to_numeric(tmp_1['building_assignable_area'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['num_of_rooms'] = pd.to_numeric(tmp_2['num_of_rooms'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['building_key'] = tmp_3['building_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['building_name'] = tmp_4['building_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['ownership_type'] = tmp_5['ownership_type'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['building_key', 'building_name', 'ownership_type', 'num_of_rooms', 'building_assignable_area']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='building_key')
# Compute building-level area from rooms (sum of room areas per building) for room-level percentages.
bldg_area_from_rooms = integrated.groupby('building_key', as_index=False)['area'].sum().rename(columns={'area':'building_area_sum_rooms'})
integrated = integrated.merge(bldg_area_from_rooms, how='left', on='building_key')
# Total area across all buildings (using room areas)
all_buildings_total_area = bldg_area_from_rooms['building_area_sum_rooms'].sum()
# Helper to format integers with commas
def fmt_int(x):
    try:
        return f"{int(round(x)):,}"
    except Exception:
        return None
# Base room-level rows with percentages relative to building (using sum of room areas per building)
integrated['percentage_of_building_area'] = (integrated['area'] / integrated['building_area_sum_rooms']) * 100
# Prepare room-level display columns
room_rows = integrated.copy()
room_rows['number_of_rooms'] = 1
room_rows['area_fmt'] = room_rows['area'].round().astype('Int64').astype(str).apply(lambda s: f"{int(s):,}" if s not in ['<NA>','nan','None'] else None)
room_rows['number_of_rooms_fmt'] = room_rows['number_of_rooms'].astype('Int64').astype(str).apply(lambda s: f"{int(s):,}" if s not in ['<NA>','nan','None'] else None)
room_rows['percentage_fmt'] = room_rows['percentage_of_building_area'].round(2)
room_rows_out = room_rows[['building_name','floor','room_number','ownership_type','organization_name','number_of_rooms_fmt','area_fmt','percentage_fmt','building_key']].rename(columns={'number_of_rooms_fmt':'number_of_rooms','area_fmt':'area','percentage_fmt':'percentage_of_area'})
# Floor subtotals (per building_key + floor). Percentage relative to that building's total area; for building/grand totals special rule will be applied later.
floor_grp = integrated.groupby(['building_key','building_name','ownership_type','floor'], as_index=False).agg(number_of_rooms=('room_number','count'), area=('area','sum'), building_area_sum_rooms=('building_area_sum_rooms','first'))
floor_grp['percentage_of_building_area'] = (floor_grp['area'] / floor_grp['building_area_sum_rooms']) * 100
floor_grp['room_number'] = 'Subtotal floor'
floor_grp['organization_name'] = '—'
floor_grp['number_of_rooms'] = floor_grp['number_of_rooms'].round().astype('Int64').astype(str).apply(lambda s: f"{int(s):,}" if s not in ['<NA>','nan','None'] else None)
floor_grp['area'] = floor_grp['area'].round().astype('Int64').astype(str).apply(lambda s: f"{int(s):,}" if s not in ['<NA>','nan','None'] else None)
floor_grp['percentage_of_area'] = floor_grp['percentage_of_building_area'].round(2)
floor_rows_out = floor_grp[['building_name','floor','room_number','ownership_type','organization_name','number_of_rooms','area','percentage_of_area','building_key']]
# Building subtotals (across all floors). Percentage relative to area of all buildings per instructions.
building_tot = integrated.groupby(['building_key','building_name','ownership_type'], as_index=False).agg(number_of_rooms=('room_number','count'), area=('area','sum'))
building_tot['percentage_of_all_buildings'] = (building_tot['area'] / all_buildings_total_area) * 100
building_tot['floor'] = 'All floors'
building_tot['room_number'] = 'Subtotal building'
building_tot['organization_name'] = '—'
building_tot['number_of_rooms'] = building_tot['number_of_rooms'].round().astype('Int64').astype(str).apply(lambda s: f"{int(s):,}" if s not in ['<NA>','nan','None'] else None)
building_tot['area'] = building_tot['area'].round().astype('Int64').astype(str).apply(lambda s: f"{int(s):,}" if s not in ['<NA>','nan','None'] else None)
building_tot['percentage_of_area'] = building_tot['percentage_of_all_buildings'].round(2)
building_rows_out = building_tot[['building_name','floor','room_number','ownership_type','organization_name','number_of_rooms','area','percentage_of_area','building_key']]
# Grand total across all buildings. Percentage relative to area of all buildings = 100%.
grand_area = integrated['area'].sum()
grand_rooms = integrated['room_number'].count()
grand = {
    'building_name': 'All buildings',
    'floor': 'All floors',
    'room_number': 'Grand total',
    'ownership_type': '—',
    'organization_name': '—',
    'number_of_rooms': f"{int(round(grand_rooms)):,}",
    'area': f"{int(round(grand_area)):,}",
    'percentage_of_area': round(100.0, 2),
    'building_key': None
}
grand_rows_out = __import__('pandas').DataFrame([grand])
# For room-level rows, percentage already relative to building. Format percentage column as numeric with 2 decimals (leave numeric for consistency with spec) and ensure number/area already formatted strings.
room_rows_out = room_rows_out.rename(columns={'percentage_of_area':'percentage_tmp'})
room_rows_out['percentage_of_area'] = room_rows_out['percentage_tmp'].round(2)
room_rows_out = room_rows_out.drop(columns=['percentage_tmp'])
# Combine: order rooms, then floor subtotals, then building subtotals for each building, and end with grand total. Use a simple concatenation and sort by building_name and a level indicator.
room_rows_out['level'] = 1
floor_rows_out['level'] = 2
building_rows_out['level'] = 3
grand_rows_out['level'] = 4
combined = __import__('pandas').concat([room_rows_out, floor_rows_out, building_rows_out, grand_rows_out], ignore_index=True, sort=False)
# Sort by building_name (grand last by level), then floor label (rooms keep original order not guaranteed; we sort by floor, then room_number where applicable)
combined['building_name_sort'] = combined['building_name'].fillna('~')
combined['floor_sort'] = combined['floor'].astype(str)
combined['room_sort'] = combined['room_number'].astype(str)
combined = combined.sort_values(by=['level','building_name_sort','floor_sort','room_sort']).drop(columns=['level','building_name_sort','floor_sort','room_sort','building_key'])
# Final projection and assign to target
target = combined[['building_name','floor','room_number','ownership_type','organization_name','number_of_rooms','area','percentage_of_area']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
