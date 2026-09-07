import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="GasStationID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['GasStationID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['GasStationID']
    if _dtype == "datetime64":
        table_1['GasStationID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['GasStationID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['GasStationID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['GasStationID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Time", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
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
    table_1["Time"] = table_1["Time"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TransactionID', 'Date', 'Time', 'GasStationID'])
    # SelectCol
    _cols = [c for c in ['TransactionID', 'Date', 'Time', 'GasStationID'] if c in table_1.columns]
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
    # MissingValueImputation(table_name="table_1", column_name="Value", mode="mode")
    # MissingValueImputation
    table_1["Value"] = table_1["Value"].fillna(table_1["Value"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['StationID', 'Value'])
    # SelectCol
    _cols = [c for c in ['StationID', 'Value'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_station_attributes = prepared_table_2

# Assumptions:
# - prepared_transactions['Date'] is datetime64 and 'Time' is a string HH:MM:SS.
# - prepared_station_attributes is a long key-value table where rows with ValueType 'Country' (or similar) exist.
#   Given the provided schema (columns: StationID, Value) without an attribute name column,
#   we attempt to locate a country by heuristic (e.g., known country names) or, if an attribute
#   name column exists but was omitted, adapt accordingly.


# 1) Filter transactions to the target date
trans = prepared_transactions.copy()
trans_date = pd.to_datetime('2012-08-25')
trans = trans[trans['Date'].dt.date == trans_date.date()].copy()

# 2) Build a sortable timestamp
# If Time may be missing, coerce errors
trans['timestamp'] = pd.to_datetime(trans['Date'].dt.date.astype(str) + ' ' + trans['Time'].astype(str), errors='coerce')

# 3) Keep the first paid customer by earliest timestamp
# Assuming all rows are paid transactions; if a paid-flag exists, filter it here.
trans = trans.sort_values(['timestamp', 'TransactionID'])
first_txn = trans.head(1)

# 4) Join to station attributes to get country. Since prepared_station_attributes lacks an attribute name,
#    we will try to detect country-like values. If your data has an attribute name column, replace this step
#    with a filter for attribute == 'Country'.
attrs = prepared_station_attributes.copy()

# Narrow attrs to only the station from first_txn to minimize false positives
station_id = None
country = None
if not first_txn.empty:
    station_id = str(first_txn.iloc[0]['GasStationID'])
    cand = attrs[attrs['StationID'].astype(str) == station_id]

    # Heuristic: match common country name patterns (letters/spaces, reasonably short)
    # If multiple candidates, take the first occurrence
    if not cand.empty:
        # If there is a hidden/implicit attribute name column in real data, replace this block with a direct filter.
        country_like = cand['Value'].astype(str)
        # Simple heuristic list; expand as needed
        possible = country_like[country_like.str.match(r'^[A-Za-z .-]{2,40}$', na=False)]
        if not possible.empty:
            country = possible.iloc[0]

# 5) Prepare final answer
if first_txn.empty:
    result = pd.DataFrame({'country': [None]})
else:
    result = pd.DataFrame({'country': [country]})

answer = result

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
