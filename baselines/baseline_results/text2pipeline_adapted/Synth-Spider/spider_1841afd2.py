import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['client_id', 'agency_id', 'sic_code', 'detail_part1', 'detail_part2']}, 'table_indices': [0]}], [{'op': 'Concatenate', 'params': {'concatenate_columns': ['invoice_details_Starting', 'invoice_details_Working', 'invoice_details_Finish'], 'target_column': 'invoice_details_raw', 'func': 'def transform(row):\n    parts = []\n    for col in ["invoice_details_Starting", "invoice_details_Working", "invoice_details_Finish"]:\n        v = row.get(col)\n        parts.append("" if v is None else str(v))\n    return " ".join(parts)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'invoice_details_raw', 'func': 'def transform(s):\n    import re\n    txt = str(s)\n    # replace case-insensitive \'nan\' tokens surrounded by word boundaries with empty\n    txt = re.sub(r"(?i)\\bnan\\b", "", txt)\n    # collapse multiple whitespace to single space\n    txt = re.sub(r"\\s+", " ", txt)\n    return txt.strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['invoice_id', 'client_id', 'invoice_details_raw']}, 'table_indices': [0]}], [{'op': 'StandardizeDatetime', 'params': {'column_name': 'start_date_time', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'start_date_time', 'new_name': 'start_dt'}]}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'end_date_time', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'end_date_time', 'new_name': 'end_dt'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'billable_yn', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['meeting_id', 'client_id', 'meeting_outcome', 'meeting_type', 'billable_yn', 'start_dt', 'end_dt', 'purpose_of_meeting', 'other_details']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['client_id', 'agency_id', 'sic_code', 'detail_part1', 'detail_part2']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(row):\n    parts = []\n    for col in ["invoice_details_Starting", "invoice_details_Working", "invoice_details_Finish"]:\n        v = row.get(col)\n        parts.append("" if v is None else str(v))\n    return " ".join(parts)', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['invoice_details_raw'] = tmp_0[['invoice_details_Starting', 'invoice_details_Working', 'invoice_details_Finish']].apply(_concat_func_1, axis=1)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    txt = str(s)\n    # replace case-insensitive \'nan\' tokens surrounded by word boundaries with empty\n    txt = re.sub(r"(?i)\\bnan\\b", "", txt)\n    # collapse multiple whitespace to single space\n    txt = re.sub(r"\\s+", " ", txt)\n    return txt.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['invoice_details_raw'] = tmp_1['invoice_details_raw'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['invoice_id', 'client_id', 'invoice_details_raw']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['start_date_time'] = pd.to_datetime(tmp_0['start_date_time'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'start_date_time': 'start_dt'})
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['end_date_time'] = pd.to_datetime(tmp_2['end_date_time'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'end_date_time': 'end_dt'})
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['billable_yn'] = pd.to_numeric(tmp_4['billable_yn'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['meeting_id', 'client_id', 'meeting_outcome', 'meeting_type', 'billable_yn', 'start_dt', 'end_dt', 'purpose_of_meeting', 'other_details']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
clients = prepared_table_1.copy()
inv = prepared_table_2.copy()
mtg = prepared_table_3.copy()
# Identify clients with at least one invoice
inv_clients = inv[['client_id']].drop_duplicates()
# Identify clients with at least one meeting
mtg_clients = mtg[['client_id']].drop_duplicates()
# Union of clients who have invoice or meeting
active_clients = inv_clients.merge(mtg_clients, on='client_id', how='outer')
# Join back to client details
result = active_clients.merge(clients, on='client_id', how='left')
# For additional context, we can optionally aggregate minimal detail text per client from invoices/meetings
# Build a brief detail string: first non-empty invoice detail and first meeting type/outcome
first_inv = inv.assign(_inv_detail=inv['invoice_details_raw'].fillna('').astype(str).str.strip())
first_inv = first_inv.loc[first_inv['_inv_detail'] != ''].sort_values(['client_id', 'invoice_id']).groupby('client_id', as_index=False).agg({'_inv_detail':'first'})
first_mtg = mtg.sort_values(['client_id', 'meeting_id']).groupby('client_id', as_index=False).agg({'meeting_type':'first','meeting_outcome':'first'})
# Merge optional details
result = result.merge(first_inv, on='client_id', how='left').merge(first_mtg, on='client_id', how='left')
# Compose a details column from available parts without re-cleaning source tables
def _compose(row):
    parts = []
    if isinstance(row.get('_inv_detail'), str) and row['_inv_detail']:
        parts.append(f"invoice: {row['_inv_detail']}")
    mt = row.get('meeting_type')
    mo = row.get('meeting_outcome')
    mt = mt if isinstance(mt, str) else ''
    mo = mo if isinstance(mo, str) else ''
    if mt or mo:
        if mt and mo:
            parts.append(f"meeting: {mt} / {mo}")
        elif mt:
            parts.append(f"meeting: {mt}")
        else:
            parts.append(f"meeting: {mo}")
    return ' | '.join(parts)
result['details'] = result.apply(_compose, axis=1)
# Final projection: ids and details of clients who have attended a meeting or had an invoice
cols_to_show = ['client_id', 'agency_id', 'sic_code', 'detail_part1', 'detail_part2', 'details']
existing_cols = [c for c in cols_to_show if c in result.columns]
target = result[existing_cols].sort_values('client_id')

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
