import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
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
    table_1["MOIRA_LIST_KEY"] = table_1["MOIRA_LIST_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
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
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
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
    table_1["IS_MOIRA_MAILING_LIST"] = table_1["IS_MOIRA_MAILING_LIST"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_ACTIVE", func="""
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
    table_1["IS_ACTIVE"] = table_1["IS_ACTIVE"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_ACTIVE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_ACTIVE'] if c in table_1.columns]
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
    # StandardizeDatetime(table_name="table_1", column_name="LAST_UPDATE_DATE", date_format="%d-%b-%y")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['LAST_UPDATE_DATE'] = table_1['LAST_UPDATE_DATE'].apply(_sd_parse)
    if '%d-%b-%y':
        table_1['LAST_UPDATE_DATE'] = table_1['LAST_UPDATE_DATE'].dt.strftime('%d-%b-%y')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     return s2.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip()
        return s2.upper()
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
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_MEMBER_FULL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # preserve null-like values as-is; otherwise trim
    #     s2 = str(s)
    #     if s2.lower() == 'nan':
    #         return None
    #     return s2.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # preserve null-like values as-is; otherwise trim
        s2 = str(s)
        if s2.lower() == 'nan':
            return None
        return s2.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_MEMBER_FULL_NAME"] = table_1["MOIRA_LIST_MEMBER_FULL_NAME"].apply(_std_apply)

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
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'moira_list_member'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'moira_list_member'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="STUDENT_YEAR", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['STUDENT_YEAR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['STUDENT_YEAR']
    if _dtype == "datetime64":
        table_1['STUDENT_YEAR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['STUDENT_YEAR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['STUDENT_YEAR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['STUDENT_YEAR'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMAIL_ADDRESS", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMAIL_ADDRESS"] = table_1["EMAIL_ADDRESS"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FULL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     # normalize internal whitespace
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        # normalize internal whitespace
        return " ".join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FULL_NAME"] = table_1["FULL_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FULL_NAME_UPPERCASE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return " ".join(s.split()).upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return " ".join(s.split()).upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FULL_NAME_UPPERCASE"] = table_1["FULL_NAME_UPPERCASE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DEPARTMENT_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ("nan", "none", ""):
    #         return None
    #     return " ".join(s.split())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ("nan", "none", ""):
            return None
        return " ".join(s.split())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DEPARTMENT_NAME"] = table_1["DEPARTMENT_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     # keep rows that are matchable by at least one key
    #     return (row.get('EMAIL_ADDRESS') is not None) or (row.get('FULL_NAME_UPPERCASE') is not None) or (row.get('FULL_NAME') is not None)
    # """)
    # Filter
    def filter_func(row):
        # keep rows that are matchable by at least one key
        return (row.get('EMAIL_ADDRESS') is not None) or (row.get('FULL_NAME_UPPERCASE') is not None) or (row.get('FULL_NAME') is not None)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EMAIL_ADDRESS'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EMAIL_ADDRESS'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FULL_NAME_UPPERCASE', 'DEPARTMENT_NAME'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FULL_NAME_UPPERCASE', 'DEPARTMENT_NAME'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FULL_NAME', 'FULL_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['FULL_NAME', 'FULL_NAME_UPPERCASE', 'EMAIL_ADDRESS', 'DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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

prepared_table_1 = _prep_1(tables['table_10'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_owners = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_people = prepared_table_4

# Assume prepared_* DataFrames already created per table_targets
lists = prepared_lists.copy()
members = prepared_memberships.copy()
owners = prepared_owners.copy()
people = prepared_people.copy()

# Normalize keys/identifiers
for df,col in [(lists,'MOIRA_LIST_NAME'), (lists,'MOIRA_LIST_KEY'), (members,'MOIRA_LIST_KEY'), (members,'MOIRA_LIST_OWNER_KEY'), (members,'moira_list_member')]:
    df[col] = df[col].astype(str).str.strip()
people['EMAIL_ADDRESS'] = people['EMAIL_ADDRESS'].astype(str).str.strip().str.lower()
people['FULL_NAME_UPPERCASE'] = people['FULL_NAME_UPPERCASE'].astype(str).str.strip()

# Filter to active mailing lists whose names start with 'e' (case-insensitive)
lists_f = lists[(lists['IS_ACTIVE'].str.upper() == 'Y') & (lists['IS_MOIRA_MAILING_LIST'].str.upper() == 'Y')]
lists_f = lists_f[lists_f['MOIRA_LIST_NAME'].str.lower().str.startswith('e')]

# Join members to those lists
lm = members.merge(lists_f[['MOIRA_LIST_KEY','MOIRA_LIST_NAME']], on='MOIRA_LIST_KEY', how='inner')

# Try to map members to people by email address first (moira_list_member often stores login/email). Normalize member as email-like
lm['member_norm'] = lm['moira_list_member'].astype(str).str.strip().str.lower()
# Left join to people on email
lm_people = lm.merge(people[['EMAIL_ADDRESS','DEPARTMENT_NAME']], left_on='member_norm', right_on='EMAIL_ADDRESS', how='left')

# If email match missing, optionally try a heuristic name match using FULL_NAME vs MOIRA_LIST_MEMBER_FULL_NAME uppercase
# Prepare name keys
people_name = people[['FULL_NAME_UPPERCASE','DEPARTMENT_NAME']].dropna().copy()
people_name.rename(columns={'FULL_NAME_UPPERCASE':'NAME_KEY','DEPARTMENT_NAME':'DEPT_FROM_NAME'}, inplace=True)
name_key = lm['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.strip().str.upper()
lm_people['NAME_KEY'] = name_key
# Name-based enrichment
lm_people = lm_people.merge(people_name, on='NAME_KEY', how='left')

# Determine if member is CS/EECS student: treat DEPARTMENT_NAME containing 'Computer Sci' or 'Electrical Eng & Computer Sci' as CS
def is_cs(dept):
    if not isinstance(dept, str):
        return False
    d = dept.lower()
    return ('computer sci' in d) or ('electrical eng & computer sci' in d) or ('electrical eng and computer sci' in d) or ('eecs' in d)

cs_flag_email = lm_people['DEPARTMENT_NAME'].apply(is_cs)
cs_flag_name = lm_people['DEPT_FROM_NAME'].apply(is_cs)
lm_people['is_cs'] = cs_flag_email | cs_flag_name

# Aggregate per list: member count and cs count
agg = lm_people.groupby(['MOIRA_LIST_KEY','MOIRA_LIST_NAME'], as_index=False).agg(
    member_count=('moira_list_member','count'),
    cs_count=('is_cs','sum')
)
agg['cs_ratio'] = agg['cs_count'] / agg['member_count']

# Keep lists with member count between 10 and 20 inclusive and cs_ratio > 0.75
eligible = agg[(agg['member_count'].between(10,20, inclusive='both')) & (agg['cs_ratio'] > 0.75)]

# Attach owner
owners_f = owners[['MOIRA_LIST_OWNER_KEY','OWNER']].drop_duplicates()
# Need one owner per list: take the most common owner per list in memberships subset
list_owner = members[members['MOIRA_LIST_KEY'].isin(eligible['MOIRA_LIST_KEY'])]
list_owner = list_owner[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY']].dropna()
# Select first owner per list (or mode if desired)
list_owner = list_owner.groupby('MOIRA_LIST_KEY', as_index=False).agg(MOIRA_LIST_OWNER_KEY=('MOIRA_LIST_OWNER_KEY','first'))
list_owner = list_owner.merge(owners_f, on='MOIRA_LIST_OWNER_KEY', how='left')

result = eligible.merge(list_owner[['MOIRA_LIST_KEY','OWNER']], on='MOIRA_LIST_KEY', how='left')

# Final output: list name, owner, member count
answer = result[['MOIRA_LIST_NAME','OWNER','member_count']].rename(columns={
    'MOIRA_LIST_NAME':'list_name',
    'OWNER':'owner',
    'member_count':'member_count'
}).sort_values(['list_name'])

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
