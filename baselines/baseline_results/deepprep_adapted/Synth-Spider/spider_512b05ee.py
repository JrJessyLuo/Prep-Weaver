import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="evt", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["evt"] = table_1["evt"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="evt", target_columns=['event_type', 'event_datetime'], func="""
    # import re
    # def split(val):
    #     if val is None:
    #         return {"event_type": None, "event_datetime": None}
    #     s = str(val).strip()
    #     # Split on the first colon only
    #     if ':' in s:
    #         etype, dt = s.split(':', 1)
    #         return {"event_type": etype.strip(), "event_datetime": dt.strip()}
    #     # Fallback if unexpected format
    #     return {"event_type": None, "event_datetime": s}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"event_type": None, "event_datetime": None}
        s = str(val).strip()
        # Split on the first colon only
        if ':' in s:
            etype, dt = s.split(':', 1)
            return {"event_type": etype.strip(), "event_datetime": dt.strip()}
        # Fallback if unexpected format
        return {"event_type": None, "event_datetime": s}
    for _c in ['event_type', 'event_datetime']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['evt']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['event_type', 'event_datetime']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['evt'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="event_datetime", date_format="%Y-%m-%d %H:%M:%S")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['event_datetime'] = table_1['event_datetime'].apply(_sd_parse)
    if '%Y-%m-%d %H:%M:%S':
        table_1['event_datetime'] = table_1['event_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['invoice_number', 'event_type', 'event_datetime'])
    # SelectCol
    _cols = [c for c in ['invoice_number', 'event_type', 'event_datetime'] if c in table_1.columns]
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
    # Concatenate(table_name="table_1", concatenate_columns=['shipment_date_part', 'shipment_time_part'], target_column="shipment_datetime", func="""
    # def concat(row):
    #     date_part = '' if row['shipment_date_part'] is None else str(row['shipment_date_part']).strip().strip('"')
    #     time_part = '' if row['shipment_time_part'] is None else str(row['shipment_time_part']).strip().strip('"')
    #     return f"{date_part} {time_part}".strip()
    #  """)
    # Concatenate
    def concat(row):
        date_part = '' if row['shipment_date_part'] is None else str(row['shipment_date_part']).strip().strip('"')
        time_part = '' if row['shipment_time_part'] is None else str(row['shipment_time_part']).strip().strip('"')
        return f"{date_part} {time_part}".strip()
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["shipment_datetime"] = table_1[['shipment_date_part', 'shipment_time_part']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['shipment_date_part', 'shipment_time_part'])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="shipment_datetime", date_format="%Y-%m-%d %H:%M:%S")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['shipment_datetime'] = table_1['shipment_datetime'].apply(_sd_parse)
    if '%Y-%m-%d %H:%M:%S':
        table_1['shipment_datetime'] = table_1['shipment_datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['invoice_number', 'shipment_id', 'shipment_datetime'])
    # SelectCol
    _cols = [c for c in ['invoice_number', 'shipment_id', 'shipment_datetime'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
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
prepared_invoices = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_shipments = prepared_table_2

# prepared_invoices expected columns: invoice_number (str), event_type (str), event_datetime (datetime)
# prepared_shipments expected columns: invoice_number (str), shipment_id (int/str), shipment_datetime (datetime)

# Keep only the invoice date from the invoices table. Prefer the 'Issued' event as the invoice date; if absent, fall back to earliest event.
inv = prepared_invoices.copy()
# If event_datetime not yet datetime, parse it
if not pd.api.types.is_datetime64_any_dtype(inv['event_datetime']):
    inv['event_datetime'] = pd.to_datetime(inv['event_datetime'], errors='coerce')

# Choose issued event when available per invoice
issued = inv[inv['event_type'].str.lower() == 'issued']
issued = issued.sort_values(['invoice_number', 'event_datetime']).drop_duplicates('invoice_number', keep='first')

# For invoices without 'Issued', take earliest event
earliest = inv.sort_values(['invoice_number', 'event_datetime']).drop_duplicates('invoice_number', keep='first')

# Combine preference
inv_dates = pd.concat([issued, earliest[~earliest['invoice_number'].isin(issued['invoice_number'])]])
inv_dates = inv_dates[['invoice_number', 'event_datetime']].rename(columns={'event_datetime': 'invoice_date'})

# Count shipments per invoice
sh = prepared_shipments.copy()
ship_counts = sh.groupby('invoice_number', as_index=False)['shipment_id'].nunique().rename(columns={'shipment_id': 'shipment_count'})

# Join and filter invoices with at least 2 shipments
merged = inv_dates.merge(ship_counts, on='invoice_number', how='inner')
result = merged[merged['shipment_count'] >= 2][['invoice_number', 'invoice_date']].sort_values(['invoice_date', 'invoice_number'])

# Final output: dates and ids (invoice_number)
answer = result.rename(columns={'invoice_number': 'invoice_id', 'invoice_date': 'date'})

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
