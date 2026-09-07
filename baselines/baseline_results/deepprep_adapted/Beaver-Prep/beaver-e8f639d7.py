import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['MOIRA_LIST_NAME'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['MOIRA_LIST_NAME'], ascending=[True])

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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN', 'IS_MOIRA_MAILING_LIST', 'IS_ACTIVE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN', 'IS_MOIRA_MAILING_LIST', 'IS_ACTIVE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN', 'IS_MOIRA_MAILING_LIST', 'IS_ACTIVE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC', 'IS_HIDDEN', 'IS_MOIRA_MAILING_LIST', 'IS_ACTIVE'], keep='last').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # normalize whitespace and casing for a stable member identifier
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # normalize whitespace and casing for a stable member identifier
        return str(s).strip().upper()
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
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # DropColumn(table_name="table_1", drop_columns=['WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_OWNER_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_OWNER_KEY"] = table_1["MOIRA_LIST_OWNER_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OWNER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OWNER"] = table_1["OWNER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OWNER_TYPE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OWNER_TYPE"] = table_1["OWNER_TYPE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_owners = prepared_table_3

# Start from prepared tables
lists = prepared_lists.copy()
memberships = prepared_memberships.copy()
owners = prepared_owners.copy()

# Filter to active Moira mailing lists
lists_f = lists[(lists['IS_MOIRA_MAILING_LIST'] == 'Y') & (lists['IS_ACTIVE'] == 'Y')]

# Join memberships to lists to scope members to valid lists
mem_lists = memberships.merge(lists_f, on='MOIRA_LIST_KEY', how='inner')

# Compute member counts per list (count distinct member ids to be robust)
member_counts = (mem_lists.dropna(subset=['moira_list_member'])
                          .groupby('MOIRA_LIST_KEY', as_index=False)
                          .agg(NUM_MEMBERS=('moira_list_member', 'nunique')))

# Join counts and list attributes back
list_with_counts = lists_f.merge(member_counts, on='MOIRA_LIST_KEY', how='left')
list_with_counts['NUM_MEMBERS'] = list_with_counts['NUM_MEMBERS'].fillna(0).astype(int)

# Find global min and max member counts
min_count = list_with_counts['NUM_MEMBERS'].min()
max_count = list_with_counts['NUM_MEMBERS'].max()

extreme_lists = list_with_counts[list_with_counts['NUM_MEMBERS'].isin([min_count, max_count])]

# Attach owners (multiple owners -> multiple rows)
extreme_with_owner = extreme_lists.merge(memberships[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY']].drop_duplicates(),
                                         on='MOIRA_LIST_KEY', how='left')\
                                  .merge(owners, on='MOIRA_LIST_OWNER_KEY', how='left')

# Prepare final output columns
result = extreme_with_owner[['MOIRA_LIST_NAME','OWNER','OWNER_TYPE','IS_PUBLIC','IS_HIDDEN','NUM_MEMBERS']].rename(columns={
    'MOIRA_LIST_NAME':'list_name',
    'OWNER':'owner',
    'OWNER_TYPE':'owner_type',
    'IS_PUBLIC':'is_public',
    'IS_HIDDEN':'is_hidden',
    'NUM_MEMBERS':'num_members'
}).sort_values(['num_members','list_name','owner'], ascending=[True, True, True])

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
