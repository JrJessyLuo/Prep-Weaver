import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
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
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TransactionID', 'Date', 'Time', 'GasStationID'])
    # SelectCol
    _cols = [c for c in ['TransactionID', 'Date', 'Time', 'GasStationID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # Deduplicate(table_name="table_1", subset=['GasStationID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['GasStationID'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="CZE", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize common null-like tokens
    #     if s.lower() in {"nan", "none", "null", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize common null-like tokens
        if s.lower() in {"nan", "none", "null", ""}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["CZE"] = table_1["CZE"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['GasStationID', 'CZE'])
    # SelectCol
    _cols = [c for c in ['GasStationID', 'CZE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_stations = prepared_table_2

# Assume prepared_transactions and prepared_stations are provided per targets above
# 1) Integrate on GasStationID
joined = prepared_transactions.merge(prepared_stations, on='GasStationID', how='left')

# 2) Filter by date and time window 08:00:00-08:59:59 on 2012/08/26 and stations in CZE
# Normalize date format if needed; compare as strings assuming ISO 'YYYY-MM-DD'
mask_date = joined['Date'].astype(str) == '2012-08-26'
# Parse time to datetime.time for robust filtering
times = pd.to_datetime(joined['Time'].astype(str), errors='coerce').dt.time
start = pd.to_datetime('08:00:00').time()
end = pd.to_datetime('08:59:59').time()
mask_time = times >= start
mask_time &= times <= end
# Determine CZE stations: treat non-null/non-empty values that indicate presence in CZE
# If CZE column encodes category like 'Premium', 'Other', count those as CZE; exclude NaN/empty
cze_col = joined['CZE']
mask_cze = cze_col.notna() & (cze_col.astype(str).str.strip() != '')

filtered = joined[mask_date & mask_time & mask_cze]

# 3) Count transactions
answer = len(filtered)

result = pd.DataFrame({'count_in_CZE_2012_08_26_08_00_09_00': [answer]})

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
