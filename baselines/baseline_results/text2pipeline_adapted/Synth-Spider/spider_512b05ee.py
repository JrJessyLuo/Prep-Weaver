import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'invoice_number', 'func': 'def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'evt', 'target_columns': ['evt_type', 'evt_ts'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split(':', 1)\n    if len(parts) == 2:\n        return [parts[0], parts[1].strip()]\n    return [s, None]"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'evt_ts', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'evt_ts', 'new_name': 'event_timestamp'}, {'old_name': 'evt_type', 'new_name': 'event_type'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['invoice_number', 'event_type', 'event_timestamp']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'shipment_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'order_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'invoice_number', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'shipment_tracking_number', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['shipment_date_part', 'shipment_time_part'], 'target_column': 'shipment_datetime', 'func': 'def transform(row):\n    date_part = row[\'shipment_date_part\']\n    time_part = row[\'shipment_time_part\']\n    if pd.isna(date_part) or pd.isna(time_part):\n      return pd.NaT\n    s = f"{date_part} {time_part}"\n    try:\n      return pd.to_datetime(s, errors=\'coerce\', format=\'%Y-%m-%d %H:%M:%S\')\n    except Exception:\n      return pd.to_datetime(s, errors=\'coerce\')'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['shipment_id', 'order_id', 'invoice_number', 'shipment_tracking_number', 'shipment_date_part', 'shipment_time_part', 'shipment_datetime']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['invoice_number'] = tmp_0['invoice_number'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split(':', 1)\n    if len(parts) == 2:\n        return [parts[0], parts[1].strip()]\n    return [s, None]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['evt'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['evt_type'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['evt_ts'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['evt_ts'] = pd.to_datetime(tmp_2['evt_ts'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'evt_ts': 'event_timestamp', 'evt_type': 'event_type'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['invoice_number', 'event_type', 'event_timestamp']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['shipment_id'] = tmp_0['shipment_id'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['order_id'] = tmp_1['order_id'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['invoice_number'] = tmp_2['invoice_number'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['shipment_tracking_number'] = tmp_3['shipment_tracking_number'].astype(str)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(row):\n    date_part = row[\'shipment_date_part\']\n    time_part = row[\'shipment_time_part\']\n    if pd.isna(date_part) or pd.isna(time_part):\n      return pd.NaT\n    s = f"{date_part} {time_part}"\n    try:\n      return pd.to_datetime(s, errors=\'coerce\', format=\'%Y-%m-%d %H:%M:%S\')\n    except Exception:\n      return pd.to_datetime(s, errors=\'coerce\')', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_4['shipment_datetime'] = tmp_4[['shipment_date_part', 'shipment_time_part']].apply(_concat_func_1, axis=1)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['shipment_id', 'order_id', 'invoice_number', 'shipment_tracking_number', 'shipment_date_part', 'shipment_time_part', 'shipment_datetime']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
inv_events = prepared_table_1
ship = prepared_table_2
# Derive invoice-level issued date from events
issued = inv_events[inv_events['event_type'].str.lower()=='issued'].copy()
issued = issued.rename(columns={'event_timestamp':'invoice_date'})[['invoice_number','invoice_date']]
# If no issued event for an invoice, fallback to the earliest event timestamp
fallback = (inv_events.sort_values('event_timestamp')
            .groupby('invoice_number', as_index=False)
            .first()
            .rename(columns={'event_timestamp':'invoice_date'})[['invoice_number','invoice_date']])
# Prefer issued date where available
inv_dates = fallback.merge(issued, on='invoice_number', how='left', suffixes=('_fb','_iss'))
inv_dates['invoice_date'] = inv_dates['invoice_date_iss'].combine_first(inv_dates['invoice_date_fb'])
inv_dates = inv_dates[['invoice_number','invoice_date']]
# Count shipments per invoice
ship_counts = ship.groupby('invoice_number', as_index=False).agg(shipment_count=('shipment_id','count'))
# Join counts to invoice dates
inv_ship = inv_dates.merge(ship_counts, on='invoice_number', how='inner')
# Filter to at least 2 shipments
result = inv_ship[inv_ship['shipment_count']>=2]
# Final projection: invoice id and date
target = result[['invoice_number','invoice_date']].sort_values(['invoice_date','invoice_number'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
