import pandas as pd

# Load tables from provided dict
clients = tables['table_1'].copy()   # spider_1841afd2_input_0.pkl
invoices = tables['table_2'].copy()  # spider_1841afd2_input_1.pkl
meetings = tables['table_3'].copy()  # spider_1841afd2_input_2.pkl

# Reproduce the same logic as the reference code

# Unique client IDs from invoices and meetings
invoice_client_ids = invoices["client_id"].dropna().astype(int).unique()
meeting_client_ids = meetings["client_id"].dropna().astype(int).unique()

# Concatenate detail columns into a single 'details' field
clients = clients.copy()
clients["detail_part1"] = clients["detail_part1"].fillna("").astype(str).str.strip()
clients["detail_part2"] = clients["detail_part2"].fillna("").astype(str).str.strip()
clients["details"] = (clients["detail_part1"] + " " + clients["detail_part2"]).str.strip()
clients["details"] = clients["details"].replace({"": pd.NA})

# Union of client_ids that have invoices or meetings
clients_union_ids = sorted(list(set(invoice_client_ids).union(set(meeting_client_ids))))

# Final result: ids and details for clients in the union
final_df = clients.loc[clients["client_id"].isin(clients_union_ids), ["client_id", "details"]].reset_index(drop=True)

# Package in the required dict format
result = {"clients_with_meeting_or_invoice": final_df}