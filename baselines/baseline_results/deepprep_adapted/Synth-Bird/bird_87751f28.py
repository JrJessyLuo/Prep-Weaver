import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="personal_info", target_columns=['gender', 'birth_date', 'age_code'], func="""
    # def split(val):
    #     if val is None:
    #         return {"gender": None, "birth_date": None, "age_code": None}
    #     parts = str(val).split('#')
    #     gender = parts[0] if len(parts) > 0 else None
    #     birth_date = parts[1] if len(parts) > 1 else None
    #     age_code = parts[2] if len(parts) > 2 else None
    #     return {"gender": gender, "birth_date": birth_date, "age_code": age_code}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"gender": None, "birth_date": None, "age_code": None}
        parts = str(val).split('#')
        gender = parts[0] if len(parts) > 0 else None
        birth_date = parts[1] if len(parts) > 1 else None
        age_code = parts[2] if len(parts) > 2 else None
        return {"gender": gender, "birth_date": birth_date, "age_code": age_code}
    for _c in ['gender', 'birth_date', 'age_code']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['personal_info']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['gender', 'birth_date', 'age_code']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['personal_info'])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="birth_date", date_format="%Y-%m-%d")
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
    table_1['birth_date'] = table_1['birth_date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['birth_date'] = table_1['birth_date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     bd = row.get('birth_date')
    #     if bd is None or pd.isna(bd):
    #         return False
    #     # birth_date standardized to YYYY-MM-DD, so year is first 4 chars
    #     return str(bd)[:4] == \"1920\"
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        bd = row.get('birth_date')
        if bd is None or pd.isna(bd):
            return False
        # birth_date standardized to YYYY-MM-DD, so year is first 4 chars
        return str(bd)[:4] == \"1920\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'gender', 'birth_date', 'age_code'])
    # SelectCol
    _cols = [c for c in ['client_id', 'gender', 'birth_date', 'age_code'] if c in table_1.columns]
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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'client id', 'new_name': 'client_id'}, {'old_name': 'account id', 'new_name': 'account_id'}])
    # Rename
    table_1 = table_1.rename(columns={'client id': 'client_id', 'account id': 'account_id'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="type", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # strip whitespace and surrounding quotes
    #     s2 = str(s).strip()
    #     s2 = re.sub(r'^["\']+|["\']+$', '', s2)
    #     return s2.strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # strip whitespace and surrounding quotes
        s2 = str(s).strip()
        s2 = re.sub(r'^["\']+|["\']+$', '', s2)
        return s2.strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["type"] = table_1["type"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'account_id', 'type'])
    # SelectCol
    _cols = [c for c in ['client_id', 'account_id', 'type'] if c in table_1.columns]
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
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="district_id", func="""
    # def is_valid(val):
    #     try:
    #         return val is not None and str(val).strip() != '' and int(val) > 0
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        try:
            return val is not None and str(val).strip() != '' and int(val) > 0
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['district_id'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'district_id'])
    # SelectCol
    _cols = [c for c in ['account_id', 'district_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="account_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['account_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['account_id']
    if _dtype == "datetime64":
        table_1['account_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['account_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['account_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['account_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="district_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['district_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['district_id']
    if _dtype == "datetime64":
        table_1['district_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['district_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['district_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['district_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['account_id', 'district_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['account_id', 'district_id'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['account_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['account_id'], keep='first').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="district_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['district_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['district_id']
    if _dtype == "datetime64":
        table_1['district_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['district_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['district_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['district_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="kraj", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # strip surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     # normalize spacing and case
    #     s = re.sub(r'\s+', ' ', s).strip().lower()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # strip surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        # normalize spacing and case
        s = re.sub(r'\s+', ' ', s).strip().lower()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["kraj"] = table_1["kraj"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['kraj'] == 'east bohemia'
    # """)
    # Filter
    def filter_func(row):
        return row['kraj'] == 'east bohemia'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['district_id', 'kraj'])
    # SelectCol
    _cols = [c for c in ['district_id', 'kraj'] if c in table_1.columns]
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
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_dispositions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_accounts = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_districts = prepared_table_4

# Assume prepared tables already created as per targets
# prepared_clients has columns: client_id, gender, birth_date, age_code
# prepared_dispositions: client_id, account_id, type
# prepared_accounts: account_id, district_id
# prepared_districts: district_id, kraj

# Integrate
cd = prepared_clients.merge(prepared_dispositions, on='client_id', how='inner')
CDA = cd.merge(prepared_accounts, on='account_id', how='inner')
CDAK = CDA.merge(prepared_districts, on='district_id', how='inner')

# Filter: born in 1920 and region is east Bohemia (case-insensitive match)
CDAK['birth_year'] = pd.to_datetime(CDAK['birth_date'], errors='coerce').dt.year
mask = (CDAK['birth_year'] == 1920) & (CDAK['kraj'].str.lower() == 'east bohemia')
subset = CDAK.loc[mask, ['client_id']].drop_duplicates()

answer = len(subset)

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
