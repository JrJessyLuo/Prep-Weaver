import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['MOIRA_LIST_KEY'] = df['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = df[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_MOIRA_MAILING_LIST','IS_MOIRA_GROUP','IS_NFS_GROUP']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member']].copy()
    target['moira_list_member'] = target['moira_list_member'].astype(str).str.strip()
    target = target[['MOIRA_LIST_KEY','MOIRA_LIST_OWNER_KEY','moira_list_member']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['MOIRA_LIST_OWNER_KEY','OWNER','OWNER_TYPE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
