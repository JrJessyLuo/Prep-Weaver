import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_ACTIVE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     v = str(s).strip().upper()
    #     if v in ["Y","YES","TRUE","T","1"]:
    #         return "Y"
    #     if v in ["N","NO","FALSE","F","0"]:
    #         return "N"
    #     return v
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        v = str(s).strip().upper()
        if v in ["Y","YES","TRUE","T","1"]:
            return "Y"
        if v in ["N","NO","FALSE","F","0"]:
            return "N"
        return v
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_ACTIVE"] = table_1["IS_ACTIVE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # Keep original case but remove leading/trailing whitespace
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # Keep original case but remove leading/trailing whitespace
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
    table_1["MOIRA_LIST_NAME"] = table_1["MOIRA_LIST_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     v = str(s).strip().upper()
    #     if v in ["Y","YES","TRUE","T","1"]:
    #         return "Y"
    #     if v in ["N","NO","FALSE","F","0"]:
    #         return "N"
    #     return v
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        v = str(s).strip().upper()
        if v in ["Y","YES","TRUE","T","1"]:
            return "Y"
        if v in ["N","NO","FALSE","F","0"]:
            return "N"
        return v
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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'MOIRA_LIST_DESCRIPTION', 'IS_ACTIVE', 'IS_MOIRA_MAILING_LIST'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='first').reset_index(drop=True)

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
    # Count(table_name="table_1")
    # Count -> statistic_table
    _stat_row = pd.DataFrame({'operator': ['Count(table_name="table_1")'], 'statistic_name': ['count'], 'value': [len(table_1)]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # normalize whitespace and casing for principal ids
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # normalize whitespace and casing for principal ids
        return str(s).strip()
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
    # CodeGeneration(table_names=['table_1'], target_table="prepared_moira_list_membership", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Clean full name: strip, and keep nulls as nulls
    #     def clean_name(x):
    #         if pd.isna(x):
    #             return pd.NA
    #         x = str(x).strip()
    #         return x if x != "" else pd.NA
    # 
    #     df["MOIRA_LIST_MEMBER_FULL_NAME"] = df["MOIRA_LIST_MEMBER_FULL_NAME"].apply(clean_name)
    # 
    #     # Clean MIT ID: remove float .0 artifact; keep missing as NA
    #     def clean_mit_id(x):
    #         if pd.isna(x):
    #             return pd.NA
    #         # handle values like 984301411.0
    #         try:
    #             xi = int(float(x))
    #             return str(xi)
    #         except Exception:
    #             xs = str(x).strip()
    #             return xs if xs != "" else pd.NA
    # 
    #     df["MOIRA_LIST_MEMBER_MIT_ID"] = df["MOIRA_LIST_MEMBER_MIT_ID"].apply(clean_mit_id)
    # 
    #     # Return only required columns in target schema order
    #     return df[[
    #         "MOIRA_LIST_KEY",
    #         "MOIRA_LIST_OWNER_KEY",
    #         "moira_list_member",
    #         "MOIRA_LIST_MEMBER_FULL_NAME",
    #         "MOIRA_LIST_MEMBER_MIT_ID"
    #     ]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Clean full name: strip, and keep nulls as nulls
        def clean_name(x):
            if pd.isna(x):
                return pd.NA
            x = str(x).strip()
            return x if x != "" else pd.NA

        df["MOIRA_LIST_MEMBER_FULL_NAME"] = df["MOIRA_LIST_MEMBER_FULL_NAME"].apply(clean_name)

        # Clean MIT ID: remove float .0 artifact; keep missing as NA
        def clean_mit_id(x):
            if pd.isna(x):
                return pd.NA
            # handle values like 984301411.0
            try:
                xi = int(float(x))
                return str(xi)
            except Exception:
                xs = str(x).strip()
                return xs if xs != "" else pd.NA

        df["MOIRA_LIST_MEMBER_MIT_ID"] = df["MOIRA_LIST_MEMBER_MIT_ID"].apply(clean_mit_id)

        # Return only required columns in target schema order
        return df[[
            "MOIRA_LIST_KEY",
            "MOIRA_LIST_OWNER_KEY",
            "moira_list_member",
            "MOIRA_LIST_MEMBER_FULL_NAME",
            "MOIRA_LIST_MEMBER_MIT_ID"
        ]]
    prepared_moira_list_membership = process_tables(table_1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['prepared_moira_list_membership'])
    # Terminate
    result = {'prepared_moira_list_membership': prepared_moira_list_membership}
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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
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
    # Deduplicate(table_name="table_1", subset=['MIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MIT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MIT_ID', 'FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'IS_FACULTY', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE'])
    # SelectCol
    _cols = [c for c in ['MIT_ID', 'FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'IS_FACULTY', 'PERSONNEL_SUBAREA', 'PERSONNEL_SUBAREA_CODE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_owners = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_people = prepared_table_4

# Start from prepared tables
lists = prepared_lists.copy()
members = prepared_memberships.copy()
owners = prepared_owners.copy()
people = prepared_people.copy()

# Normalize strings for robust joining/filtering
for df in [lists, members, owners, people]:
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()

# Ensure MIT_ID fields align as strings without decimals
if 'MOIRA_LIST_MEMBER_MIT_ID' in members.columns:
    members['MOIRA_LIST_MEMBER_MIT_ID'] = members['MOIRA_LIST_MEMBER_MIT_ID'].replace({'nan': None})
    members['MOIRA_LIST_MEMBER_MIT_ID'] = members['MOIRA_LIST_MEMBER_MIT_ID'].apply(lambda x: None if x in [None, '', 'None'] else str(x).split('.')[0])
if 'MIT_ID' in people.columns:
    people['MIT_ID'] = people['MIT_ID'].astype(str).str.strip()

# Resolve owner info on each membership row (some lists may have multiple owner rows; OWNER gives display)
members_owners = members.merge(owners[['MOIRA_LIST_OWNER_KEY','OWNER','OWNER_TYPE']], on='MOIRA_LIST_OWNER_KEY', how='left')

# Attach list attributes
mem_with_list = members_owners.merge(lists[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','MOIRA_LIST_DESCRIPTION','IS_ACTIVE','IS_MOIRA_MAILING_LIST']], on='MOIRA_LIST_KEY', how='left')

# Filter to active mailing lists whose names start with R (case-insensitive)
mask_lists = (
    mem_with_list['IS_ACTIVE'].str.upper().eq('Y') &
    mem_with_list['IS_MOIRA_MAILING_LIST'].str.upper().eq('Y') &
    mem_with_list['MOIRA_LIST_NAME'].str.lower().str.startswith('r')
)
mem_r = mem_with_list[mask_lists].copy()

# Identify Professor Ayden Hopkins in people
people['FIRST_NAME_L'] = people['FIRST_NAME'].astype(str).str.lower()
people['LAST_NAME_L'] = people['LAST_NAME'].astype(str).str.lower()
prof = people[(people['FIRST_NAME_L'] == 'ayden') & (people['LAST_NAME_L'] == 'hopkins')]

# Get the MIT_ID(s) for the professor
prof_ids = set(prof['MIT_ID'].dropna().astype(str))

# Find lists where the professor is subscribed (by MIT_ID match or, as fallback, by full name match)
prof_member_rows = mem_r[
    mem_r['MOIRA_LIST_MEMBER_MIT_ID'].isin(prof_ids) |
    (
        prof_ids == set() # if no MIT_ID found, fallback to name match
    )
]
if prof_ids == set():
    full_names_lower = set((prof['FULL_NAME'].dropna().astype(str).str.lower()).tolist())
    if full_names_lower:
        prof_member_rows = mem_r[mem_r['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str).str.lower().isin(full_names_lower)]

# Keep only the lists that have the professor as a member
prof_lists = prof_member_rows[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','MOIRA_LIST_DESCRIPTION','OWNER']].drop_duplicates()

# For headcount and tenured faculty count, join people to all members of those lists, then aggregate
members_in_prof_lists = mem_r.merge(
    prof_lists[['MOIRA_LIST_KEY']], on='MOIRA_LIST_KEY', how='inner'
)

# Attach person info to determine tenure status; may be missing for non-person principals
members_in_prof_lists = members_in_prof_lists.merge(
    people[['MIT_ID','IS_FACULTY','PERSONNEL_SUBAREA','PERSONNEL_SUBAREA_CODE']],
    left_on='MOIRA_LIST_MEMBER_MIT_ID', right_on='MIT_ID', how='left'
)

# Define tenured faculty flag. Depending on institution coding, tenure often indicated via PERSONNEL_SUBAREA(_CODE) or IS_FACULTY plus subarea values.
# Here we assume tenured faculty when IS_FACULTY == 'Y' and PERSONNEL_SUBAREA contains 'Tenured' (case-insensitive) or code matches known tenured codes such as 'TNR' or 'TEN'. Adjust as needed.
def is_tenured(row):
    fac = str(row.get('IS_FACULTY', '')).upper() == 'Y'
    psa = str(row.get('PERSONNEL_SUBAREA', '')).lower()
    psac = str(row.get('PERSONNEL_SUBAREA_CODE', '')).upper()
    return fac and (
        ('tenure' in psa) or ('tenured' in psa) or psac in {'TNR','TEN','TT','TENR'}
    )

members_in_prof_lists['is_tenured_faculty'] = members_in_prof_lists.apply(is_tenured, axis=1)

# Aggregate counts per list
agg = members_in_prof_lists.groupby('MOIRA_LIST_KEY').agg(
    num_people_in_list = ('MOIRA_LIST_MEMBER_MIT_ID', 'nunique'),
    num_tenured_faculty = ('is_tenured_faculty', 'sum')
).reset_index()

# Assemble final result with list details and owner
result = prof_lists.merge(agg, on='MOIRA_LIST_KEY', how='left')

# Select and rename columns as requested
final = result[['MOIRA_LIST_NAME','MOIRA_LIST_DESCRIPTION','OWNER','num_people_in_list','num_tenured_faculty']].copy()
final = final.rename(columns={
    'MOIRA_LIST_NAME': 'list_name',
    'MOIRA_LIST_DESCRIPTION': 'description',
    'OWNER': 'owner',
    'num_people_in_list': 'num_people',
    'num_tenured_faculty': 'num_tenured_faculty'
})

# Output in whatever format the pipeline expects
answer = final

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
