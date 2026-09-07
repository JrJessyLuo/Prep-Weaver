import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'superhero_name'])
    # SelectCol
    _cols = [c for c in ['id', 'superhero_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'superhero_name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'superhero_name'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['power_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['power_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="power_name", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize internal whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["power_name"] = table_1["power_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['power_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['power_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'power_name'])
    # SelectCol
    _cols = [c for c in ['id', 'power_name'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['hero_id', 'attribute_id', 'attribute_value'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['hero_id', 'attribute_id', 'attribute_value'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['hero_id', 'attribute_id', 'attribute_value'])
    # SelectCol
    _cols = [c for c in ['hero_id', 'attribute_id', 'attribute_value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="hero_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['hero_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['hero_id']
    if _dtype == "datetime64":
        table_1['hero_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['hero_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['hero_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['hero_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="attribute_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['attribute_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['attribute_id']
    if _dtype == "datetime64":
        table_1['attribute_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['attribute_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['attribute_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['attribute_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="attribute_value", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['attribute_value'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['attribute_value']
    if _dtype == "datetime64":
        table_1['attribute_value'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['attribute_value'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['attribute_value'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['attribute_value'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['hero_id', 'attribute_id', 'attribute_value'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['hero_id', 'attribute_id', 'attribute_value'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['attribute_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['attribute_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['id']
    if _dtype == "datetime64":
        table_1['id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute_name", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ["'", '"']):
    #         s = s[1:-1].strip()
    #     # collapse internal whitespace
    #     s = re.sub(r"\s+", " ", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ["'", '"']):
            s = s[1:-1].strip()
        # collapse internal whitespace
        s = re.sub(r"\s+", " ", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute_name"] = table_1["attribute_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'attribute_name'])
    # SelectCol
    _cols = [c for c in ['id', 'attribute_name'] if c in table_1.columns]
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
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
powers = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
hero_attributes = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
attributes = prepared_table_4

# Assume prepared tables are provided as DataFrames: heroes, powers, hero_attributes, attributes
# Count powers per hero by interpreting the three quoted columns in heroes as binary power flags
power_flag_cols = [c for c in heroes.columns if c.strip('"') in ['1','2','3']]

# Convert to numeric and treat non-null & >0 as having that power
flag_df = heroes[['id','superhero_name'] + power_flag_cols].copy()
for c in power_flag_cols:
    flag_df[c] = pd.to_numeric(flag_df[c], errors='coerce')

# Count number of powers per hero (count non-na where value > 0)
power_counts = flag_df.assign(
    power_count=flag_df[power_flag_cols].gt(0).sum(axis=1)
)[['id','superhero_name','power_count']]

# Find hero(es) with max powers
max_cnt = power_counts['power_count'].max()
result = power_counts.loc[power_counts['power_count'] == max_cnt, ['superhero_name']]

# Prepare final answer as a list of names or a single name depending on ties
answer = result['superhero_name'].tolist()

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
