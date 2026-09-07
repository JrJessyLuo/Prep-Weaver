import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="guoji", func="""
    # def transform_func(s):
    #     return s.strip().title() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip().title() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["guoji"] = table_1["guoji"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'guoji'])
    # SelectCol
    _cols = [c for c in ['driverId', 'guoji'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['driverId'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['driverId'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['driverId'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['driverId'], keep='last').reset_index(drop=True)

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
    # ErrorDetection(table_name="table_1", column_name="fastestLapTime", func="""
    # import re
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip().strip('"').strip("'")
    #     # allow m:ss.mmm or mm:ss.mmm
    #     return re.fullmatch(r"\d{1,2}:\d{2}\.\d{3}", s) is not None
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip().strip('"').strip("'")
        # allow m:ss.mmm or mm:ss.mmm
        return re.fullmatch(r"\d{1,2}:\d{2}\.\d{3}", s) is not None
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['fastestLapTime'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fastestLapTime", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     t = str(s).strip().strip('"').strip("'")
    #     # Keep only valid m:ss.mmm / mm:ss.mmm patterns; otherwise set to None
    #     return t if re.fullmatch(r"\d{1,2}:\d{2}\.\d{3}", t) else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        t = str(s).strip().strip('"').strip("'")
        # Keep only valid m:ss.mmm / mm:ss.mmm patterns; otherwise set to None
        return t if re.fullmatch(r"\d{1,2}:\d{2}\.\d{3}", t) else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fastestLapTime"] = table_1["fastestLapTime"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['driverId', 'fastestLapTime'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['driverId', 'fastestLapTime'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'fastestLapTime'])
    # SelectCol
    _cols = [c for c in ['driverId', 'fastestLapTime'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
drivers_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_11'])
results_prepared = prepared_table_2

def parse_lap_time(s):
    # Expect formats like 'M:SS.mmm' or 'MM:SS.mmm'; return milliseconds
    if pd.isna(s):
        return pd.NA
    try:
        parts = str(s).split(':')
        if len(parts) != 2:
            return pd.NA
        minutes = int(parts[0])
        sec_ms = parts[1]
        if '.' in sec_ms:
            seconds, millis = sec_ms.split('.')
            seconds = int(seconds)
            millis = int((millis + '000')[:3])
        else:
            seconds = int(sec_ms)
            millis = 0
        return minutes*60_000 + seconds*1_000 + millis
    except Exception:
        return pd.NA

# Join drivers with results on driverId
merged = drivers_prepared.merge(results_prepared, on='driverId', how='inner')

# Filter French drivers (nationality column 'guoji' equals 'French')
french = merged[merged['guoji'].str.lower() == 'french']

# Parse fastest lap times and filter under 02:00.000 (i.e., < 120,000 ms)
french = french.assign(
    fastestLapMs=french['fastestLapTime'].apply(parse_lap_time)
)
valid = french[pd.notna(french['fastestLapMs']) & (french['fastestLapMs'] < 120_000)]

# Count distinct drivers who have any lap under 2 minutes
answer = valid['driverId'].nunique()

result = pd.DataFrame({'answer': [int(answer)]})

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
