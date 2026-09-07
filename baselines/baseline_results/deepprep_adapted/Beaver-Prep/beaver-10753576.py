import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_OWNER_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
    # StandardizeString(table_name="table_1", column_name="IS_PUBLIC", func="""
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
    table_1["IS_PUBLIC"] = table_1["IS_PUBLIC"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
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
    table_1["IS_MOIRA_MAILING_LIST"] = table_1["IS_MOIRA_MAILING_LIST"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_HIDDEN", func="""
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
    table_1["IS_HIDDEN"] = table_1["IS_HIDDEN"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # trim leading/trailing whitespace only; preserve internal characters
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # trim leading/trailing whitespace only; preserve internal characters
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_KEY"] = table_1["MOIRA_LIST_KEY"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_PUBLIC', 'IS_HIDDEN'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_PUBLIC', 'IS_HIDDEN'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
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
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_list_owners = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_lists = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_memberships = prepared_table_3

# Assume prepared_* DataFrames already exist as per target schemas
# Normalize keys (e.g., strip spaces) for robust joins
prepared_lists = prepared_lists.assign(MOIRA_LIST_KEY=prepared_lists['MOIRA_LIST_KEY'].astype(str).str.strip())
prepared_memberships = prepared_memberships.assign(MOIRA_LIST_KEY=prepared_memberships['MOIRA_LIST_KEY'].astype(str).str.strip())

# Join memberships to owners
m_with_owner = prepared_memberships.merge(
    prepared_list_owners, how='left', on='MOIRA_LIST_OWNER_KEY'
)

# Join list visibility
m_full = m_with_owner.merge(
    prepared_lists[['MOIRA_LIST_KEY','IS_MOIRA_MAILING_LIST','IS_PUBLIC','IS_HIDDEN']],
    how='left', on='MOIRA_LIST_KEY'
)

# Keep only mailing lists
m_full = m_full[m_full['IS_MOIRA_MAILING_LIST'] == 'Y'].copy()

# Derive member visibility label per list
m_full['member_visibility'] = pd.Series(
    ['Public Members' if x == 'Y' else 'Hidden Members' for x in m_full['IS_PUBLIC']]
)

# Count members per list and visibility
per_list = (
    m_full.groupby(['MOIRA_LIST_KEY','OWNER','OWNER_TYPE','member_visibility'], dropna=False)['moira_list_member']
    .nunique()
    .reset_index(name='member_count')
)

# Build grand totals per (owner, owner type) across all their lists/members
grand_totals = (
    m_full.groupby(['OWNER','OWNER_TYPE'], dropna=False)['moira_list_member']
    .nunique()
    .reset_index(name='member_count')
)
grand_totals['MOIRA_LIST_KEY'] = pd.NA
grand_totals['member_visibility'] = pd.NA

# Align columns and concatenate
per_list_out = per_list[['MOIRA_LIST_KEY','OWNER','OWNER_TYPE','member_visibility','member_count']]
grand_out = grand_totals[['MOIRA_LIST_KEY','OWNER','OWNER_TYPE','member_visibility','member_count']]

result = pd.concat([per_list_out, grand_out], ignore_index=True)

# Final columns per question
target = result.rename(columns={
    'MOIRA_LIST_KEY': 'mailing_list',
    'OWNER': 'owner',
    'OWNER_TYPE': 'owner_type',
    'member_visibility': 'member_visibility',
    'member_count': 'members'
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
