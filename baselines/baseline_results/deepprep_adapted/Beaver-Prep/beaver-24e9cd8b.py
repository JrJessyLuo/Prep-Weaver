import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="ASSIGNABLE_AREA", mode="median")
    # MissingValueImputation
    table_1["ASSIGNABLE_AREA"] = table_1["ASSIGNABLE_AREA"].fillna(table_1["ASSIGNABLE_AREA"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_BUILDING_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_BUILDING_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="CAMPUS_SECTOR", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "(null)", "none", ""]:
    #         return None
    #     s = re.sub(r"\s+", " ", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "(null)", "none", ""]:
            return None
        s = re.sub(r"\s+", " ", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["CAMPUS_SECTOR"] = table_1["CAMPUS_SECTOR"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SITE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "(null)", "none", ""]:
    #         return None
    #     s = re.sub(r"\s+", " ", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "(null)", "none", ""]:
            return None
        s = re.sub(r"\s+", " ", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SITE"] = table_1["SITE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OWNERSHIP_TYPE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "(null)", "none", ""]:
    #         return None
    #     s = re.sub(r"\s+", " ", s)
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "(null)", "none", ""]:
            return None
        s = re.sub(r"\s+", " ", s)
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OWNERSHIP_TYPE"] = table_1["OWNERSHIP_TYPE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "(null)", "none", ""]:
    #         return None
    #     s = re.sub(r"\s+", " ", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "(null)", "none", ""]:
            return None
        s = re.sub(r"\s+", " ", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "(null)", "none", ""]:
    #         return None
    #     s = re.sub(r"\s+", " ", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "(null)", "none", ""]:
            return None
        s = re.sub(r"\s+", " ", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 8 ----------------
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

    # ---------------- Step 9 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ASSIGNABLE_AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ASSIGNABLE_AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ASSIGNABLE_AREA']
    if _dtype == "datetime64":
        table_1['ASSIGNABLE_AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ASSIGNABLE_AREA'] = _series.astype(str)

    # ---------------- Step 10 ----------------
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

    # ---------------- Step 11 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="EXT_GROSS_AREA", mode="median")
    # MissingValueImputation
    table_1["EXT_GROSS_AREA"] = table_1["EXT_GROSS_AREA"].fillna(table_1["EXT_GROSS_AREA"].median())

    # ---------------- Step 12 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="NUM_OF_ROOMS", mode="median")
    # MissingValueImputation
    table_1["NUM_OF_ROOMS"] = table_1["NUM_OF_ROOMS"].fillna(table_1["NUM_OF_ROOMS"].median())

    # ---------------- Step 13 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="OWNERSHIP_TYPE", mode="mode")
    # MissingValueImputation
    table_1["OWNERSHIP_TYPE"] = table_1["OWNERSHIP_TYPE"].fillna(table_1["OWNERSHIP_TYPE"].mode().iloc[0])

    # ---------------- Step 14 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 15 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CAMPUS_SECTOR', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_NUMBER', 'SITE', 'OWNERSHIP_TYPE', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS', 'FCLT_BUILDING_KEY'])
    # SelectCol
    _cols = [c for c in ['CAMPUS_SECTOR', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_NUMBER', 'SITE', 'OWNERSHIP_TYPE', 'ASSIGNABLE_AREA', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS', 'FCLT_BUILDING_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 16 ----------------
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
prepared_buildings = prepared_table_1

# Start from prepared table
df = prepared_buildings.copy()

# Derive building name preference
df['BUILDING_DISPLAY_NAME'] = df['BUILDING_NAME'].fillna(df['BUILDING_NAME_LONG'])

# City/State inference: if not present in data, set placeholders or map from SITE if a lookup exists
# Here, set City/State as unknown due to lack of columns
df['CITY'] = pd.NA
df['STATE'] = pd.NA

# Ensure numeric
for c in ['ASSIGNABLE_AREA', 'EXT_GROSS_AREA', 'NUM_OF_ROOMS']:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors='coerce')

# If a floors column existed, we'd use it; since it's not available, set total floors to NaN
df['TOTAL_FLOORS'] = pd.NA

# Total number of organizations not available in source; set to NaN
df['TOTAL_ORGANIZATIONS'] = pd.NA

# Rank within sector by descending assignable area
df['RANK_IN_SECTOR'] = df.sort_values(['CAMPUS_SECTOR','ASSIGNABLE_AREA'], ascending=[True, False])\
    .groupby('CAMPUS_SECTOR').cumcount() + 1

# Per-building detail rows
detail_cols = ['CAMPUS_SECTOR','BUILDING_DISPLAY_NAME','CITY','STATE','TOTAL_FLOORS','ASSIGNABLE_AREA','NUM_OF_ROOMS','TOTAL_ORGANIZATIONS','OWNERSHIP_TYPE','RANK_IN_SECTOR']
detail = df[detail_cols].rename(columns={'BUILDING_DISPLAY_NAME':'BUILDING_NAME','ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA'})

# Subtotals per sector (only floors and assignable area required; floors unknown -> NaN sum)
subtotals = df.groupby('CAMPUS_SECTOR', as_index=False).agg({
    'ASSIGNABLE_AREA':'sum'
})
subtotals['TOTAL_FLOORS'] = pd.NA
subtotals['ROW_TYPE'] = 'SUBTOTAL'
subtotals = subtotals[['CAMPUS_SECTOR','TOTAL_FLOORS','ASSIGNABLE_AREA','ROW_TYPE']]

# Grand total
grand = pd.DataFrame({
    'CAMPUS_SECTOR': ['GRAND TOTAL'],
    'ASSIGNABLE_AREA': [df['ASSIGNABLE_AREA'].sum(skipna=True)],
    'TOTAL_FLOORS': [pd.NA],
    'ROW_TYPE': ['GRAND_TOTAL']
})

# Label detail rows
detail['ROW_TYPE'] = 'DETAIL'

# Prepare subtotal rows to align columns for final presentation
sub_detail_like = subtotals.merge(
    df[['CAMPUS_SECTOR']].drop_duplicates().assign(
        BUILDING_NAME=pd.NA, CITY=pd.NA, STATE=pd.NA, NUM_OF_ROOMS=pd.NA, TOTAL_ORGANIZATIONS=pd.NA, OWNERSHIP_TYPE=pd.NA, RANK_IN_SECTOR=pd.NA
    ),
    on='CAMPUS_SECTOR', how='left'
).drop_duplicates(subset=['CAMPUS_SECTOR'])
sub_detail_like = sub_detail_like.rename(columns={'ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA'})[
    ['CAMPUS_SECTOR','BUILDING_NAME','CITY','STATE','TOTAL_FLOORS','TOTAL_ASSIGNABLE_AREA','NUM_OF_ROOMS','TOTAL_ORGANIZATIONS','OWNERSHIP_TYPE','RANK_IN_SECTOR','ROW_TYPE']
]

grand_like = grand.assign(BUILDING_NAME=pd.NA, CITY=pd.NA, STATE=pd.NA, NUM_OF_ROOMS=pd.NA, TOTAL_ORGANIZATIONS=pd.NA, OWNERSHIP_TYPE=pd.NA, RANK_IN_SECTOR=pd.NA)
grand_like = grand_like.rename(columns={'ASSIGNABLE_AREA':'TOTAL_ASSIGNABLE_AREA'})[
    ['CAMPUS_SECTOR','BUILDING_NAME','CITY','STATE','TOTAL_FLOORS','TOTAL_ASSIGNABLE_AREA','NUM_OF_ROOMS','TOTAL_ORGANIZATIONS','OWNERSHIP_TYPE','RANK_IN_SECTOR','ROW_TYPE']
]

# Combine: interleave detail and subtotal per sector
out = []
for sector, grp in detail.sort_values(['CAMPUS_SECTOR','TOTAL_ASSIGNABLE_AREA'], ascending=[True, False]).groupby('CAMPUS_SECTOR', sort=False):
    out.append(grp)
    out.append(sub_detail_like[sub_detail_like['CAMPUS_SECTOR']==sector])
result = pd.concat(out + [grand_like], ignore_index=True)

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
