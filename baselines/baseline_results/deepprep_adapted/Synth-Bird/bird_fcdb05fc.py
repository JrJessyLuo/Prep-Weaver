import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="first_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["first_name"] = table_1["first_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="superhero_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     if s == "-":
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        if s == "-":
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["superhero_name"] = table_1["superhero_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="first_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     if s == "-":
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        if s == "-":
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["first_name"] = table_1["first_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="last_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     if s == "-":
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        if s == "-":
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["last_name"] = table_1["last_name"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="height_cm", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['height_cm'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['height_cm']
    if _dtype == "datetime64":
        table_1['height_cm'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['height_cm'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['height_cm'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['height_cm'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="weight_kg", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['weight_kg'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['weight_kg']
    if _dtype == "datetime64":
        table_1['weight_kg'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['weight_kg'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['weight_kg'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['weight_kg'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'superhero_name', 'gender_id', 'eye_colour_id', 'hair_colour_id', 'skin_colour_id', 'race_id', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg', 'first_name', 'last_name'])
    # SelectCol
    _cols = [c for c in ['id', 'superhero_name', 'gender_id', 'eye_colour_id', 'hair_colour_id', 'skin_colour_id', 'race_id', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg', 'first_name', 'last_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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
    # DropNulls(table_name="table_1", subset=['hero_id', 'aid', 'av'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['hero_id', 'aid', 'av'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['hero_id', 'aid', 'av'])
    # SelectCol
    _cols = [c for c in ['hero_id', 'aid', 'av'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="aid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['aid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['aid']
    if _dtype == "datetime64":
        table_1['aid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['aid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['aid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['aid'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="av", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['av'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['av']
    if _dtype == "datetime64":
        table_1['av'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['av'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['av'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['av'] = _series.astype(str)

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
    # Explode(table_name="table_1", column=['id', 'attribute_name'], split_comma=False)
    # Explode
    _ex_cols = ['id', 'attribute_name'] if isinstance(['id', 'attribute_name'], list) else [['id', 'attribute_name']]
    if all(_c in table_1.columns for _c in _ex_cols):
        try:
            for _col in _ex_cols:
                _nn = table_1[_col].dropna()
                _sample = _nn.iloc[0] if not _nn.empty else None
                if isinstance(_sample, str) or (pd.isna(_sample) and False):
                    if False:
                        table_1[_col] = table_1[_col].apply(lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) and x != '' else [])
                    else:
                        def _ex_parse(x):
                            if pd.isna(x) or x == '':
                                return []
                            try:
                                _r = ast.literal_eval(str(x))
                                return _r if isinstance(_r, list) else [_r]
                            except Exception:
                                return [i.strip() for i in str(x).split()]
                        table_1[_col] = table_1[_col].apply(_ex_parse)
                elif not isinstance(_sample, list) and _sample is not None:
                    table_1[_col] = table_1[_col].apply(lambda x: [x] if pd.notna(x) else [])
            if len(_ex_cols) == 1:
                table_1 = table_1.explode(_ex_cols[0]).reset_index(drop=True)
            else:
                table_1 = table_1.explode(_ex_cols).reset_index(drop=True)
        except Exception:
            pass

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
    # CastType(table_name="table_1", column="attribute_name", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['attribute_name'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['attribute_name']
    if _dtype == "datetime64":
        table_1['attribute_name'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['attribute_name'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['attribute_name'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['attribute_name'] = _series.astype(str)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="id", func="""
    # def is_valid(val):
    #     try:
    #         int(val)
    #         return True
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        try:
            int(val)
            return True
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['id'].apply(_err_apply)]

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
    # StandardizeString(table_name="table_1", column_name="gender", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ["'", '"']):
    #         s = s[1:-1].strip()
    #     # normalize common NA markers
    #     if s.upper() in ["N/A", "NA", "NULL", "NONE", ""]:
    #         return "Unknown"
    #     # normalize capitalization for known values
    #     if s.lower() == "male":
    #         return "Male"
    #     if s.lower() == "female":
    #         return "Female"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ["'", '"']):
            s = s[1:-1].strip()
        # normalize common NA markers
        if s.upper() in ["N/A", "NA", "NULL", "NONE", ""]:
            return "Unknown"
        # normalize capitalization for known values
        if s.lower() == "male":
            return "Male"
        if s.lower() == "female":
            return "Female"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["gender"] = table_1["gender"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'gender'])
    # SelectCol
    _cols = [c for c in ['id', 'gender'] if c in table_1.columns]
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
def _prep_5(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="colour", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     # normalize internal whitespace
    #     s2 = " ".join(s2.split())
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip()
        # normalize internal whitespace
        s2 = " ".join(s2.split())
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["colour"] = table_1["colour"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'colour'])
    # SelectCol
    _cols = [c for c in ['id', 'colour'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # DropNulls(table_name="table_1", subset=['id', 'colour'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'colour'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

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
def _prep_6(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['race'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['race'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'race'])
    # SelectCol
    _cols = [c for c in ['id', 'race'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['id'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['id'], ascending=[True])

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
def _prep_7(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'publisher_name'])
    # SelectCol
    _cols = [c for c in ['id', 'publisher_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="publisher_name", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return "Unknown"
    #     # strip quotes if they exist as literal characters and trim whitespace
    #     s2 = str(s).strip().strip('"').strip("'").strip()
    #     # treat empty as unknown
    #     if s2 == "":
    #         return "Unknown"
    #     # collapse internal whitespace
    #     s2 = re.sub(r'\s+', ' ', s2)
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return "Unknown"
        # strip quotes if they exist as literal characters and trim whitespace
        s2 = str(s).strip().strip('"').strip("'").strip()
        # treat empty as unknown
        if s2 == "":
            return "Unknown"
        # collapse internal whitespace
        s2 = re.sub(r'\s+', ' ', s2)
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["publisher_name"] = table_1["publisher_name"].apply(_std_apply)

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
def _prep_8(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="alignment", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     return str(val).strip() in {"Good","Bad","Neutral"}
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        return str(val).strip() in {"Good","Bad","Neutral"}
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['alignment'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="alignment", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1].strip()
    #     # normalize capitalization
    #     return s.capitalize()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding quotes if present
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1].strip()
        # normalize capitalization
        return s.capitalize()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["alignment"] = table_1["alignment"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'alignment'])
    # SelectCol
    _cols = [c for c in ['id', 'alignment'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
hero_attribute_values = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
attribute_dictionary = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
gender_lu = prepared_table_4
prepared_table_5 = _prep_5(tables['table_5'])
colour_lu = prepared_table_5
prepared_table_6 = _prep_6(tables['table_9'])
race_lu = prepared_table_6
prepared_table_7 = _prep_7(tables['table_8'])
publisher_lu = prepared_table_7
prepared_table_8 = _prep_8(tables['table_4'])
alignment_lu = prepared_table_8

# Assume prepared tables exist as DataFrames: heroes, hero_attribute_values, attribute_dictionary, gender_lu, colour_lu, race_lu, publisher_lu, alignment_lu

# Filter to the target hero
h = heroes[heroes['superhero_name'] == '3-D Man'].copy()

# Decode categorical attributes
h = h.merge(gender_lu.rename(columns={'id':'gender_id'}), on='gender_id', how='left')
h = h.merge(race_lu.rename(columns={'id':'race_id'}), on='race_id', how='left')
h = h.merge(publisher_lu.rename(columns={'id':'publisher_id'}), on='publisher_id', how='left')
h = h.merge(alignment_lu.rename(columns={'id':'alignment_id'}), on='alignment_id', how='left')

# Decode colours (eye, hair, skin) using colour_lu three times
h = h.merge(colour_lu.rename(columns={'id':'eye_colour_id','colour':'eye_colour'}), on='eye_colour_id', how='left')
h = h.merge(colour_lu.rename(columns={'id':'hair_colour_id','colour':'hair_colour'}), on='hair_colour_id', how='left')
h = h.merge(colour_lu.rename(columns={'id':'skin_colour_id','colour':'skin_colour'}), on='skin_colour_id', how='left')

# Pull numeric attributes for the hero and map attribute names
attrs = hero_attribute_values.merge(attribute_dictionary, left_on='aid', right_on='id', how='left')
attrs = attrs[attrs['hero_id'].isin(h['id'])]

# Assemble attribute name -> value pairs
pairs = []
if not h.empty:
    row = h.iloc[0]
    basic_attrs = {
        'Superhero Name': row['superhero_name'],
        'First Name': row.get('first_name'),
        'Last Name': row.get('last_name'),
        'Gender': row.get('gender'),
        'Eye Colour': row.get('eye_colour'),
        'Hair Colour': row.get('hair_colour'),
        'Skin Colour': row.get('skin_colour'),
        'Race': row.get('race'),
        'Publisher': row.get('publisher_name'),
        'Alignment': row.get('alignment'),
        'Height (cm)': row.get('height_cm'),
        'Weight (kg)': row.get('weight_kg')
    }
    for k,v in basic_attrs.items():
        pairs.append({'attribute': k, 'value': v})

# Add numeric ability attributes (Intelligence, Strength, etc.)
if not attrs.empty:
    for _, r in attrs.iterrows():
        pairs.append({'attribute': r['attribute_name'], 'value': r['av']})

answer = pd.DataFrame(pairs)
answer

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
