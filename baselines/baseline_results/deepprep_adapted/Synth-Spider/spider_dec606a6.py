import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['client_id', 'agency_id', 'attribute'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['client_id', 'agency_id', 'attribute'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize spacing and case for attribute keys
    #     s = re.sub(r'\s+', '_', s.strip())
    #     return s.lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize spacing and case for attribute keys
        s = re.sub(r'\s+', '_', s.strip())
        return s.lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute"] = table_1["attribute"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="value", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["value"] = table_1["value"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="client_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['client_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['client_id']
    if _dtype == "datetime64":
        table_1['client_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['client_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="agency_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['agency_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['agency_id']
    if _dtype == "datetime64":
        table_1['agency_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['agency_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['agency_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['agency_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['client_id', 'agency_id', 'attribute'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['client_id', 'agency_id', 'attribute'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'agency_id', 'attribute', 'value'])
    # SelectCol
    _cols = [c for c in ['client_id', 'agency_id', 'attribute', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="invoice_details_Working", mode="mode")
    # MissingValueImputation
    table_1["invoice_details_Working"] = table_1["invoice_details_Working"].fillna(table_1["invoice_details_Working"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="invoice_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['invoice_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['invoice_id']
    if _dtype == "datetime64":
        table_1['invoice_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['invoice_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['invoice_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['invoice_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="client_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['client_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['client_id']
    if _dtype == "datetime64":
        table_1['client_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['client_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['invoice_id', 'client_id', 'invoice_details_Finish', 'invoice_details_Starting', 'invoice_details_Working'])
    # SelectCol
    _cols = [c for c in ['invoice_id', 'client_id', 'invoice_details_Finish', 'invoice_details_Starting', 'invoice_details_Working'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['agency_id', 'staff_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['agency_id', 'staff_id'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['agency_id', 'staff_id', 'staff_details'])
    # SelectCol
    _cols = [c for c in ['agency_id', 'staff_id', 'staff_details'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['agency_id', 'staff_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['agency_id', 'staff_id'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_invoices = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_agencies = prepared_table_3

# prepared tables are provided as dataframes: prepared_invoices, prepared_clients, prepared_agencies
# 1) Join invoices to client-agency metadata on client_id
ivc = prepared_invoices.merge(prepared_clients, on='client_id', how='left', suffixes=('', '_clientmeta'))

# 2) Join to agency details on agency_id
ivc_ag = ivc.merge(prepared_agencies, on='agency_id', how='left', suffixes=('', '_agency'))

# 3) Select columns to show invoice status codes/details plus client and agency identifiers/details
# Pivot client attribute/value pairs into columns for readability (client_details, sic_code, agency_details if present)
client_attrs = ivc_ag.pivot_table(index=['invoice_id','client_id','agency_id','invoice_details_Finish','invoice_details_Starting','invoice_details_Working','staff_id','staff_details'], 
                                  columns='attribute', values='value', aggfunc='first').reset_index()
client_attrs.columns = [c if not isinstance(c, tuple) else (c[1] if c[1] else c[0]) for c in client_attrs.columns]

# Build final view. If an explicit agency_details attribute exists in client metadata, keep it; otherwise we can expose staff_details as agency_details_proxy.
cols_base = ['invoice_id','client_id','agency_id','invoice_details_Finish','invoice_details_Starting','invoice_details_Working']
possible_client_detail_cols = [c for c in client_attrs.columns if c not in cols_base + ['staff_id','staff_details']]
final_cols = cols_base + possible_client_detail_cols + ['staff_details']
final = client_attrs[final_cols].sort_values(['invoice_id','client_id','agency_id'])

target = final

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
