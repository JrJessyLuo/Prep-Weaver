import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ORGANIZATION'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ORGANIZATION'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # collapse internal whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # collapse internal whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ORGANIZATION"] = table_1["ORGANIZATION"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ORGANIZATION_NAME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        s = re.sub(r'\s+', ' ', s)
        return s
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
    # StandardizeString(table_name="table_1", column_name="DLC_KEY", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # keep NaN-like values as-is
    #     s0 = str(s).strip()
    #     if s0.lower() in ('nan', 'none', ''):
    #         return s
    #     if (len(s0) >= 2) and ((s0[0] == '"' and s0[-1] == '"') or (s0[0] == "'" and s0[-1] == "'")):
    #         s0 = s0[1:-1].strip()
    #     s0 = re.sub(r'\s+', ' ', s0)
    #     return s0
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # keep NaN-like values as-is
        s0 = str(s).strip()
        if s0.lower() in ('nan', 'none', ''):
            return s
        if (len(s0) >= 2) and ((s0[0] == '"' and s0[-1] == '"') or (s0[0] == "'" and s0[-1] == "'")):
            s0 = s0[1:-1].strip()
        s0 = re.sub(r'\s+', ' ', s0)
        return s0
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DLC_KEY"] = table_1["DLC_KEY"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_ORGANIZATION_KEY', 'ORGANIZATION_ID', 'ORGANIZATION', 'ORGANIZATION_NAME', 'ORGANIZATION_LEVEL', 'ORGANIZATION_NUMBER', 'DLC_KEY'])
    # SelectCol
    _cols = [c for c in ['FCLT_ORGANIZATION_KEY', 'ORGANIZATION_ID', 'ORGANIZATION', 'ORGANIZATION_NAME', 'ORGANIZATION_LEVEL', 'ORGANIZATION_NUMBER', 'DLC_KEY'] if c in table_1.columns]
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
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['dlc_key', 'HIERARCHY_TYPE'])
    # SelectCol
    _cols = [c for c in ['dlc_key', 'HIERARCHY_TYPE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="dlc_key", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding single/double quotes if present
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
    table_1["dlc_key"] = table_1["dlc_key"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HIERARCHY_TYPE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
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
    table_1["HIERARCHY_TYPE"] = table_1["HIERARCHY_TYPE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['dlc_key', 'HIERARCHY_TYPE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['dlc_key', 'HIERARCHY_TYPE'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['dlc_key', 'HIERARCHY_TYPE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['dlc_key', 'HIERARCHY_TYPE'], keep='first').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="DIRECTORY_ORG_UNIT_TITLE", mode="mode")
    # MissingValueImputation
    table_1["DIRECTORY_ORG_UNIT_TITLE"] = table_1["DIRECTORY_ORG_UNIT_TITLE"].fillna(table_1["DIRECTORY_ORG_UNIT_TITLE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="EMERITUS_STATUS", mode="mode")
    # MissingValueImputation
    table_1["EMERITUS_STATUS"] = table_1["EMERITUS_STATUS"].fillna(table_1["EMERITUS_STATUS"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="DIRECTORY_ORG_UNIT_TITLE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["DIRECTORY_ORG_UNIT_TITLE"] = table_1["DIRECTORY_ORG_UNIT_TITLE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="EMERITUS_STATUS", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["EMERITUS_STATUS"] = table_1["EMERITUS_STATUS"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['DIRECTORY_ORG_UNIT_TITLE', 'EMERITUS_STATUS'])
    # SelectCol
    _cols = [c for c in ['DIRECTORY_ORG_UNIT_TITLE', 'EMERITUS_STATUS'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_orgs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_9'])
prepared_table_3 = _prep_3(tables['table_5'])
prepared_hierarchy = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_people = prepared_table_4

# Start from prepared tables
orgs = prepared_orgs.copy()
hier = prepared_hierarchy.copy()
people = prepared_people.copy()

# Join orgs to hierarchy via DLC key
merged = orgs.merge(hier, left_on='DLC_KEY', right_on='dlc_key', how='left')

# Derive emeritus membership per organization by matching people.DIRECTORY_ORG_UNIT_TITLE to org ORGANIZATION_NAME
# Flag people as emeritus/non-emeritus
people_flags = people.dropna(subset=['DIRECTORY_ORG_UNIT_TITLE']).copy()
people_flags['is_emeritus'] = people_flags['EMERITUS_STATUS'].fillna('').str.strip().str.lower().isin(['emeritus','emerita','emeritus/emerita','emeritus status'])

# Map directory titles to organization names using case-insensitive equality
# Build normalization for join
merged['_org_name_norm'] = merged['ORGANIZATION_NAME'].astype(str).str.strip().str.lower()
people_flags['_dir_name_norm'] = people_flags['DIRECTORY_ORG_UNIT_TITLE'].astype(str).str.strip().str.lower()

# Count members per org by emeritus flag
member_counts = (
    people_flags
    .groupby('_dir_name_norm')['is_emeritus']
    .value_counts(dropna=False)
    .unstack(fill_value=0)
    .reset_index()
)
# Ensure both columns exist
if True not in member_counts.columns:
    member_counts[True] = 0
if False not in member_counts.columns:
    member_counts[False] = 0
member_counts = member_counts.rename(columns={True: 'emeritus_count', False: 'non_emeritus_count'})

merged = merged.merge(member_counts, left_on='_org_name_norm', right_on='_dir_name_norm', how='left')
merged['emeritus_count'] = merged['emeritus_count'].fillna(0).astype(int)
merged['non_emeritus_count'] = merged['non_emeritus_count'].fillna(0).astype(int)

# Exclude organizations '139' and '250' (compare to ORGANIZATION_ID as strings)
result = merged[~merged['ORGANIZATION_ID'].astype(str).isin(['139','250'])].copy()

# Compute employer count totals per hierarchy type
result['EMPLOYER_COUNT'] = result['emeritus_count'] + result['non_emeritus_count']

totals = (
    result.groupby('HIERARCHY_TYPE', dropna=False)['EMPLOYER_COUNT']
    .sum()
    .reset_index()
    .rename(columns={'EMPLOYER_COUNT':'EMPLOYER_COUNT_TOTAL'})
)

result = result.merge(totals, on='HIERARCHY_TYPE', how='left')

# Prepare final projection and sorting by hierarchy type
final_cols = [
    'ORGANIZATION',            # break group (short code)
    'ORGANIZATION_ID',
    'ORGANIZATION_NAME',       # name
    'ORGANIZATION_NAME',       # formatted name according to its level (no special formatting available; using name)
    'HIERARCHY_TYPE',
    'ORGANIZATION_NUMBER',
    'ORGANIZATION_LEVEL',
    'emeritus_count',
    'non_emeritus_count',
    'EMPLOYER_COUNT',
    'EMPLOYER_COUNT_TOTAL'
]
final = result.sort_values(['HIERARCHY_TYPE', 'ORGANIZATION_NAME'], kind='mergesort')[final_cols].copy()

# Rename for clarity
final = final.rename(columns={
    'ORGANIZATION': 'BREAK_GROUP',
    'ORGANIZATION_NAME': 'ORGANIZATION_NAME',
    'ORGANIZATION_NUMBER': 'ORGANIZATION_NUMBER',
    'ORGANIZATION_LEVEL': 'ORGANIZATION_LEVEL'
})

target = final

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
