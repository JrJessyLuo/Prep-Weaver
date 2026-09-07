import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY', 'FLOOR'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY', 'FLOOR'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'FLOOR'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'FLOOR'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    #     s = str(s).strip()
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return " ".join(s.split())
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
    #     s = str(s).strip()
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return " ".join(s.split())
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
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return " ".join(s.split())
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_NUMBER'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'BUILDING_NUMBER'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'krb_name', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'krb_name', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['krb_name', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['krb_name', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="krb_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["krb_name"] = table_1["krb_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="KRB_NAME_UPPERCASE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["KRB_NAME_UPPERCASE"] = table_1["KRB_NAME_UPPERCASE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFICE_LOCATION", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     # normalize to uppercase for consistent downstream building-key parsing
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        # normalize to uppercase for consistent downstream building-key parsing
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFICE_LOCATION"] = table_1["OFFICE_LOCATION"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'krb_name', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'krb_name', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     v = str(s).strip().upper()
    #     return v
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        v = str(s).strip().upper()
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_MOIRA_MAILING_LIST"] = table_1["IS_MOIRA_MAILING_LIST"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["MOIRA_LIST_KEY"] = table_1["MOIRA_LIST_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # canonical name for case-insensitive prefix filtering
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # canonical name for case-insensitive prefix filtering
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_NAME"] = table_1["MOIRA_LIST_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_ACTIVE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["IS_ACTIVE"] = table_1["IS_ACTIVE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_9'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_people = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
prepared_moira_lists = prepared_table_4

# Inputs: prepared_rooms, prepared_buildings, prepared_people, prepared_moira_lists, and a memberships bridge table (people-to-lists)
# Assumptions for integration:
# - A memberships table named prepared_memberships exists with columns: MIT_ID, MOIRA_LIST_KEY (or MOIRA_LIST_NAME) linking people to lists.
#   If the bridge uses kerberos instead of MIT_ID, rename to MIT_ID via lookup on prepared_people.
# - OFFICE_LOCATION pattern like 'E94-1573D' -> building key 'E94' (substring before first '-')

# 1) Compute building with most distinct floors from rooms
rooms = prepared_rooms.copy()
rooms['FLOOR_NORM'] = rooms['FLOOR'].astype(str).str.strip().str.lower()
floors_per_bldg = rooms.dropna(subset=['FCLT_BUILDING_KEY', 'FLOOR_NORM']).groupby('FCLT_BUILDING_KEY')['FLOOR_NORM'].nunique().reset_index(name='num_floors')
max_bldg_key = floors_per_bldg.sort_values(['num_floors','FCLT_BUILDING_KEY'], ascending=[False, True]).head(1)['FCLT_BUILDING_KEY'].iloc[0]

# 2) Get building names
bldg_row = prepared_buildings[prepared_buildings['FCLT_BUILDING_KEY'] == max_bldg_key].head(1)
building_name = (bldg_row['BUILDING_NAME'].iloc[0]
                 if ('BUILDING_NAME' in bldg_row and pd.notna(bldg_row['BUILDING_NAME'].iloc[0]))
                 else (bldg_row['BUILDING_NAME_LONG'].iloc[0] if 'BUILDING_NAME_LONG' in bldg_row else max_bldg_key))

# 3) Identify employees in that building (by office location)
people = prepared_people.copy()
people['OFFICE_LOCATION'] = people['OFFICE_LOCATION'].astype(str)
people['OFFICE_BLDG_KEY'] = people['OFFICE_LOCATION'].str.split('-', n=1).str[0].str.strip()
# Some office locations may be lowercase like 'w98-299a'; normalize case to match building keys' case
people['OFFICE_BLDG_KEY_UP'] = people['OFFICE_BLDG_KEY'].str.upper()
max_bldg_key_up = str(max_bldg_key).upper()
people_in_bldg = people[people['OFFICE_BLDG_KEY_UP'] == max_bldg_key_up]

# 4) Filter people by kerberos starting with 'c' (case-insensitive)
people_in_bldg = people_in_bldg[people_in_bldg['krb_name'].astype(str).str.startswith(('c','C'))]

# 5) Memberships join to get lists they subscribe to
# Expect prepared_memberships with at least columns: MIT_ID and MOIRA_LIST_KEY (preferred) or MOIRA_LIST_NAME
m = prepared_memberships.copy()
# If memberships contain MOIRA_LIST_NAME instead of key, join on name; otherwise join on key
lists = prepared_moira_lists.copy()
# standardize list name case
lists['MOIRA_LIST_NAME_UP'] = lists['MOIRA_LIST_NAME'].astype(str).str.strip().str.upper()

if 'MOIRA_LIST_KEY' in m.columns and 'MOIRA_LIST_KEY' in lists.columns:
    merged = m.merge(lists[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']], on='MOIRA_LIST_KEY', how='inner')
else:
    m['MOIRA_LIST_NAME_UP'] = m['MOIRA_LIST_NAME'].astype(str).str.strip().str.upper()
    merged = m.merge(lists[['MOIRA_LIST_NAME','MOIRA_LIST_NAME_UP','IS_ACTIVE','IS_MOIRA_MAILING_LIST']], on='MOIRA_LIST_NAME_UP', how='inner')

# 6) Filter to active Moira mailing lists whose names start with 'a' (case-insensitive)
merged = merged[(merged['IS_MOIRA_MAILING_LIST'] == 'Y') & (merged['IS_ACTIVE'] == 'Y')]
merged['MOIRA_LIST_NAME_LOW'] = merged['MOIRA_LIST_NAME'].astype(str).str.strip().str.lower()
merged = merged[merged['MOIRA_LIST_NAME_LOW'].str.startswith('a')]

# 7) Join people filter with memberships
people_cols = people_in_bldg[['MIT_ID','krb_name']].drop_duplicates()
subscribed = people_cols.merge(merged, on='MIT_ID', how='inner')

# 8) Prepare final answer: building name and list names (distinct)
result = subscribed[['MOIRA_LIST_NAME']].drop_duplicates().assign(BUILDING_NAME=building_name)
# Reorder columns
result = result[['BUILDING_NAME','MOIRA_LIST_NAME']]

answer = result

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
