import pandas as pd

# Source tables from provided `tables` dict
df_agencies = tables['table_1']
df_client_agency = tables['table_2']

# Merge client-agency mapping with agencies on agency_id (same logic as reference)
df_linked = df_client_agency.merge(df_agencies, on="agency_id", how="left")

# Filter clients whose sic_client_combined has detail 'Mac' after the pipe
# Assuming pattern "<something>|<detail>", we split by '|' and compare the second part to 'Mac'
detail_split = df_linked['sic_client_combined'].str.split('|', n=1, expand=True)
df_linked = df_linked.assign(_detail=detail_split[1])

answer_df = df_linked.loc[df_linked['_detail'] == 'Mac', ['agency_details']].drop_duplicates().reset_index(drop=True)

# Package final result
result = {
    "agency_details_for_client_with_detail_Mac": answer_df
}