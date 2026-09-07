import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="eid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['eid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['eid']
    if _dtype == "datetime64":
        table_1['eid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['eid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['eid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['eid'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'superhero_name', 'eid', 'hid'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'superhero_name', 'eid', 'hid'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="hid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['hid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['hid']
    if _dtype == "datetime64":
        table_1['hid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['hid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['hid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['hid'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'superhero_name', 'eid', 'hid'])
    # SelectCol
    _cols = [c for c in ['id', 'superhero_name', 'eid', 'hid'] if c in table_1.columns]
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
    # ErrorDetection(table_name="table_1", column_name="attribute_name", func="""
    # def is_valid_email(val):
    #     # validate non-empty attribute name after stripping quotes/whitespace
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return len(s) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_email(val):
        # validate non-empty attribute name after stripping quotes/whitespace
        if val is None:
            return False
        s = str(val).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return len(s) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_email(val))
        except Exception:
            return False
    table_1 = table_1[table_1['attribute_name'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute_name", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace
    #     s = re.sub(r'\s+', ' ', s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize internal whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute_name"] = table_1["attribute_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'attribute_name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'attribute_name'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     v = row['attribute_name']
    #     return v is not None and str(v).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        v = row['attribute_name']
        return v is not None and str(v).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'attribute_name'])
    # SelectCol
    _cols = [c for c in ['id', 'attribute_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['hero_id', 'attribute_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['hero_id', 'attribute_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['hero_id', 'attribute_id', 'attribute_value'])
    # SelectCol
    _cols = [c for c in ['hero_id', 'attribute_id', 'attribute_value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="attribute_value", dtype="float")
    # CastType
    _dtype = 'float'
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
prepared_heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_attributes_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_hero_attributes = prepared_table_3

# Assume prepared_heroes, prepared_attributes_lookup, prepared_hero_attributes are given DataFrames
# 1) Join attributes to their names
attr_long = prepared_hero_attributes.merge(prepared_attributes_lookup, left_on='attribute_id', right_on='id', how='left')

# 2) Pivot attributes so each hero has named attributes as columns (if applicable)
attr_wide = attr_long.pivot_table(index='hero_id', columns='attribute_name', values='attribute_value', aggfunc='first').reset_index()

# 3) Merge heroes with attributes
heroes_enriched = prepared_heroes.merge(attr_wide, left_on='id', right_on='hero_id', how='left')

# Note: The question asks for blue eyes and blond hair. If eye/hair colors are stored via eid/hid FK codes,
# the actual color decoding tables are not provided among selected tables. If instead colors are present in attributes
# (e.g., columns named 'Eye color' and 'Hair color' after pivot), filter using those.

# Try attribute-based filtering first
name_col = 'superhero_name'
results = []
if 'Eye color' in heroes_enriched.columns and 'Hair color' in heroes_enriched.columns:
    mask = (heroes_enriched['Eye color'].astype(str).str.lower() == 'blue') & \
           (heroes_enriched['Hair color'].astype(str).str.lower().isin(['blond','blonde']))
    results = heroes_enriched.loc[mask, name_col].dropna().drop_duplicates().sort_values().tolist()
else:
    # Fallback: cannot resolve eid/hid to color names with available tables; return empty pending lookup tables
    results = []

answer = results

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
