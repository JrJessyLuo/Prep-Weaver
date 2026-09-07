import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CustomerId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CustomerId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CustomerId']
    if _dtype == "datetime64":
        table_1['CustomerId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CustomerId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CustomerId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CustomerId'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ReceiptNumber", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes (including doubled quotes like ""10013"")
    #     while (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # also collapse any remaining double-quotes inside
    #     s = s.replace('""', '').replace('"', '').strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes (including doubled quotes like ""10013"")
        while (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # also collapse any remaining double-quotes inside
        s = s.replace('""', '').replace('"', '').strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ReceiptNumber"] = table_1["ReceiptNumber"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
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
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CustomerId', 'Date', 'ReceiptNumber'])
    # SelectCol
    _cols = [c for c in ['CustomerId', 'Date', 'ReceiptNumber'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="ming", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     return s.title()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        return s.title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ming"] = table_1["ming"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove repeated wrapping quotes like ""1"" or "1"
    #     while (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove repeated wrapping quotes like ""1"" or "1"
        while (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id"] = table_1["Id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="xing", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     return s.title()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        return s.title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["xing"] = table_1["xing"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Id', 'xing', 'ming'])
    # SelectCol
    _cols = [c for c in ['Id', 'xing', 'ming'] if c in table_1.columns]
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
prepared_visits = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_customers = prepared_table_2

# Assume prepared_visits and prepared_customers are already synthesized per targets.
# Normalize key types because sources show numeric ids stored as strings with possible quotes.
vis = prepared_visits.copy()
cust = prepared_customers.copy()

# Strip quotes and cast to int for robust joining
vis['CustomerId'] = vis['CustomerId'].astype(str).str.replace('"', '', regex=False).astype(int)
cust['Id'] = cust['Id'].astype(str).str.replace('"', '', regex=False).astype(int)

# Parse dates; source format like '17-Oct-2007'
vis['Date_parsed'] = pd.to_datetime(vis['Date'], format='%d-%b-%Y', errors='coerce')

# Find the earliest visit date
min_date = vis['Date_parsed'].min()
earliest_visits = vis[vis['Date_parsed'] == min_date]

# Join to customers to get names
joined = earliest_visits.merge(cust, left_on='CustomerId', right_on='Id', how='left')

# Select required output columns: first name (ming) and last name (xing)
# If multiple customers share the same earliest date, return all.
answer = joined[['ming', 'xing']].rename(columns={'ming': 'FirstName', 'xing': 'LastName'})

target = answer

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
