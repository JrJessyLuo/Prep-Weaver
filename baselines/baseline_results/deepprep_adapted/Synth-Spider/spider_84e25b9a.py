import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['role', 'conference_staff'])
    # SelectCol
    _cols = [c for c in ['role', 'conference_staff'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Explode(table_name="table_1", column="conference_staff", split_comma=True)
    # Explode
    _ex_cols = 'conference_staff' if isinstance('conference_staff', list) else ['conference_staff']
    if all(_c in table_1.columns for _c in _ex_cols):
        try:
            for _col in _ex_cols:
                _nn = table_1[_col].dropna()
                _sample = _nn.iloc[0] if not _nn.empty else None
                if isinstance(_sample, str) or (pd.isna(_sample) and True):
                    if True:
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
    # StandardizeString(table_name="table_1", column_name="conference_staff", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return re.sub(r'\s+', '', str(s).strip())
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return re.sub(r'\s+', '', str(s).strip())
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["conference_staff"] = table_1["conference_staff"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="conference_staff", target_columns=['staff_id', 'conference_id'], func="""
    # def split(val):
    #     if val is None:
    #         return {"staff_id": None, "conference_id": None}
    #     parts = str(val).split('-', 1)
    #     if len(parts) != 2:
    #         return {"staff_id": None, "conference_id": None}
    #     return {"staff_id": parts[0], "conference_id": parts[1]}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"staff_id": None, "conference_id": None}
        parts = str(val).split('-', 1)
        if len(parts) != 2:
            return {"staff_id": None, "conference_id": None}
        return {"staff_id": parts[0], "conference_id": parts[1]}
    for _c in ['staff_id', 'conference_id']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['conference_staff']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['staff_id', 'conference_id']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['conference_staff'])

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="staff_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['staff_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['staff_id']
    if _dtype == "datetime64":
        table_1['staff_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['staff_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['staff_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['staff_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="conference_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['conference_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['conference_id']
    if _dtype == "datetime64":
        table_1['conference_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['conference_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['conference_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['conference_id'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['staff_id', 'conference_id', 'role'])
    # SelectCol
    _cols = [c for c in ['staff_id', 'conference_id', 'role'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_staff", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     # assume first column contains attributes like name/Age/Nationality
    #     attr_col = table_1.columns[0]
    #     df = table_1.copy()
    #     df[attr_col] = df[attr_col].astype(str).str.strip().str.lower()
    # 
    #     # melt then pivot to one row per staff_id
    #     id_cols = [c for c in df.columns if c != attr_col]
    #     long_df = df.melt(id_vars=[attr_col], value_vars=id_cols, var_name="staff_id", value_name="val")
    #     long_df["staff_id"] = pd.to_numeric(long_df["staff_id"], errors="coerce").astype("Int64")
    # 
    #     wide = long_df.pivot_table(index="staff_id", columns=attr_col, values="val", aggfunc="first").reset_index()
    # 
    #     # normalize expected column names
    #     rename_map = {}
    #     for c in wide.columns:
    #         if isinstance(c, str):
    #             if c in ["age"]:
    #                 rename_map[c] = "age"
    #             elif c in ["name"]:
    #                 rename_map[c] = "name"
    #             elif c in ["nationality"]:
    #                 rename_map[c] = "nationality"
    #     wide = wide.rename(columns=rename_map)
    # 
    #     # enforce types
    #     if "age" in wide.columns:
    #         wide["age"] = pd.to_numeric(wide["age"], errors="coerce").astype("Int64")
    #     if "name" in wide.columns:
    #         wide["name"] = wide["name"].astype(str)
    #     if "nationality" in wide.columns:
    #         wide["nationality"] = wide["nationality"].astype(str)
    # 
    #     # keep only required columns if present
    #     cols = ["staff_id", "name", "age", "nationality"]
    #     return wide[[c for c in cols if c in wide.columns]]
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        # assume first column contains attributes like name/Age/Nationality
        attr_col = table_1.columns[0]
        df = table_1.copy()
        df[attr_col] = df[attr_col].astype(str).str.strip().str.lower()

        # melt then pivot to one row per staff_id
        id_cols = [c for c in df.columns if c != attr_col]
        long_df = df.melt(id_vars=[attr_col], value_vars=id_cols, var_name="staff_id", value_name="val")
        long_df["staff_id"] = pd.to_numeric(long_df["staff_id"], errors="coerce").astype("Int64")

        wide = long_df.pivot_table(index="staff_id", columns=attr_col, values="val", aggfunc="first").reset_index()

        # normalize expected column names
        rename_map = {}
        for c in wide.columns:
            if isinstance(c, str):
                if c in ["age"]:
                    rename_map[c] = "age"
                elif c in ["name"]:
                    rename_map[c] = "name"
                elif c in ["nationality"]:
                    rename_map[c] = "nationality"
        wide = wide.rename(columns=rename_map)

        # enforce types
        if "age" in wide.columns:
            wide["age"] = pd.to_numeric(wide["age"], errors="coerce").astype("Int64")
        if "name" in wide.columns:
            wide["name"] = wide["name"].astype(str)
        if "nationality" in wide.columns:
            wide["nationality"] = wide["nationality"].astype(str)

        # keep only required columns if present
        cols = ["staff_id", "name", "age", "nationality"]
        return wide[[c for c in cols if c in wide.columns]]
    prepared_staff = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="prepared_staff", columns=['staff_id', 'name', 'age', 'nationality'])
    # SelectCol
    _cols = [c for c in ['staff_id', 'name', 'age', 'nationality'] if c in prepared_staff.columns]
    prepared_staff = prepared_staff[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="prepared_staff", column="staff_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_staff['staff_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_staff['staff_id']
    if _dtype == "datetime64":
        prepared_staff['staff_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_staff['staff_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_staff['staff_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_staff['staff_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="prepared_staff", column="age", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_staff['age'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_staff['age']
    if _dtype == "datetime64":
        prepared_staff['age'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_staff['age'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_staff['age'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_staff['age'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="prepared_staff", column="name", dtype="str")
    # CastType
    _dtype = 'str'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_staff['name'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_staff['name']
    if _dtype == "datetime64":
        prepared_staff['name'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_staff['name'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_staff['name'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_staff['name'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="prepared_staff", column="nationality", dtype="str")
    # CastType
    _dtype = 'str'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = prepared_staff['nationality'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = prepared_staff['nationality']
    if _dtype == "datetime64":
        prepared_staff['nationality'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        prepared_staff['nationality'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        prepared_staff['nationality'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        prepared_staff['nationality'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['prepared_staff'])
    # Terminate
    result = {'prepared_staff': prepared_staff}
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_staff_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_staff = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])

# prepared_staff_assignments has columns: staff_id(int), conference_id(int), role(str)
# prepared_staff has columns: staff_id(int), name(str), age(str/int), nationality(str)

merged = prepared_staff_assignments.merge(prepared_staff, on='staff_id', how='inner')

# Filter for Canadian staff
canadian = merged[merged['nationality'].str.strip().str.casefold() == 'canada']

# Get conference IDs with Canadian staff
conf_ids = canadian['conference_id'].dropna().astype(int).unique()

# If conference names are not available in the selected tables, return IDs as names surrogate
# Deduplicate and sort for deterministic output
result = pd.Series(conf_ids).sort_values().astype(str).tolist()

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
