import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MOIRA_LIST_MEMBER_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID']
    if _dtype == "datetime64":
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    #     # kerberos usernames are typically case-insensitive; keep as lowercase for stable joining
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", ""]:
            return None
        # kerberos usernames are typically case-insensitive; keep as lowercase for stable joining
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_MIT_ID", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    #     # remove a trailing .0 if present (common from float-to-string)
    #     if re.match(r'^\d+\.0$', s):
    #         s = s[:-2]
    #     # keep only pure digits; otherwise null
    #     if not re.match(r'^\d+$', s):
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", ""]:
            return None
        # remove a trailing .0 if present (common from float-to-string)
        if re.match(r'^\d+\.0$', s):
            s = s[:-2]
        # keep only pure digits; otherwise null
        if not re.match(r'^\d+$', s):
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_MIT_ID"] = table_1["MOIRA_LIST_MEMBER_MIT_ID"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MOIRA_LIST_MEMBER_MIT_ID", dtype="Int64")
    # CastType
    _dtype = 'Int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MOIRA_LIST_MEMBER_MIT_ID']
    if _dtype == "datetime64":
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MOIRA_LIST_MEMBER_MIT_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_MEMBER_MIT_ID', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_MEMBER_MIT_ID', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="KRB_NAME_UPPERCASE", func="""
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
    table_1["KRB_NAME_UPPERCASE"] = table_1["KRB_NAME_UPPERCASE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="KRB_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        if s.lower() in ["nan", "none", ""]:
            return None
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["KRB_NAME"] = table_1["KRB_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OFFICE_LOCATION", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        if s.lower() in ["nan", "none", ""]:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OFFICE_LOCATION"] = table_1["OFFICE_LOCATION"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'KRB_NAME', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'KRB_NAME', 'KRB_NAME_UPPERCASE', 'OFFICE_LOCATION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MIT_ID'], keep='last').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
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
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
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
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['BUILDING_NUMBER'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['BUILDING_NUMBER'], ascending=[True])

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
prepared_mailing_list_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_people_offices = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_buildings = prepared_table_3

ml = prepared_mailing_list_members.copy()
people = prepared_people_offices.copy()

# Normalize keys
# MIT IDs
ml['MOIRA_LIST_MEMBER_MIT_ID'] = pd.to_numeric(ml['MOIRA_LIST_MEMBER_MIT_ID'], errors='coerce').astype('Int64')
people['MIT_ID'] = pd.to_numeric(people['MIT_ID'], errors='coerce').astype('Int64')

# Kerberos usernames: strip and uppercase in ml; ensure people has uppercase variant
ml['KRB_FROM_MEMBER'] = ml['moira_list_member'].astype(str).str.strip().str.upper()
people['KRB_NAME_UPPERCASE'] = people['KRB_NAME_UPPERCASE'].astype(str).str.strip()

# Build two linkage paths and union them to maximize matches
join_on_mit = ml.merge(people[['MIT_ID','OFFICE_LOCATION']], left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID', how='inner')
join_on_krb = ml.merge(people[['KRB_NAME_UPPERCASE','OFFICE_LOCATION']], left_on='KRB_FROM_MEMBER', right_on='KRB_NAME_UPPERCASE', how='inner')

# Standardize columns
join_on_mit = join_on_mit[['MOIRA_LIST_KEY','OFFICE_LOCATION']]
join_on_krb = join_on_krb[['MOIRA_LIST_KEY','OFFICE_LOCATION']]

joined = pd.concat([join_on_mit, join_on_krb], ignore_index=True).drop_duplicates()

# Filter to people with physical offices in building 24
# Assume office codes like '24-xxx' or '24xxx'; match starting with '24' followed by '-' or a digit
mask_b24 = joined['OFFICE_LOCATION'].astype(str).str.match(r'^\s*24(\-|\d)')
joined_b24 = joined[mask_b24]

# Count subscribers per mailing list among building 24 occupants
counts = joined_b24.groupby('MOIRA_LIST_KEY', as_index=False).size().rename(columns={'size':'subscriber_count'})

# Identify the most subscribed list and its count
if counts.empty:
    result = pd.DataFrame([{'mailing_list': None, 'subscriber_count': 0}])
else:
    top = counts.sort_values(['subscriber_count','MOIRA_LIST_KEY'], ascending=[False, True]).head(1)
    result = top.rename(columns={'MOIRA_LIST_KEY':'mailing_list'})[['mailing_list','subscriber_count']]

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
