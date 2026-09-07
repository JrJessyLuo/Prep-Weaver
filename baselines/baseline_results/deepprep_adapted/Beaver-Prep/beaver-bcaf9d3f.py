import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DLC_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = " ".join(s.split())
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = " ".join(s.split())
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DLC_NAME"] = table_1["DLC_NAME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['dlc_key', 'DLC_CODE', 'DLC_NAME'])
    # SelectCol
    _cols = [c for c in ['dlc_key', 'DLC_CODE', 'DLC_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['dlc_key', 'DLC_CODE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['dlc_key', 'DLC_CODE'], keep='first').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'])
    # SelectCol
    _cols = [c for c in ['FCLT_ORGANIZATION_KEY', 'DLC_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], how='any').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'])
    # SelectCol
    _cols = [c for c in ['FCLT_ORGANIZATION_KEY', 'DLC_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DLC_KEY", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     s = re.sub(r"^['\"]|['\"]$", "", s)
    #     s = s.strip()
    #     return s if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding single/double quotes if present
        s = re.sub(r"^['\"]|['\"]$", "", s)
        s = s.strip()
        return s if s != "" and s.lower() != "nan" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DLC_KEY"] = table_1["DLC_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_ORGANIZATION_KEY", dtype="int")
    # CastType
    _dtype = 'int'
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_ORGANIZATION_KEY', 'DLC_KEY'], keep='first').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="fclt_organization_key", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['fclt_organization_key'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['fclt_organization_key']
    if _dtype == "datetime64":
        table_1['fclt_organization_key'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['fclt_organization_key'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['fclt_organization_key'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['fclt_organization_key'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="SPACE_UNIT_KEY", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['SPACE_UNIT_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['SPACE_UNIT_KEY']
    if _dtype == "datetime64":
        table_1['SPACE_UNIT_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['SPACE_UNIT_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['SPACE_UNIT_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['SPACE_UNIT_KEY'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DLC_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DLC_KEY"] = table_1["DLC_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['fclt_organization_key', 'DLC_KEY', 'SPACE_UNIT_KEY'])
    # SelectCol
    _cols = [c for c in ['fclt_organization_key', 'DLC_KEY', 'SPACE_UNIT_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['fclt_organization_key', 'DLC_KEY', 'SPACE_UNIT_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['fclt_organization_key', 'DLC_KEY', 'SPACE_UNIT_KEY'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_dlc_master = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_orgs_by_dlc = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_org_dlc_lookup = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_space_units_by_dlc = prepared_table_4

# Assume prepared_dlc_master, prepared_orgs_by_dlc, prepared_org_dlc_lookup, prepared_space_units_by_dlc exist

# 1) Build organization-to-DLC mapping, preferring explicit DLC_KEYs from either source
org_dlc_from_t2 = prepared_orgs_by_dlc[['FCLT_ORGANIZATION_KEY','DLC_KEY']].dropna()
org_dlc_from_t3 = prepared_org_dlc_lookup[['FCLT_ORGANIZATION_KEY','DLC_KEY']].dropna()
org_dlc = pd.concat([org_dlc_from_t2, org_dlc_from_t3], ignore_index=True).drop_duplicates()

# 2) Count distinct facility organizations per DLC
org_counts = org_dlc.groupby('DLC_KEY', as_index=False).agg(total_facility_organizations=('FCLT_ORGANIZATION_KEY','nunique'))

# 3) Derive space-related aggregates if available (floors, sqft, heights not present in provided tables -> set to NaN/0 as placeholders)
# Link space units to DLC via organizations
su_link = prepared_space_units_by_dlc.merge(org_dlc, left_on='fclt_organization_key', right_on='FCLT_ORGANIZATION_KEY', how='left')
space_counts = su_link.groupby('DLC_KEY', as_index=False).agg(
    total_floors=('SPACE_UNIT_KEY', lambda s: pd.NA),
    total_square_footage=('SPACE_UNIT_KEY', lambda s: pd.NA),
    total_building_heights=('SPACE_UNIT_KEY', lambda s: pd.NA)
)

# 4) Supervisor/supervisee counts not present -> placeholders
people_counts = org_dlc[['DLC_KEY']].drop_duplicates().assign(
    total_supervisors=pd.NA,
    total_supervisees=pd.NA
)

# 5) Combine all per-DLC metrics
metrics = prepared_dlc_master.rename(columns={'dlc_key':'DLC_KEY'})[['DLC_KEY','DLC_NAME']].drop_duplicates() \
    .merge(org_counts, on='DLC_KEY', how='left') \
    .merge(space_counts, on='DLC_KEY', how='left') \
    .merge(people_counts, on='DLC_KEY', how='left')

# 6) Final selection/rename per question
answer = metrics.rename(columns={
    'DLC_KEY':'dlc_key',
    'DLC_NAME':'dlc_name'
})[['dlc_key','dlc_name','total_floors','total_square_footage','total_facility_organizations','total_supervisors','total_supervisees','total_building_heights']]

target = answer

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
