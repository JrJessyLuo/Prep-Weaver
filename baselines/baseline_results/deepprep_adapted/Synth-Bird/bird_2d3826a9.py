import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['player_api_id', 'date'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['player_api_id', 'date'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="player_api_id", dtype="int64")
    # CastType
    _dtype = 'int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['player_api_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['player_api_id']
    if _dtype == "datetime64":
        table_1['player_api_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['player_api_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['player_api_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['player_api_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="player_fifa_api_id", dtype="int64")
    # CastType
    _dtype = 'int64'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['player_fifa_api_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['player_fifa_api_id']
    if _dtype == "datetime64":
        table_1['player_fifa_api_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['player_fifa_api_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['player_fifa_api_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['player_fifa_api_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="overall_rating", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['overall_rating'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['overall_rating']
    if _dtype == "datetime64":
        table_1['overall_rating'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['overall_rating'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['overall_rating'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['overall_rating'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['player_api_id', 'player_fifa_api_id', 'date', 'overall_rating'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
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
    # SelectCol(table_name="table_1", columns=['id', 'variable', 'value'])
    # SelectCol
    _cols = [c for c in ['id', 'variable', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'variable', 'value'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'variable', 'value'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id', 'variable', 'value'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id', 'variable', 'value'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_player_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_player_lookup = prepared_table_2

# Assume prepared_player_attributes (attrs) and prepared_player_lookup (lookup) are available
attrs = prepared_player_attributes.copy()
lookup = prepared_player_lookup.copy()

# Identify Aaron Doran's player_api_id using lookup if it contains a name mapping.
# Common patterns in such long tables: id could be 'player_name' with value being the name,
# and variable holding the player_api_id or vice-versa. We'll try two robust options:

# Option A: rows where id == 'player_name' (or 'name') and value == 'Aaron Doran', then take variable as player_api_id
name_keys = lookup[lookup['id'].isin(['player_name','name']) & (lookup['value'].str.lower() == 'aaron doran')]
player_ids = pd.to_numeric(name_keys['variable'], errors='coerce').dropna().astype(int)

# Option B (fallback): rows where id is 'player_api_id' and variable corresponds to name entries
if player_ids.empty:
    name_rows = lookup[lookup['id'].isin(['player_name','name']) & (lookup['value'].str.lower() == 'aaron doran')]
    # If variable in name_rows links to another table key holding player_api_id, join within lookup
    # Try to find entries where variable matches lookup['variable'] and id == 'player_api_id'
    merged = name_rows.merge(lookup[lookup['id']=='player_api_id'], on='variable', suffixes=('_name',''))
    player_ids = pd.to_numeric(merged['value'], errors='coerce').dropna().astype(int)

# If still empty, attempt fifa id path similarly
if player_ids.empty:
    fifa_rows = lookup[lookup['id'].isin(['player_name','name']) & (lookup['value'].str.lower() == 'aaron doran')]
    merged_fifa = fifa_rows.merge(lookup[lookup['id'].isin(['player_fifa_api_id','fifa_api_id'])], on='variable', suffixes=('_name',''))
    fifa_ids = pd.to_numeric(merged_fifa['value'], errors='coerce').dropna().astype(int)
    if not fifa_ids.empty:
        # Map fifa_id to attrs via player_fifa_api_id
        target_rows = attrs[attrs['player_fifa_api_id'].isin(fifa_ids)]
        result_value = float(target_rows['overall_rating'].mean()) if not target_rows.empty else None
    else:
        result_value = None
else:
    target_rows = attrs[attrs['player_api_id'].isin(player_ids)]
    result_value = float(target_rows['overall_rating'].mean()) if not target_rows.empty else None

answer = {"average_overall_rating": result_value}

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
