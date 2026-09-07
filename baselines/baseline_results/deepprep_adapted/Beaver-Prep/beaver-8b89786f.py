import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR_KEY', 'SPACE_UNIT_KEY', 'SPACE_USAGE_KEY', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'FLOOR_KEY', 'SPACE_UNIT_KEY', 'SPACE_USAGE_KEY', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FLOOR_KEY"] = table_1["FLOOR_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_ROOM", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_ROOM"] = table_1["BUILDING_ROOM"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_ROOM_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_ROOM_NAME"] = table_1["BUILDING_ROOM_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ROOM_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ROOM_NUMBER"] = table_1["ROOM_NUMBER"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_space_units", func="""
    # import pandas as pd
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Normalize key-like numeric columns into clean string keys (e.g., 63000.0 -> "63000")
    #     def key_to_str(x):
    #         if pd.isna(x):
    #             return None
    #         try:
    #             xf = float(x)
    #             if xf.is_integer():
    #                 return str(int(xf))
    #             return str(xf)
    #         except Exception:
    #             return str(x).strip()
    # 
    #     df["SPACE_UNIT_KEY"] = df["SPACE_UNIT_KEY"].apply(key_to_str)
    #     df["SPACE_USAGE_KEY"] = df["SPACE_USAGE_KEY"].apply(key_to_str)
    # 
    #     # Keep only required target columns
    #     df = df[[
    #         "BUILDING_KEY",
    #         "FLOOR_KEY",
    #         "SPACE_UNIT_KEY",
    #         "SPACE_USAGE_KEY",
    #         "BUILDING_ROOM",
    #         "BUILDING_ROOM_NAME",
    #         "ROOM_NUMBER"
    #     ]]
    #     return df
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Normalize key-like numeric columns into clean string keys (e.g., 63000.0 -> "63000")
        def key_to_str(x):
            if pd.isna(x):
                return None
            try:
                xf = float(x)
                if xf.is_integer():
                    return str(int(xf))
                return str(xf)
            except Exception:
                return str(x).strip()

        df["SPACE_UNIT_KEY"] = df["SPACE_UNIT_KEY"].apply(key_to_str)
        df["SPACE_USAGE_KEY"] = df["SPACE_USAGE_KEY"].apply(key_to_str)

        # Keep only required target columns
        df = df[[
            "BUILDING_KEY",
            "FLOOR_KEY",
            "SPACE_UNIT_KEY",
            "SPACE_USAGE_KEY",
            "BUILDING_ROOM",
            "BUILDING_ROOM_NAME",
            "ROOM_NUMBER"
        ]]
        return df
    prepared_space_units = process_tables(table_1)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Terminate(result=['prepared_space_units'])
    # Terminate
    result = {'prepared_space_units': prepared_space_units}
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
    # StandardizeString(table_name="table_1", column_name="BUILDING_STREET_ADDRESS", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)  # collapse multiple spaces
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)  # collapse multiple spaces
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_STREET_ADDRESS"] = table_1["BUILDING_STREET_ADDRESS"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'BUILDING_NUMBER'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FLOOR"] = table_1["FLOOR"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FLOOR_KEY"] = table_1["FLOOR_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # normalize outer whitespace; keep internal spacing as-is
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # normalize outer whitespace; keep internal spacing as-is
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FLOOR_NAME"] = table_1["FLOOR_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FLOOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FLOOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FLOOR_KEY', 'FLOOR', 'FLOOR_NAME'])
    # SelectCol
    _cols = [c for c in ['FLOOR_KEY', 'FLOOR', 'FLOOR_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['space_usage_key'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['space_usage_key'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="space_usage_key", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['space_usage_key'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['space_usage_key']
    if _dtype == "datetime64":
        table_1['space_usage_key'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['space_usage_key'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['space_usage_key'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['space_usage_key'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SPACE_USAGE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SPACE_USAGE'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SPACE_USAGE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # Normalize common 'nan' textual artifacts just in case
    #     if s.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # Normalize common 'nan' textual artifacts just in case
        if s.lower() in {"nan", "none", "null", ""}:
            return None
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SPACE_USAGE"] = table_1["SPACE_USAGE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SPACE_USAGE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SPACE_USAGE'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['space_usage_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['space_usage_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['space_usage_key', 'SPACE_USAGE'])
    # SelectCol
    _cols = [c for c in ['space_usage_key', 'SPACE_USAGE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
def _prep_5(table_1):
    return table_1.copy()
def _prep_6(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY'], ascending=[True, True, True, True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY'], ascending=[True, True, True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ROOM", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().upper()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ROOM"] = table_1["ROOM"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'FLOOR_KEY', 'ROOM', 'ORGANIZATION_KEY', 'ORGANIZATION_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
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
prepared_space_units = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_floors = prepared_table_3
prepared_table_4 = _prep_4(tables['table_10'])
prepared_space_usage = prepared_table_4
prepared_table_5 = _prep_5(tables['table_6'])
prepared_table_6 = _prep_6(tables['table_5'])
prepared_org_rooms = prepared_table_6

# Assume prepared_* dataframes exist per targets.
sp = prepared_space_units.copy()
# Normalize key types/whitespace for robust joins
sp['BUILDING_KEY'] = sp['BUILDING_KEY'].astype(str).str.strip()
sp['FLOOR_KEY'] = sp['FLOOR_KEY'].astype(str).str.strip()
sp['SPACE_USAGE_KEY'] = sp['SPACE_USAGE_KEY'].astype(str).str.strip()

bldg = prepared_buildings.copy()
bldg['BUILDING_KEY'] = bldg['BUILDING_KEY'].astype(str).str.strip()

fl = prepared_floors.copy()
fl['FLOOR_KEY'] = fl['FLOOR_KEY'].astype(str).str.strip()

su = prepared_space_usage.copy()
su['space_usage_key'] = su['space_usage_key'].astype(str).str.strip()

org = prepared_org_rooms.copy()
org['BUILDING_KEY'] = org['BUILDING_KEY'].astype(str).str.strip()
org['FLOOR_KEY'] = org['FLOOR_KEY'].astype(str).str.strip()
org['ROOM'] = org['ROOM'].astype(str).str.strip()

# Filter to building 36 using building number/name from buildings table, joining first to find BUILDING_KEY of number '36'
# If BUILDING_NUMBER holds the canonical building identifier like '36', match on that; otherwise assume BUILDING_KEY equals that identifier.
# Create a building selector for '36' in either key or number.
bldg_sel_keys = set(bldg.loc[(bldg['BUILDING_NUMBER'].astype(str).str.strip()=='36') | (bldg['BUILDING_KEY'].astype(str).str.strip()=='36'), 'BUILDING_KEY'].astype(str).str.strip())
if len(bldg_sel_keys)==0:
    # Fallback: use raw '36'
    bldg_sel_keys = {'36'}

sp36 = sp[sp['BUILDING_KEY'].isin(bldg_sel_keys)].copy()

# Join building info
sp36 = sp36.merge(bldg[['BUILDING_KEY','BUILDING_NAME','BUILDING_STREET_ADDRESS']], on='BUILDING_KEY', how='left')

# Join floor info
sp36 = sp36.merge(fl[['FLOOR_KEY','FLOOR','FLOOR_NAME']], on='FLOOR_KEY', how='left')

# Join space usage
sp36 = sp36.merge(su.rename(columns={'space_usage_key':'SPACE_USAGE_KEY'}), on='SPACE_USAGE_KEY', how='left')

# Prepare org aggregation by building+floor
org_bf = org[org['BUILDING_KEY'].isin(bldg_sel_keys)].copy()
# Distinct organizations per building-floor
org_counts = (org_bf.dropna(subset=['ORGANIZATION_KEY'])
                 .groupby(['BUILDING_KEY','FLOOR_KEY'])['ORGANIZATION_KEY']
                 .nunique()
                 .reset_index(name='num_organizations_on_floor'))

# Space unit counts per building-floor from sp table
su_counts = (sp36.groupby(['BUILDING_KEY','FLOOR_KEY'])['SPACE_UNIT_KEY']
                 .nunique()
                 .reset_index(name='num_space_units_on_floor'))

# Attach counts to each space unit row
sp36 = sp36.merge(org_counts, on=['BUILDING_KEY','FLOOR_KEY'], how='left')
sp36 = sp36.merge(su_counts, on=['BUILDING_KEY','FLOOR_KEY'], how='left')

# Final selection of columns
target = sp36[['SPACE_UNIT_KEY', 'BUILDING_ROOM', 'BUILDING_ROOM_NAME', 'ROOM_NUMBER', 'FLOOR', 'FLOOR_NAME', 'BUILDING_NAME', 'BUILDING_STREET_ADDRESS', 'SPACE_USAGE', 'num_organizations_on_floor', 'num_space_units_on_floor']]

# target now contains all space units in building 36 with required fields and counts

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
