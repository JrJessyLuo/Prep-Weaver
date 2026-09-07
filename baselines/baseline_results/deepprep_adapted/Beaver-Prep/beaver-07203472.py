import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'PARENT_BUILDING_NUMBER', 'BUILDING_USE', 'EXT_GROSS_AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NUMBER', 'PARENT_BUILDING_NUMBER', 'BUILDING_USE', 'EXT_GROSS_AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='first').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY', 'FCLT_ORGANIZATION_KEY', 'ORGANIZATION_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # trim and collapse repeated whitespace
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # trim and collapse repeated whitespace
        s = str(s).strip()
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ORGANIZATION_NAME"] = table_1["ORGANIZATION_NAME"].apply(_std_apply)

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

prepared_table_1 = _prep_1(tables['table_6'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_rooms = prepared_table_2

# Assume prepared_buildings and prepared_rooms are available DataFrames from the per-table targets
bld = prepared_buildings.copy()
rooms = prepared_rooms.drop_duplicates()

# Exclude subdivisions: keep only buildings without a parent (null/NaN or empty)
bld_main = bld[bld['PARENT_BUILDING_NUMBER'].isna() | (bld['PARENT_BUILDING_NUMBER'].astype(str).str.strip() == 'nan') | (bld['PARENT_BUILDING_NUMBER'].astype(str).str.strip() == '')]

# Normalize numeric
bld_main['EXT_GROSS_AREA'] = pd.to_numeric(bld_main['EXT_GROSS_AREA'], errors='coerce').fillna(0)

# Join rooms to buildings to get orgs per building
br = bld_main[['FCLT_BUILDING_KEY','BUILDING_USE','EXT_GROSS_AREA']].merge(
    rooms[['FCLT_BUILDING_KEY','FCLT_ORGANIZATION_KEY']].dropna(subset=['FCLT_ORGANIZATION_KEY']).astype({'FCLT_ORGANIZATION_KEY': str}),
    on='FCLT_BUILDING_KEY', how='left'
)

# Compute per-building org counts
orgs_per_bld = br.groupby('FCLT_BUILDING_KEY')['FCLT_ORGANIZATION_KEY'].nunique(dropna=True).reset_index(name='unique_orgs')

bld_with_orgs = bld_main.merge(orgs_per_bld, on='FCLT_BUILDING_KEY', how='left')
bld_with_orgs['unique_orgs'] = bld_with_orgs['unique_orgs'].fillna(0).astype(int)

# Map building use type label: if use indicates residence, label as RESIDENTIAL
# Treat codes starting with 'RES' or equal to 'RES' (case-insensitive) as residential
use_series = bld_with_orgs['BUILDING_USE'].astype(str).str.upper().fillna('')
bld_with_orgs['USE_TYPE'] = use_series.where(~use_series.str.startswith('RES'), 'RESIDENTIAL')

# Aggregate by use type
agg = bld_with_orgs.groupby('USE_TYPE').agg(
    buildings=('FCLT_BUILDING_KEY','nunique'),
    gross_sqft=('EXT_GROSS_AREA','sum'),
    unique_orgs=('unique_orgs','sum')
).reset_index()

# Totals row across all types
total_row = pd.DataFrame({
    'USE_TYPE': ['TOTAL'],
    'buildings': [bld_with_orgs['FCLT_BUILDING_KEY'].nunique()],
    'gross_sqft': [bld_with_orgs['EXT_GROSS_AREA'].sum()],
    'unique_orgs': [bld_with_orgs['unique_orgs'].sum()]
})

result = pd.concat([agg, total_row], ignore_index=True)

# Round to integers and format with commas
for col in ['buildings','gross_sqft','unique_orgs']:
    result[col] = result[col].round(0).astype(int).map(lambda x: f"{x:,}")

# Final output
target = result[['USE_TYPE','buildings','gross_sqft','unique_orgs']].rename(columns={
    'USE_TYPE':'use_type',
    'buildings':'number_of_buildings',
    'gross_sqft':'total_gross_sqft',
    'unique_orgs':'number_of_organizations'
})

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
