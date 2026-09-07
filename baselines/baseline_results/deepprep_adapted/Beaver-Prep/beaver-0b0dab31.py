import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="ORGANIZATION_NAME", mode="mode")
    # MissingValueImputation
    table_1["ORGANIZATION_NAME"] = table_1["ORGANIZATION_NAME"].fillna(table_1["ORGANIZATION_NAME"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="AREA", mode="median")
    # MissingValueImputation
    table_1["AREA"] = table_1["AREA"].fillna(table_1["AREA"].median())

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['AREA']
    if _dtype == "datetime64":
        table_1['AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['AREA'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR']
    if _dtype == "datetime64":
        table_1['FLOOR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY', 'AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'FCLT_FLOOR_KEY', 'FLOOR', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME', 'FCLT_ROOM_KEY', 'AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_FLOOR_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FCLT_FLOOR_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FCLT_FLOOR_KEY']
    if _dtype == "datetime64":
        table_1['FCLT_FLOOR_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FCLT_FLOOR_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FCLT_FLOOR_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FCLT_FLOOR_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'FLOOR_SORT_SEQUENCE'])
    # SelectCol
    _cols = [c for c in ['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR', 'FLOOR_SORT_SEQUENCE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_BUILDING_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FCLT_BUILDING_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FCLT_BUILDING_KEY']
    if _dtype == "datetime64":
        table_1['FCLT_BUILDING_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FCLT_BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FCLT_BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FCLT_BUILDING_KEY'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR']
    if _dtype == "datetime64":
        table_1['FLOOR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR_SORT_SEQUENCE", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR_SORT_SEQUENCE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR_SORT_SEQUENCE']
    if _dtype == "datetime64":
        table_1['FLOOR_SORT_SEQUENCE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR_SORT_SEQUENCE'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR_SORT_SEQUENCE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_FLOOR_KEY', 'FCLT_BUILDING_KEY', 'FLOOR_SORT_SEQUENCE'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_FLOOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_FLOOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['FCLT_BUILDING_KEY', 'FLOOR_SORT_SEQUENCE', 'FLOOR'], ascending=[True, True, True])
    # Sort
    table_1 = table_1.sort_values(by=['FCLT_BUILDING_KEY', 'FLOOR_SORT_SEQUENCE', 'FLOOR'], ascending=[True, True, True])

    # ---------------- Step 9 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_floors = prepared_table_3

# Assume the three prepared tables are available as DataFrames: prepared_rooms, prepared_buildings, prepared_floors
# 1) Identify the Stata building key from buildings (commonly E62 is Stata Center). Match by name contains 'STATA'.
bld = prepared_buildings.copy()
stata_mask = bld['BUILDING_NAME'].fillna('').str.contains('STATA', case=False) | bld['BUILDING_NAME_LONG'].fillna('').str.contains('STATA', case=False)
stata_buildings = bld.loc[stata_mask, ['FCLT_BUILDING_KEY']].dropna().drop_duplicates()

# If multiple matches, use all; if none, result will be empty
rooms = prepared_rooms.merge(stata_buildings, on='FCLT_BUILDING_KEY', how='inner')

# Join floors to ensure consistent floor metadata if needed
rooms = rooms.merge(prepared_floors[['FCLT_FLOOR_KEY','FLOOR','FLOOR_SORT_SEQUENCE']], on='FCLT_FLOOR_KEY', how='left', suffixes=('', '_f'))
# Prefer FLOOR from rooms if present; otherwise fallback to floors table
rooms['FLOOR_FINAL'] = rooms['FLOOR'].where(rooms['FLOOR'].notna(), rooms['FLOOR_f'])

# Exclude departments without any rooms implicitly handled by grouping over existing rows
# Compute per-floor, per-department aggregations
rooms['AREA_NUM'] = pd.to_numeric(rooms['AREA'], errors='coerce')
agg = rooms.groupby(['FCLT_FLOOR_KEY','FLOOR_FINAL','FCLT_ORGANIZATION_KEY','ORGANIZATION_NAME'], dropna=False).agg(
    num_rooms=('FCLT_ROOM_KEY','nunique'),
    total_area=('AREA_NUM','sum')
).reset_index()
# Exclude dept groups with zero rooms (nunique gives 0 only if no rows; not possible), and drop NaN org names
agg = agg[agg['num_rooms'] > 0]

# Compute averages
agg['avg_area'] = agg['total_area'] / agg['num_rooms']

# Floor subtotals
floor_sub = agg.groupby(['FCLT_FLOOR_KEY','FLOOR_FINAL'], dropna=False).agg(
    num_rooms=('num_rooms','sum'),
    total_area=('total_area','sum')
).reset_index()
floor_sub['avg_area'] = floor_sub['total_area'] / floor_sub['num_rooms']

# Grand total
grand = pd.DataFrame({
    'num_rooms': [floor_sub['num_rooms'].sum()],
    'total_area': [floor_sub['total_area'].sum()],
    'avg_area': [floor_sub['total_area'].sum() / floor_sub['num_rooms'].sum() if floor_sub['num_rooms'].sum() else pd.NA]
})

# Sorting by floor key and department name ascending
# Ensure department name for sorting; fillna with empty for stable sort but we won't show for totals
agg_sorted = agg.sort_values(by=['FCLT_FLOOR_KEY','ORGANIZATION_NAME'], kind='mergesort').reset_index(drop=True)

# Build display rows
def fmt_int(n):
    if pd.isna(n):
        return ''
    try:
        return f"{int(round(n)):,}"
    except Exception:
        return ''

detail_rows = []
current_floor = None
for _, r in agg_sorted.iterrows():
    floor_key = r['FCLT_FLOOR_KEY']
    floor_label = r['FLOOR_FINAL']
    # Only show floor key on first row of each floor group
    show_floor = '' if floor_key == current_floor else floor_key
    current_floor = floor_key
    detail_rows.append({
        'Floor Key': show_floor,
        'Department Name': r['ORGANIZATION_NAME'] if pd.notna(r['ORGANIZATION_NAME']) else '',
        'Number of Rooms': fmt_int(r['num_rooms']),
        'Total Area': fmt_int(r['total_area']),
        'Average Area': fmt_int(r['avg_area'])
    })
    
    # If next row is different floor or this is last row for the floor, we'll add subtotal later

# Add subtotals per floor in the correct positions (after each floor's block)
# We'll iterate floors in sorted order and append subtotal after last detail row for that floor
result_rows = []
seen_floor = None
# Map floor to its subtotal
floor_sub_map = floor_sub.set_index('FCLT_FLOOR_KEY').to_dict(orient='index')
# For ordering floors, use the order observed in agg_sorted
floors_in_order = []
for fk in agg_sorted['FCLT_FLOOR_KEY']:
    if fk not in floors_in_order:
        floors_in_order.append(fk)

for fk in floors_in_order:
    # append all detail rows for this floor in the order they were created
    for row in [d for d in detail_rows if (d['Floor Key'] == fk) or (d['Floor Key'] == '' and seen_floor == fk)]:
        # track current floor to help capture continuation rows
        if row['Floor Key'] != '':
            seen_floor = fk
        result_rows.append(row)
    # Add subtotal row
    sub = floor_sub_map.get(fk, None)
    if sub is not None:
        result_rows.append({
            'Floor Key': '',
            'Department Name': '',
            'Number of Rooms': fmt_int(sub['num_rooms']),
            'Total Area': fmt_int(sub['total_area']),
            'Average Area': fmt_int(sub['avg_area'])
        })

# Grand total row (no floor key or department)
result_rows.append({
    'Floor Key': '',
    'Department Name': '',
    'Number of Rooms': fmt_int(grand.loc[0,'num_rooms']),
    'Total Area': fmt_int(grand.loc[0,'total_area']),
    'Average Area': fmt_int(grand.loc[0,'avg_area'])
})

# Convert to DataFrame and ensure final sort order is by floor key (already grouped) and department name ascending within floor
answer_df = pd.DataFrame(result_rows)
# Reorder columns exactly as requested
answer_df = answer_df[['Floor Key','Department Name','Number of Rooms','Total Area','Average Area']]

target = answer_df

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
