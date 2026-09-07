import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['player_fifa_api_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['player_fifa_api_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'player_fifa_api_id', 'preferred_foot'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'player_fifa_api_id', 'preferred_foot'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="preferred_foot", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().lower()
    #     if s in ["left", "right"]:
    #         return s
    #     return None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().lower()
        if s in ["left", "right"]:
            return s
        return None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["preferred_foot"] = table_1["preferred_foot"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="preferred_foot", mode="mode")
    # MissingValueImputation
    table_1["preferred_foot"] = table_1["preferred_foot"].fillna(table_1["preferred_foot"].mode().iloc[0])

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['player_api_id', 'player_fifa_api_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['player_api_id', 'player_fifa_api_id'], how='any').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="weight", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['weight'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['weight']
    if _dtype == "datetime64":
        table_1['weight'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['weight'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['weight'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['weight'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'player_fifa_api_id', 'weight'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'player_fifa_api_id', 'weight'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['player_api_id', 'player_fifa_api_id', 'weight'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['player_api_id', 'player_fifa_api_id', 'weight'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['player_api_id', 'player_fifa_api_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['player_api_id', 'player_fifa_api_id'], keep='last').reset_index(drop=True)

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

target = prepared_player_attributes.merge(prepared_players, on='player_api_id', how='inner')
# Ensure weight is numeric and filter under 130
if target['weight'].dtype == object:
    target['weight_numeric'] = pd.to_numeric(target['weight'], errors='coerce')
else:
    target['weight_numeric'] = target['weight']
filtered = target[target['weight_numeric'] < 130]
answer = (filtered['preferred_foot'].str.lower() == 'left').sum()

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
