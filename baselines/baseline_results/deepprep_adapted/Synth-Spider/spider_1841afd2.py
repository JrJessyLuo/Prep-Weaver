import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="detail_part2", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['detail_part2'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['detail_part2']
    if _dtype == "datetime64":
        table_1['detail_part2'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['detail_part2'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['detail_part2'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['detail_part2'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="sic_code", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding quotes if present
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
    table_1["sic_code"] = table_1["sic_code"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="detail_part1", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
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
    table_1["detail_part1"] = table_1["detail_part1"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="detail_part2", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # preserve empty string as-is (do not impute)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # preserve empty string as-is (do not impute)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["detail_part2"] = table_1["detail_part2"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'detail_part1', 'detail_part2', 'sic_code', 'agency_id'])
    # SelectCol
    _cols = [c for c in ['client_id', 'detail_part1', 'detail_part2', 'sic_code', 'agency_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['client_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['client_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
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
    # SelectCol(table_name="table_1", columns=['invoice_id', 'client_id', 'invoice_details_Finish', 'invoice_details_Starting', 'invoice_details_Working'])
    # SelectCol
    _cols = [c for c in ['invoice_id', 'client_id', 'invoice_details_Finish', 'invoice_details_Starting', 'invoice_details_Working'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="invoice_details_Finish", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in {"nan", "null", "none", ""}):
    #         return None
    #     if isinstance(s, str):
    #         s2 = s.strip()
    #         if (s2.startswith('"') and s2.endswith('"')) or (s2.startswith("'") and s2.endswith("'")):
    #             s2 = s2[1:-1].strip()
    #         return s2
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in {"nan", "null", "none", ""}):
            return None
        if isinstance(s, str):
            s2 = s.strip()
            if (s2.startswith('"') and s2.endswith('"')) or (s2.startswith("'") and s2.endswith("'")):
                s2 = s2[1:-1].strip()
            return s2
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["invoice_details_Finish"] = table_1["invoice_details_Finish"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="invoice_details_Starting", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in {"nan", "null", "none", ""}):
    #         return None
    #     if isinstance(s, str):
    #         s2 = s.strip()
    #         if (s2.startswith('"') and s2.endswith('"')) or (s2.startswith("'") and s2.endswith("'")):
    #             s2 = s2[1:-1].strip()
    #         return s2
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in {"nan", "null", "none", ""}):
            return None
        if isinstance(s, str):
            s2 = s.strip()
            if (s2.startswith('"') and s2.endswith('"')) or (s2.startswith("'") and s2.endswith("'")):
                s2 = s2[1:-1].strip()
            return s2
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["invoice_details_Starting"] = table_1["invoice_details_Starting"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="invoice_details_Working", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in {"nan", "null", "none", ""}):
    #         return None
    #     if isinstance(s, str):
    #         s2 = s.strip()
    #         if (s2.startswith('"') and s2.endswith('"')) or (s2.startswith("'") and s2.endswith("'")):
    #             s2 = s2[1:-1].strip()
    #         return s2
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or (isinstance(s, str) and s.strip().lower() in {"nan", "null", "none", ""}):
            return None
        if isinstance(s, str):
            s2 = s.strip()
            if (s2.startswith('"') and s2.endswith('"')) or (s2.startswith("'") and s2.endswith("'")):
                s2 = s2[1:-1].strip()
            return s2
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["invoice_details_Working"] = table_1["invoice_details_Working"].apply(_std_apply)

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
    # DropColumn(table_name="table_1", drop_columns=['billable_yn', 'other_details'])
    # DropColumn
    table_1 = table_1.drop(columns=['billable_yn', 'other_details'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="meeting_outcome", func="""
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
    table_1["meeting_outcome"] = table_1["meeting_outcome"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="meeting_type", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
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
    table_1["meeting_type"] = table_1["meeting_type"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="purpose_of_meeting", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
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
    table_1["purpose_of_meeting"] = table_1["purpose_of_meeting"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="start_date_time", date_format="%Y-%m-%d %H:%M:%S")
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
    table_1['start_date_time'] = table_1['start_date_time'].apply(_sd_parse)
    if '%Y-%m-%d %H:%M:%S':
        table_1['start_date_time'] = table_1['start_date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="end_date_time", date_format="%Y-%m-%d %H:%M:%S")
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
    table_1['end_date_time'] = table_1['end_date_time'].apply(_sd_parse)
    if '%Y-%m-%d %H:%M:%S':
        table_1['end_date_time'] = table_1['end_date_time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="meeting_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['meeting_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['meeting_id']
    if _dtype == "datetime64":
        table_1['meeting_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['meeting_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['meeting_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['meeting_id'] = _series.astype(str)

    # ---------------- Step 8 ----------------
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

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['meeting_id', 'client_id', 'meeting_outcome', 'meeting_type', 'start_date_time', 'end_date_time', 'purpose_of_meeting'])
    # SelectCol
    _cols = [c for c in ['meeting_id', 'client_id', 'meeting_outcome', 'meeting_type', 'start_date_time', 'end_date_time', 'purpose_of_meeting'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_invoices = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_meetings = prepared_table_3

clients = prepared_clients
inv = prepared_invoices
mtg = prepared_meetings
# Determine clients who have either an invoice or a meeting
clients_with_activity = clients.merge(inv[['client_id','invoice_id']], on='client_id', how='left')\
    .merge(mtg[['client_id','meeting_id']], on='client_id', how='left')
mask = clients_with_activity['invoice_id'].notna() | clients_with_activity['meeting_id'].notna()
result_clients = clients_with_activity.loc[mask]
# Build a details field from available client details (non-aggregating)
result = result_clients.assign(details=(result_clients['detail_part1'].fillna('') + ' ' + result_clients['detail_part2'].fillna('')).str.strip())
# Return ids and details of clients
answer = result[['client_id','details']].drop_duplicates()

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
