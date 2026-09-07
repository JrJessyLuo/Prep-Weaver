import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['superhero_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['superhero_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['superhero_name', 'xb', 'yc', 'hc', 'sc'])
    # SelectCol
    _cols = [c for c in ['superhero_name', 'xb', 'yc', 'hc', 'sc'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="xb", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['xb'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['xb']
    if _dtype == "datetime64":
        table_1['xb'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['xb'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['xb'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['xb'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="yc", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['yc'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['yc']
    if _dtype == "datetime64":
        table_1['yc'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['yc'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['yc'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['yc'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="hc", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['hc'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['hc']
    if _dtype == "datetime64":
        table_1['hc'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['hc'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['hc'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['hc'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="sc", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['sc'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['sc']
    if _dtype == "datetime64":
        table_1['sc'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['sc'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['sc'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['sc'] = _series.astype(str)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['id'])
    # DropColumn
    table_1 = table_1.drop(columns=['id'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="variable", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['variable'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['variable']
    if _dtype == "datetime64":
        table_1['variable'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['variable'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['variable'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['variable'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="colour", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["colour"] = table_1["colour"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['variable'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['variable'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['variable', 'colour'])
    # SelectCol
    _cols = [c for c in ['variable', 'colour'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_2'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
colour_lookup = prepared_table_2

# Prepared inputs: heroes, colour_lookup
# Ensure colour_lookup only has the relevant domain if needed
colour_lookup_f = colour_lookup.copy()
if 'id' in colour_lookup_f.columns:
    colour_lookup_f = colour_lookup_f[colour_lookup_f['id'] == 'colour'][['variable','colour']]

# Cast join keys to string for reliable joins
for col in ['xb','yc','hc','sc']:
    if col in heroes.columns:
        heroes[col] = heroes[col].astype(str)
colour_lookup_f['variable'] = colour_lookup_f['variable'].astype(str)

# Join each code to its colour name
eye_map = colour_lookup_f.rename(columns={'colour':'eye_colour', 'variable':'yc'})
hair_map = colour_lookup_f.rename(columns={'colour':'hair_colour', 'variable':'hc'})
skin_map = colour_lookup_f.rename(columns={'colour':'skin_colour', 'variable':'sc'})
# xb is ambiguous; we won't use it for eye colour unless yc missing
xb_map = colour_lookup_f.rename(columns={'colour':'xb_colour', 'variable':'xb'})

enriched = heroes.merge(eye_map, on='yc', how='left') \
               .merge(hair_map, on='hc', how='left') \
               .merge(skin_map, on='sc', how='left') \
               .merge(xb_map, on='xb', how='left')

# Filter to the requested hero
row = enriched[enriched['superhero_name'].str.lower() == 'blackwulf']

# Prefer explicit eye_colour from yc; fallback to xb_colour if eye_colour missing
def pick_eye(r):
    return r['eye_colour'] if pd.notna(r.get('eye_colour')) and str(r['eye_colour']).strip() != '' else r.get('xb_colour')

answer = None
if not row.empty:
    r0 = row.iloc[0]
    answer = pick_eye(r0)

result = pd.DataFrame({'answer': [answer]})

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
