import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="date", dtype="datetime")
    # CastType
    _dtype = 'datetime'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['date'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['date']
    if _dtype == "datetime64":
        table_1['date'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['date'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['date'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['date'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['account_id', 'district_id', 'date'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['account_id', 'district_id', 'date'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'district_id', 'date'])
    # SelectCol
    _cols = [c for c in ['account_id', 'district_id', 'date'] if c in table_1.columns]
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="client_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['client_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['client_id']
    if _dtype == "datetime64":
        table_1['client_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['client_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="type", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["type"] = table_1["type"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'client_id', 'type'])
    # SelectCol
    _cols = [c for c in ['account_id', 'client_id', 'type'] if c in table_1.columns]
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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'client_id', 'new_name': 'client_id'}, {'old_name': 'gender', 'new_name': 'gender'}])
    # Rename
    table_1 = table_1.rename(columns={'client_id': 'client_id', 'gender': 'gender'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="gender", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     # convert to string, strip whitespace, remove quotes, uppercase
    #     t = str(s).strip()
    #     t = re.sub(r"["']", "", t).strip()
    #     t = t.upper()
    #     # normalize common variants
    #     if t in ["F", "FEMALE"]:
    #         return "F"
    #     if t in ["M", "MALE"]:
    #         return "M"
    #     return t
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        # convert to string, strip whitespace, remove quotes, uppercase
        t = str(s).strip()
        t = re.sub(r"["']", "", t).strip()
        t = t.upper()
        # normalize common variants
        if t in ["F", "FEMALE"]:
            return "F"
        if t in ["M", "MALE"]:
            return "M"
        return t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["gender"] = table_1["gender"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'gender'])
    # SelectCol
    _cols = [c for c in ['client_id', 'gender'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['client_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['client_id'], keep='last').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="value", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['value'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['value']
    if _dtype == "datetime64":
        table_1['value'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['value'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['value'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['value'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="district_number", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['district_number'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['district_number']
    if _dtype == "datetime64":
        table_1['district_number'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['district_number'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['district_number'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['district_number'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['district_number', 'value'])
    # SelectCol
    _cols = [c for c in ['district_number', 'value'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
accounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
dispositions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
clients = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
district_metrics = prepared_table_4

# Assume prepared tables exist: accounts, dispositions, clients, district_metrics
# 1) Convert keys to comparable types
accounts = accounts.copy()
accounts['district_id'] = pd.to_numeric(accounts['district_id'], errors='coerce')

metrics = district_metrics.copy()
metrics['district_number'] = pd.to_numeric(metrics['district_number'], errors='coerce')
metrics['value'] = pd.to_numeric(metrics['value'], errors='coerce')

# 2) Join accounts to district metrics to get average salary per account's district
acc_with_salary = accounts.merge(metrics, left_on='district_id', right_on='district_number', how='inner')

# 3) Keep only districts with average salary > 10000
rich_acc = acc_with_salary[acc_with_salary['value'] > 10000][['account_id']]

# 4) Link dispositions (only owners) to those accounts
owners = dispositions[dispositions['type'].str.upper() == 'OWNER']
rich_owner_links = owners.merge(rich_acc, on='account_id', how='inner')

# 5) Join to clients to get gender
rich_clients = rich_owner_links.merge(clients[['client_id','gender']], on='client_id', how='left')

# 6) Compute percentage of women among these clients
denom = len(rich_clients)
if denom == 0:
    result = 0.0
else:
    num_women = (rich_clients['gender'].str.upper() == 'F').sum()
    result = 100.0 * num_women / denom

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
