import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="IS_MOIRA_MAILING_LIST", func="""
    # def is_valid_email(val):
    #     if val is None:
    #         return False
    #     v = str(val).strip().upper()
    #     return v in ["Y", "N"]
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_email(val):
        if val is None:
            return False
        v = str(val).strip().upper()
        return v in ["Y", "N"]
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_email(val))
        except Exception:
            return False
    table_1 = table_1[table_1['IS_MOIRA_MAILING_LIST'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     # remove surrounding quotes if present
    #     if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
    #         v = v[1:-1].strip()
    #     # keys are typically stored uppercase; keep stable by uppercasing
    #     return v.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        # remove surrounding quotes if present
        if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
            v = v[1:-1].strip()
        # keys are typically stored uppercase; keep stable by uppercasing
        return v.upper()
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
    #         return None
    #     v = str(s).strip()
    #     if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
    #         v = v[1:-1].strip()
    #     # names are typically lowercase
    #     return v.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
            v = v[1:-1].strip()
        # names are typically lowercase
        return v.lower()
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
    #         return None
    #     v = str(s).strip()
    #     if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
    #         v = v[1:-1].strip()
    #     v = v.upper()
    #     return "Y" if v == "Y" else ("N" if v == "N" else v)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
            v = v[1:-1].strip()
        v = v.upper()
        return "Y" if v == "Y" else ("N" if v == "N" else v)
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
    # StandardizeString(table_name="table_1", column_name="IS_MOIRA_GROUP", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
    #         v = v[1:-1].strip()
    #     v = v.upper()
    #     return "Y" if v == "Y" else ("N" if v == "N" else v)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
            v = v[1:-1].strip()
        v = v.upper()
        return "Y" if v == "Y" else ("N" if v == "N" else v)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_MOIRA_GROUP"] = table_1["IS_MOIRA_GROUP"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IS_NFS_GROUP", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
    #         v = v[1:-1].strip()
    #     v = v.upper()
    #     return "Y" if v == "Y" else ("N" if v == "N" else v)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        if len(v) >= 2 and ((v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'")):
            v = v[1:-1].strip()
        v = v.upper()
        return "Y" if v == "Y" else ("N" if v == "N" else v)
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IS_NFS_GROUP"] = table_1["IS_NFS_GROUP"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_MOIRA_MAILING_LIST', 'IS_MOIRA_GROUP', 'IS_NFS_GROUP'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="MOIRA_LIST_OWNER_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["MOIRA_LIST_OWNER_KEY"] = table_1["MOIRA_LIST_OWNER_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OWNER", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OWNER"] = table_1["OWNER"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OWNER_TYPE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return s.strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return s.strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OWNER_TYPE"] = table_1["OWNER_TYPE"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['MOIRA_LIST_OWNER_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_OWNER_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_members = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_owners = prepared_table_3

# Assume prepared_lists, prepared_members, prepared_owners already materialized per targets
# Join members to owners to resolve owner name
mem_with_owner = prepared_members.merge(
    prepared_owners[["MOIRA_LIST_OWNER_KEY", "OWNER", "OWNER_TYPE"]],
    on="MOIRA_LIST_OWNER_KEY",
    how="left"
)
# Join list attributes
full = mem_with_owner.merge(
    prepared_lists[["MOIRA_LIST_KEY", "MOIRA_LIST_NAME", "IS_MOIRA_MAILING_LIST", "IS_MOIRA_GROUP", "IS_NFS_GROUP"]],
    on="MOIRA_LIST_KEY",
    how="left"
)

# Normalize name prefix filter (starts with 'A', case-insensitive)
mask_a = full["MOIRA_LIST_NAME"].astype(str).str.strip().str.lower().str.startswith("a")
full_a = full[mask_a]

# Count distinct people per list (distinct member identifiers)
agg = (
    full_a.assign(member_norm=full_a["moira_list_member"].astype(str).str.strip())
        .groupby(["MOIRA_LIST_KEY", "MOIRA_LIST_NAME", "IS_MOIRA_MAILING_LIST", "IS_MOIRA_GROUP", "IS_NFS_GROUP"], dropna=False)
        .agg(num_people=("member_norm", lambda s: s.dropna().nunique()))
        .reset_index()
)

# Keep owner per list: choose the most common resolved owner among rows for stability
owners = (
    full_a.groupby(["MOIRA_LIST_KEY"]) 
         .apply(lambda g: g["OWNER"].dropna().mode().iloc[0] if not g["OWNER"].dropna().empty else None)
         .reset_index(name="OWNER")
)

out = agg.merge(owners, on="MOIRA_LIST_KEY", how="left")

# Filter lists with more than 1000 people
out = out[out["num_people"] > 1000]

# Select and rename columns per question
result = out[[
    "MOIRA_LIST_NAME",
    "IS_MOIRA_MAILING_LIST",
    "IS_MOIRA_GROUP",
    "IS_NFS_GROUP",
    "OWNER",
    "num_people"
]].rename(columns={
    "MOIRA_LIST_NAME": "list_name",
    "IS_MOIRA_MAILING_LIST": "is_mailing_list",
    "IS_MOIRA_GROUP": "is_moira_group",
    "IS_NFS_GROUP": "is_nfs_group",
    "OWNER": "owner",
    "num_people": "people_count"
}).drop_duplicates()

# Sort by list name for readability (not required)
result = result.sort_values("list_name", kind="stable")

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
