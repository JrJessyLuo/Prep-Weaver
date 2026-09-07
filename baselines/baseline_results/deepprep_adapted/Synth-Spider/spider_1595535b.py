import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'name', 'heat_result'])
    # SelectCol
    _cols = [c for c in ['id', 'name', 'heat_result'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="heat_result", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"')
    #     # Convert formats like "4-4:16.571" or "1-4:21.558" -> "4:16.571" / "4:21.558"
    #     s = re.sub(r'^\d+\s*-\s*', '', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"')
        # Convert formats like "4-4:16.571" or "1-4:21.558" -> "4:16.571" / "4:21.558"
        s = re.sub(r'^\d+\s*-\s*', '', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["heat_result"] = table_1["heat_result"].apply(_std_apply)

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
    # SelectCol(table_name="table_1", columns=['cid', 'bike_id'])
    # SelectCol
    _cols = [c for c in ['cid', 'bike_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['cid', 'bike_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['cid', 'bike_id'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'product_material'])
    # SelectCol
    _cols = [c for c in ['id', 'product_material'] if c in table_1.columns]
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
prepared_cyclists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_purchases = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_bikes = prepared_table_3

# Assume prepared_* dataframes exist
# 1) Parse heat_result like '3-4:19.232' -> time '4:19.232'
def parse_time_to_seconds(s):
    # s is like 'rank-mm:ss.mmm' or 'mm:ss.mmm'
    if pd.isna(s):
        return None
    part = s
    if '-' in s:
        part = s.split('-', 1)[1]
    try:
        mm, rest = part.split(':', 1)
        mm = int(mm)
        ss = float(rest)
        return mm*60 + ss
    except Exception:
        return None

threshold_sec = parse_time_to_seconds('4:21.558')

cyclists = prepared_cyclists.copy()
cyclists['time_sec'] = cyclists['heat_result'].apply(parse_time_to_seconds)
fast_cyclists = cyclists[cyclists['time_sec'].notna() & (cyclists['time_sec'] < threshold_sec)][['id']]

# 2) Join purchases
cp = fast_cyclists.merge(prepared_purchases, left_on='id', right_on='cid', how='inner')

# 3) Join bikes
cpb = cp.merge(prepared_bikes, left_on='bike_id', right_on='id', how='inner', suffixes=('', '_bike'))

# 4) Extract bike name from product_material before '###'
def extract_bike_name(s):
    if pd.isna(s):
        return None
    return s.split('###', 1)[0].strip()

cpb['bike_name'] = cpb['product_material'].apply(extract_bike_name)

# 5) Select distinct bike names
result = sorted(cpb['bike_name'].dropna().unique().tolist())

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
