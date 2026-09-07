import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['preferred_foot'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['preferred_foot'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
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
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'preferred_foot', 'date'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'preferred_foot', 'date'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="birthday", date_format="%Y-%m-%d")
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
    table_1['birthday'] = table_1['birthday'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['birthday'] = table_1['birthday'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['player_api_id', 'birthday'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['player_api_id', 'birthday'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['player_api_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['player_api_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'birthday'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'birthday'] if c in table_1.columns]
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
prepared_player_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_players = prepared_table_2

# prepared_player_attributes and prepared_players are the synthesized per-table outputs
merged = prepared_player_attributes.merge(prepared_players, on='player_api_id', how='inner')

# Derive birth year
merged['birthday'] = pd.to_datetime(merged['birthday'], errors='coerce')
merged['birth_year'] = merged['birthday'].dt.year

# Filter birth year range
eligible = merged[(merged['birth_year'] >= 1987) & (merged['birth_year'] <= 1992)]

# If multiple attribute rows per player, reduce to one per player (e.g., most recent record)
eligible['date'] = pd.to_datetime(eligible['date'], errors='coerce')
eligible_sorted = eligible.sort_values(['player_api_id', 'date'], ascending=[True, False])
per_player = eligible_sorted.drop_duplicates(subset=['player_api_id'], keep='first')

# Compute percentage preferring left foot
denom = len(per_player)
if denom == 0:
    result = 0.0
else:
    num_left = (per_player['preferred_foot'].str.lower() == 'left').sum()
    result = 100.0 * num_left / denom

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
