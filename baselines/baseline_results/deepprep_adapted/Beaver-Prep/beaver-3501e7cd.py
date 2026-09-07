import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row.get('SITE', '')).strip().upper() == 'MIT'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row.get('SITE', '')).strip().upper() == 'MIT'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="EXT_GROSS_AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['EXT_GROSS_AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['EXT_GROSS_AREA']
    if _dtype == "datetime64":
        table_1['EXT_GROSS_AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['EXT_GROSS_AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['EXT_GROSS_AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['EXT_GROSS_AREA'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_OF_ROOMS", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_OF_ROOMS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_OF_ROOMS']
    if _dtype == "datetime64":
        table_1['NUM_OF_ROOMS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_OF_ROOMS'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'OWNERSHIP_TYPE', 'BUILDING_USE', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'OWNERSHIP_TYPE', 'BUILDING_USE', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS'] if c in table_1.columns]
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_ORGANIZATION_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FCLT_ORGANIZATION_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FCLT_ORGANIZATION_KEY']
    if _dtype == "datetime64":
        table_1['FCLT_ORGANIZATION_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FCLT_ORGANIZATION_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FCLT_ORGANIZATION_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FCLT_ORGANIZATION_KEY'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # normalize whitespace and trim
    #     return " ".join(str(s).strip().split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # normalize whitespace and trim
        return " ".join(str(s).strip().split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ORGANIZATION_NAME"] = table_1["ORGANIZATION_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_rooms = prepared_table_2

# prepared_buildings and prepared_rooms are the synthesized per-table results
b = prepared_buildings.copy()
r = prepared_rooms.copy()

# Ensure correct types
# NUM_OF_ROOMS may already be an integer; EXT_GROSS_AREA numeric
b['EXT_GROSS_AREA'] = pd.to_numeric(b['EXT_GROSS_AREA'], errors='coerce')

# Count distinct organizations per building
org_per_bldg = (
    r.dropna(subset=['FCLT_BUILDING_KEY'])
     .drop_duplicates(subset=['FCLT_BUILDING_KEY','FCLT_ORGANIZATION_KEY'])
     .groupby('FCLT_BUILDING_KEY', as_index=False)
     .agg(ASSOCIATED_ORG_COUNT=('FCLT_ORGANIZATION_KEY','nunique'))
)

# Join to buildings
bt = b.merge(org_per_bldg, on='FCLT_BUILDING_KEY', how='left')
bt['ASSOCIATED_ORG_COUNT'] = bt['ASSOCIATED_ORG_COUNT'].fillna(0).astype(int)

# Map ownership into Owned vs Leased groups; preserve detailed ownership in column for display logic
bt['OWNERSHIP_GROUP'] = bt['OWNERSHIP_TYPE'].fillna('UNKNOWN').str.upper().map(lambda x: 'OWNED' if 'OWN' in x else ('LEASED' if 'LEASE' in x else x))

# Aggregate by Ownership Group and Usage Type
by_group_use = (
    bt.groupby(['OWNERSHIP_GROUP','BUILDING_USE'], dropna=False)
      .agg(
          BUILDING_COUNT=('FCLT_BUILDING_KEY','nunique'),
          GROSS_SQFT=('EXT_GROSS_AREA','sum'),
          ROOMS=('NUM_OF_ROOMS','sum'),
          ORG_COUNT=('ASSOCIATED_ORG_COUNT','sum')
      )
      .reset_index()
)

# Subtotals per Ownership Group
subtotals = (
    by_group_use.groupby('OWNERSHIP_GROUP', as_index=False)
      .agg(
          BUILDING_COUNT=('BUILDING_COUNT','sum'),
          GROSS_SQFT=('GROSS_SQFT','sum'),
          ROOMS=('ROOMS','sum'),
          ORG_COUNT=('ORG_COUNT','sum')
      )
)
subtotals['SUBTOTAL_ROW'] = True
subtotals['BUILDING_USE'] = ''

by_group_use['SUBTOTAL_ROW'] = False

# Concatenate detail and subtotals, then sort by ownership group then usage
out = pd.concat([by_group_use, subtotals], ignore_index=True)
out['OWNERSHIP_TYPE_DISPLAY'] = out['OWNERSHIP_GROUP']

# Insert grand total row (no ownership or usage shown)
grand = pd.DataFrame({
    'OWNERSHIP_GROUP':[''],
    'BUILDING_USE':[''],
    'BUILDING_COUNT':[out.loc[out['SUBTOTAL_ROW']==False,'BUILDING_COUNT'].sum()],
    'GROSS_SQFT':[out.loc[out['SUBTOTAL_ROW']==False,'GROSS_SQFT'].sum()],
    'ROOMS':[out.loc[out['SUBTOTAL_ROW']==False,'ROOMS'].sum()],
    'ORG_COUNT':[out.loc[out['SUBTOTAL_ROW']==False,'ORG_COUNT'].sum()],
    'SUBTOTAL_ROW':[True],
    'OWNERSHIP_TYPE_DISPLAY':['']
})

# Sort: OWNED first, then LEASED, then others; within group, alphabetical BUILDING_USE with subtotal at end
order_map = {'OWNED':0,'LEASED':1}
out['group_order'] = out['OWNERSHIP_GROUP'].map(order_map).fillna(99)
# place subtotal rows at end of each group
out['row_order_in_group'] = out['SUBTOTAL_ROW'].map({False:0, True:1})

out = out.sort_values(by=['group_order','row_order_in_group','BUILDING_USE'], kind='mergesort')

# Display ownership type only when it differs from previous displayed row
out = out.reset_index(drop=True)
display_owner = []
prev = None
for _, row in out.iterrows():
    if row['SUBTOTAL_ROW']:
        display_owner.append('')
    else:
        curr = row['OWNERSHIP_GROUP']
        if curr != prev:
            display_owner.append(curr)
            prev = curr
        else:
            display_owner.append('')
out['OWNERSHIP_TYPE_DISPLAY'] = display_owner

# Rounding and formatting
for col in ['GROSS_SQFT']:
    out[col] = out[col].round(0).astype('Int64')
for col in ['GROSS_SQFT','BUILDING_COUNT','ROOMS','ORG_COUNT']:
    out[col] = out[col].apply(lambda x: (f"{int(x):,}" if pd.notna(x) else ''))

# Append grand total at the end
final = pd.concat([out.drop(columns=['group_order','row_order_in_group']), grand], ignore_index=True)
for col in ['GROSS_SQFT','BUILDING_COUNT','ROOMS','ORG_COUNT']:
    # format grand totals
    if pd.api.types.is_numeric_dtype(final[col]):
        final[col] = final[col].apply(lambda x: (f"{int(x):,}" if pd.notna(x) else ''))

# Select and rename columns for presentation
answer = final.rename(columns={
    'OWNERSHIP_TYPE_DISPLAY':'Ownership Type',
    'BUILDING_USE':'Usage Type',
    'BUILDING_COUNT':'Number of Buildings',
    'GROSS_SQFT':'Gross Square Footage',
    'ROOMS':'Number of Rooms',
    'ORG_COUNT':'Number of Organizations'
})[['Ownership Type','Usage Type','Number of Buildings','Gross Square Footage','Number of Rooms','Number of Organizations']]

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
