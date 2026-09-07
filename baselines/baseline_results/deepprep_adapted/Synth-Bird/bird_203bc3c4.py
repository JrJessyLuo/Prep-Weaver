import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Date", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r"\s*[/\-]\s*", "-", s)   # normalize separators and remove surrounding spaces
    #     s = re.sub(r"\s+", "", s)              # remove remaining spaces
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r"\s*[/\-]\s*", "-", s)   # normalize separators and remove surrounding spaces
        s = re.sub(r"\s+", "", s)              # remove remaining spaces
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Date"] = table_1["Date"].apply(_std_apply)

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
    # import re
    # from datetime import datetime
    # 
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # Accept 'H:M', 'HH:MM', 'HH:MM:SS' (and variants with extra spaces)
    #     s = re.sub(r"\s+", "", s)
    #     for fmt in ("%H:%M:%S", "%H:%M"):
    #         try:
    #             t = datetime.strptime(s, fmt).time()
    #             return t.strftime("%H:%M:%S")
    #         except Exception:
    #             pass
    #     return s
    # """)
    # StandardizeString

    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # Accept 'H:M', 'HH:MM', 'HH:MM:SS' (and variants with extra spaces)
        s = re.sub(r"\s+", "", s)
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                t = datetime.strptime(s, fmt).time()
                return t.strftime("%H:%M:%S")
            except Exception:
                pass
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
    # Concatenate(table_name="table_1", concatenate_columns=['Country_Part1', 'Country_Part2'], target_column="Country_Code", func="""
    # def concat(row: pd.Series) -> str:
    #     p1 = '' if pd.isna(row['Country_Part1']) else str(row['Country_Part1']).strip()
    #     p2 = '' if pd.isna(row['Country_Part2']) else str(row['Country_Part2']).strip()
    #     return f"{p1}{p2}" if (p1 or p2) else None
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        p1 = '' if pd.isna(row['Country_Part1']) else str(row['Country_Part1']).strip()
        p2 = '' if pd.isna(row['Country_Part2']) else str(row['Country_Part2']).strip()
        return f"{p1}{p2}" if (p1 or p2) else None
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["Country_Code"] = table_1[['Country_Part1', 'Country_Part2']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['Country_Part1', 'Country_Part2'])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="Country_Code", target_columns=['Country_Part1', 'Country_Part2'], func="""
    # import pandas as pd
    # def split(val):
    #     if pd.isna(val):
    #         return {"Country_Part1": None, "Country_Part2": None}
    #     s = str(val).strip()
    #     if len(s) <= 2:
    #         return {"Country_Part1": s if s else None, "Country_Part2": None}
    #     return {"Country_Part1": s[:2], "Country_Part2": s[2:]}
    # """)
    # SplitColumn
    def split(val):
        if pd.isna(val):
            return {"Country_Part1": None, "Country_Part2": None}
        s = str(val).strip()
        if len(s) <= 2:
            return {"Country_Part1": s if s else None, "Country_Part2": None}
        return {"Country_Part1": s[:2], "Country_Part2": s[2:]}
    for _c in ['Country_Part1', 'Country_Part2']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['Country_Code']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['Country_Part1', 'Country_Part2']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['Country_Code'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['GasStationID', 'Country_Part1', 'Country_Part2'])
    # SelectCol
    _cols = [c for c in ['GasStationID', 'Country_Part1', 'Country_Part2'] if c in table_1.columns]
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

# Assume prepared tables are provided as DataFrames: prepared_transactions, prepared_stations
# 1) Join on GasStationID
merged = prepared_transactions.merge(prepared_stations, on='GasStationID', how='left')

# 2) Normalize date and time for exact match
# The question datetime is '2012/8/24 12:42:00'. We normalize both the data and the query.
def norm_date(s):
    # handle formats like '2012-08-24' and '2012 / 08 / 24'
    s = str(s).replace(' ', '')  # remove spaces
    s = s.replace('/', '-')
    return s  # '2012-08-24'

def norm_time(s):
    return str(s).strip()

merged['_norm_date'] = merged['Date'].apply(norm_date)
merged['_norm_time'] = merged['Time'].apply(norm_time)

query_dt = '2012/8/24 12:42:00'
# normalize query
q_date_raw, q_time = query_dt.split(' ')
# pad month/day to two digits by parsing with pandas
q_date_parsed = pd.to_datetime(q_date_raw, format='%Y/%m/%d')
q_date_norm = q_date_parsed.strftime('%Y-%m-%d')
q_time_norm = q_time.strip()

# 3) Filter to the specific deal
row = merged[(merged['_norm_date'] == q_date_norm) & (merged['_norm_time'] == q_time_norm)]

# 4) Construct country from parts; prefer concatenation without separator if parts look like code pieces
def build_country(r):
    p1 = str(r.get('Country_Part1', ''))
    p2 = str(r.get('Country_Part2', ''))
    if p1 and p2 and len(p2) == 1:
        return p1 + p2
    elif p1 and p2:
        return (p1 + ' ' + p2).strip()
    else:
        return p1 or p2 or None

row = row.copy()
if not row.empty:
    row['Country'] = row.apply(build_country, axis=1)

# 5) Select final answer (country) — if multiple matches, take unique values
answer = row['Country'].dropna().unique().tolist()

result = {'answer': answer[0] if len(answer)==1 else answer, 'evidence_count': len(row), 'evidence_transaction_ids': row['TransactionID'].astype(str).tolist()}

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
