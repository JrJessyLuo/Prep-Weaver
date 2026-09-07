import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CustomerID", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CustomerID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CustomerID']
    if _dtype == "datetime64":
        table_1['CustomerID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CustomerID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Segment", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Segment"] = table_1["Segment"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Currency", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1]
    #     return s.strip().upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1]
        return s.strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Currency"] = table_1["Currency"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['CustomerID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['CustomerID'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CustomerID', 'Segment', 'Currency'])
    # SelectCol
    _cols = [c for c in ['CustomerID', 'Segment', 'Currency'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CustomerID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CustomerID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CustomerID']
    if _dtype == "datetime64":
        table_1['CustomerID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CustomerID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Consumption", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Consumption'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Consumption']
    if _dtype == "datetime64":
        table_1['Consumption'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Consumption'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Consumption'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Consumption'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Year", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Year'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Year']
    if _dtype == "datetime64":
        table_1['Year'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Year'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Year'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Year'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Month", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Month'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Month']
    if _dtype == "datetime64":
        table_1['Month'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Month'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Month'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Month'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['CustomerID', 'Year', 'Month', 'Consumption'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['CustomerID', 'Year', 'Month', 'Consumption'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # GroupBy(table_name="table_1", by=['CustomerID', 'Year', 'Month'], agg=[{'column': 'Consumption', 'agg_func': 'sum'}])
    # GroupBy
    table_1 = table_1.groupby(['CustomerID', 'Year', 'Month'], as_index=False).agg({'Consumption': 'sum'})

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CustomerID', 'Year', 'Month', 'Consumption'])
    # SelectCol
    _cols = [c for c in ['CustomerID', 'Year', 'Month', 'Consumption'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
customers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
consumption_facts = prepared_table_2

target = consumption_facts.merge(customers[['CustomerID','Segment']], on='CustomerID', how='inner')
result = target[(target['Segment']=='SME') & (target['Year']==2013)].groupby('Month', as_index=False)['Consumption'].mean().rename(columns={'Consumption':'avg_monthly_consumption'})

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
