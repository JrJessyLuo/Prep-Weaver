import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['invoice_id', 'wc', 'ks', 'gz']}, 'table_indices': [0]}], [{'op': 'Concatenate', 'params': {'concatenate_columns': ['card_type_prefix', 'card_type_suffix'], 'target_column': 'card_type', 'func': "def transform(row):\n    a = str(row.get('card_type_prefix', '') if row.get('card_type_prefix', '') is not None else '')\n    b = str(row.get('card_type_suffix', '') if row.get('card_type_suffix', '') is not None else '')\n    return (a + ' ' + b).strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'payment_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'invoice_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['payment_id', 'invoice_id', 'card_type']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['invoice_id', 'wc', 'ks', 'gz']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    a = str(row.get('card_type_prefix', '') if row.get('card_type_prefix', '') is not None else '')\n    b = str(row.get('card_type_suffix', '') if row.get('card_type_suffix', '') is not None else '')\n    return (a + ' ' + b).strip()", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['card_type'] = tmp_0[['card_type_prefix', 'card_type_suffix']].apply(_concat_func_1, axis=1)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['payment_id'] = pd.to_numeric(tmp_1['payment_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['invoice_id'] = pd.to_numeric(tmp_2['invoice_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['payment_id', 'invoice_id', 'card_type']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
inv = prepared_table_1.copy()
pay = prepared_table_2.copy()
# Identify a best-effort invoice status column from wc/ks/gz: choose the first non-null/non-empty across these columns
for col in ['wc','ks','gz']:
    if col not in inv.columns:
        inv[col] = None
inv['status'] = inv[['wc','ks','gz']].apply(lambda r: next((str(v).strip() for v in r if v is not None and str(v).strip().lower() != 'nan' and str(v).strip() != ''), None), axis=1)
# Left join invoices to payments to find invoices without a payment
merged = inv.merge(pay[['invoice_id','payment_id']], on='invoice_id', how='left')
no_payment = merged[merged['payment_id'].isna()].copy()
# Final projection: invoice ids and statuses
target = no_payment[['invoice_id','status']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
