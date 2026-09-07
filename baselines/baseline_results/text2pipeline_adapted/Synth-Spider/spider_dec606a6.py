import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'agency_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'agency_id', 'attribute', 'value']}, 'table_indices': [0]}], [{'op': 'WideToLong', 'params': {'subnames': ['invoice_details'], 'i': ['invoice_id', 'client_id'], 'j': 'status_type', 'sep': '_', 'suffix': '\\w+'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'invoice_details', 'new_name': 'status_detail'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status_type', 'func': "def transform(s):\n    s = str(s)\n    return s.replace('invoice_details_', '')"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'invoice_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['invoice_id', 'client_id', 'status_type', 'status_detail']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['staff_id', 'agency_id', 'staff_details']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['client_id'] = pd.to_numeric(tmp_0['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['agency_id'] = pd.to_numeric(tmp_1['agency_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['client_id', 'agency_id', 'attribute', 'value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: WideToLong
    tmp_0 = pd.wide_to_long(df, stubnames=['invoice_details'], i=['invoice_id', 'client_id'], j='status_type', sep='_', suffix='\\w+').reset_index()
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'invoice_details': 'status_detail'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    return s.replace('invoice_details_', '')", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['status_type'] = tmp_2['status_type'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['invoice_id'] = pd.to_numeric(tmp_3['invoice_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['client_id'] = pd.to_numeric(tmp_4['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['invoice_id', 'client_id', 'status_type', 'status_detail']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['staff_id', 'agency_id', 'staff_details']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
inv_long = prepared_table_2.copy()
# prepared_table_2 is expected already long with columns: invoice_id, client_id, status_type, status_detail
# Prepare client and agency details from EAV table_1
clients = prepared_table_1.copy()
# Pivot client/agency attributes so we can expose client_details and agency-related attributes while retaining keys
pivot = clients.pivot_table(index=["client_id", "agency_id"], columns="attribute", values="value", aggfunc="first").reset_index()
# Merge invoices to client/agency pivot on client_id
integrated = inv_long.merge(pivot, on="client_id", how="left")
# Build status code and detail columns: status_type is the status code; status_detail is the detail
# Select columns: show invoice status code/detail + client id/details + agency id/details (if present in attributes)
# Try to include common detail attribute columns if present
cols = [c for c in integrated.columns]
client_detail_cols = [c for c in cols if c.lower() in ["client_details", "client_detail", "client_name", "name"]]
agency_detail_cols = [c for c in cols if c.lower() in ["agency_details", "agency_detail", "agency_name", "name_agency"]]
base_cols = ["invoice_id", "status_type", "status_detail", "client_id", "agency_id"]
project_cols = []
for c in base_cols:
    if c in integrated.columns:
        project_cols.append(c)
# Add best-effort client details columns
for c in client_detail_cols:
    if c not in project_cols:
        project_cols.append(c)
# Add best-effort agency details columns
for c in agency_detail_cols:
    if c not in project_cols:
        project_cols.append(c)
# If no explicit agency detail column exists, still keep agency_id from pivot/integration
target = integrated[project_cols].sort_values(["client_id", "invoice_id", "status_type"])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
