import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Date", mode="mode")
    # MissingValueImputation
    table_1["Date"] = table_1["Date"].fillna(table_1["Date"].mode().iloc[0])

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
    # StandardizeDatetime(table_name="table_1", column_name="Time", date_format="%H:%M:%S")
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
    table_1['Time'] = table_1['Time'].apply(_sd_parse)
    if '%H:%M:%S':
        table_1['Time'] = table_1['Time'].dt.strftime('%H:%M:%S')

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # morning hours interpreted as 00:00:00 to 11:59:59
    #     return str(row['Date']) == '2012-08-26' and str(row['Time']) < '12:00:00'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # morning hours interpreted as 00:00:00 to 11:59:59
        return str(row['Date']) == '2012-08-26' and str(row['Time']) < '12:00:00'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Amount', 'Price'])
    # SelectCol
    _cols = [c for c in ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Amount', 'Price'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
    # Transpose(table_name="table_1")
    # Transpose
    if table_1.empty or len(table_1.columns) == 0:
        table_1 = table_1.transpose()
    else:
        _t = table_1.transpose()
        _newcols = _t.iloc[0].tolist()
        _t = _t.iloc[1:]
        _first = table_1.columns[0]
        _t.insert(0, _first, _t.index)
        _t.columns = [_first] + _newcols
        table_1 = _t.reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['Currency']).strip() == 'CZK'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['Currency']).strip() == 'CZK'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['CustomerID_Segment'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['CustomerID_Segment'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="target_table", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     # Collect unique, non-null segments in stable order
    #     vals = [v for v in table_1['CustomerID_Segment'].tolist() if pd.notna(v) and str(v).strip() != '']
    #     # Represent as an array-like string
    #     czk_cols = '[' + ', '.join([repr(str(v)) for v in vals]) + ']'
    #     return pd.DataFrame([{
    #         'Currency': 'CustomerID_Segment',
    #         'CZK_cols': czk_cols
    #     }])
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        # Collect unique, non-null segments in stable order
        vals = [v for v in table_1['CustomerID_Segment'].tolist() if pd.notna(v) and str(v).strip() != '']
        # Represent as an array-like string
        czk_cols = '[' + ', '.join([repr(str(v)) for v in vals]) + ']'
        return pd.DataFrame([{
            'Currency': 'CustomerID_Segment',
            'CZK_cols': czk_cols
        }])
    target_table = process_tables(table_1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['target_table'])
    # Terminate
    result = {'target_table': target_table}
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
prepared_currency_map = prepared_table_2

# prepared_transactions: as-is from table_1
trans = prepared_transactions.copy()

# prepared_currency_map contains an array-like column 'CZK_cols' with entries like '38144-SME'.
# Build a set of customer IDs whose segment currency is CZK (parsing the 'NNNNN-SEG' pattern).
czk_entries = prepared_currency_map.loc[:, 'CZK_cols']
if isinstance(czk_entries, pd.Series):
    # explode in case it's stored as list in a single row
    czk_list = []
    for v in czk_entries.explode().dropna().tolist():
        czk_list.append(v)
else:
    czk_list = []

czk_customer_ids = set()
for entry in czk_list:
    # Expect format like '38144-KAM'; split on last '-'
    if isinstance(entry, str) and '-' in entry:
        cid = entry.split('-', 1)[0]
        try:
            czk_customer_ids.add(int(cid))
        except ValueError:
            pass

# Filter transactions to date 2012-08-26 and morning times (00:00:00-11:59:59)
mask_date = pd.to_datetime(trans['Date']).dt.date == pd.to_datetime('2012-08-26').date()
# Parse Time as datetime.time; handle strings like 'HH:MM:SS'
time_series = pd.to_datetime(trans['Time'], format='%H:%M:%S', errors='coerce')
mask_morning = time_series.dt.hour.between(0, 11)  # inclusive 0-11

# Determine CZK-paid transactions by mapping CustomerID to the CZK customer set
is_czk_customer = trans['CustomerID'].isin(list(czk_customer_ids))

result_count = trans[mask_date & mask_morning & is_czk_customer].shape[0]

answer = result_count

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
