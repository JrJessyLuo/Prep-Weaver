import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['driverId'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['driverId'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['driverId', 'fn', 'ln', 'dr', 'code'])
    # SelectCol
    _cols = [c for c in ['driverId', 'fn', 'ln', 'dr', 'code'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['driverId'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['driverId'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['raceId', 'driverId'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['raceId', 'driverId'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['raceId', 'driverId'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['raceId', 'driverId'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'driverId'])
    # SelectCol
    _cols = [c for c in ['raceId', 'driverId'] if c in table_1.columns]
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
def _prep_3(table_1):
    return table_1.copy()
def _prep_4(table_1):
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
drivers_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_11'])
qualifying_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_table_4 = _prep_4(tables['table_10'])

# Assume prepared tables are provided as dataframes: drivers_prepared, qualifying_prepared
# 1) Identify Lewis Hamilton's driverId
hamilton = drivers_prepared[(drivers_prepared['fn'].str.lower()=='lewis') & (drivers_prepared['ln'].str.lower()=='hamilton')]
# Fallbacks if necessary
if hamilton.empty:
    hamilton = drivers_prepared[(drivers_prepared['dr'].str.lower()=='hamilton') | (drivers_prepared['code'].str.lower()=='ham')]

# 2) Join to qualifying to get his race participations (raceId)
merged = hamilton[['driverId']].merge(qualifying_prepared[['driverId','raceId']], on='driverId', how='inner')

# 3) Map raceId to years
# Note: Year mapping requires a races table (raceId -> year). Since it's not among selected tables,
# we cannot derive years directly here. If a races table is available as `races_prepared` with columns ['raceId','year'], do:
# merged = merged.merge(races_prepared[['raceId','year']], on='raceId', how='left')
# years = sorted(merged['year'].dropna().unique().tolist())
# target = pd.DataFrame({'year': years})

# Without races table, return unique raceIds as participation evidence
race_ids = sorted(merged['raceId'].dropna().unique().tolist())
target = pd.DataFrame({'raceId': race_ids})

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
