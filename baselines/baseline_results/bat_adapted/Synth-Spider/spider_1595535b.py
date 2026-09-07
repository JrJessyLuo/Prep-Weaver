import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['id', 'name', 'heat_result']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['cid','bike_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['product_material'] = df['product_material'].astype(str).str.split('###').str[0]
    target = df[['id','product_material']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
