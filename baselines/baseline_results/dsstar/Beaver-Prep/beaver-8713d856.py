import pandas as pd

# The input tables are provided in the dict `tables`:
# tables['table_1'] -> MOIRA_LIST_DETAIL.pkl
# tables['table_2'] -> MOIRA_LIST_OWNER.pkl
# tables['table_3'] -> MOIRA_LIST.pkl
# ... (others not needed for this task)

# Parameters
key_to_find = "LIST69.377-keeper-xenon"

# Source DataFrames from `tables`
moira_list_detail = tables['table_1']
moira_list_owner = tables['table_2']

# Owner lookup (same logic as reference)
owner_series = moira_list_owner.loc[
    moira_list_owner["MOIRA_LIST_OWNER_KEY"] == key_to_find, "OWNER"
]
owner_list = owner_series.tolist()
owner_value = owner_list[0] if len(owner_list) > 0 else None

# Detail filtering and aggregations (same logic as reference)
filtered_detail = moira_list_detail.loc[
    moira_list_detail["MOIRA_LIST_OWNER_KEY"] == key_to_find
]

num_distinct_lists = filtered_detail["MOIRA_LIST_KEY"].nunique(dropna=True)
total_member_rows = len(filtered_detail)

# Build final answer DataFrame
answer_df = pd.DataFrame([{
    "MOIRA_LIST_OWNER_KEY": key_to_find,
    "owner": owner_value,
    "total_mailing_lists": int(num_distinct_lists),
    "total_members_across_lists": int(total_member_rows),
}])

# Assign to `result` as required
result = {"mailing_list_summary": answer_df}