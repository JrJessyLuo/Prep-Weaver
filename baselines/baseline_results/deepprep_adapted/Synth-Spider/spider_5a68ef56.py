import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Value", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     if (len(t) >= 2) and ((t[0] == t[-1]) and t[0] in ['"', "'"]):
    #         t = t[1:-1].strip()
    #     return t
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        t = str(s).strip()
        if (len(t) >= 2) and ((t[0] == t[-1]) and t[0] in ['"', "'"]):
            t = t[1:-1].strip()
        return t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Value"] = table_1["Value"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Attribute", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     if (len(t) >= 2) and ((t[0] == t[-1]) and t[0] in ['"', "'"]):
    #         t = t[1:-1].strip()
    #     return t
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        t = str(s).strip()
        if (len(t) >= 2) and ((t[0] == t[-1]) and t[0] in ['"', "'"]):
            t = t[1:-1].strip()
        return t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Attribute"] = table_1["Attribute"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Value", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     t = str(s).strip()
    #     if (len(t) >= 2) and ((t[0] == t[-1]) and t[0] in ['"', "'"]):
    #         t = t[1:-1].strip()
    #     return t
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        t = str(s).strip()
        if (len(t) >= 2) and ((t[0] == t[-1]) and t[0] in ['"', "'"]):
            t = t[1:-1].strip()
        return t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Value"] = table_1["Value"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row['Attribute']).strip() == 'Item'
    # """)
    # Filter
    def filter_func(row):
        return str(row['Attribute']).strip() == 'Item'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Receipt', 'Ordinal', 'Attribute', 'Value'])
    # SelectCol
    _cols = [c for c in ['Receipt', 'Ordinal', 'Attribute', 'Value'] if c in table_1.columns]
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
    # OutlierDetection(table_name="table_1", column_name="Price", action="delete")
    # OutlierDetection (IQR method)
    _q1 = table_1['Price'].quantile(0.25)
    _q3 = table_1['Price'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_Price_is_outlier'] = table_1['Price'].apply(lambda x: True if x < _low or x > _high else False)
    if 'delete' == 'delete':
        table_1 = table_1[table_1['table_1_Price_is_outlier'] == False]
        table_1.drop(columns=['table_1_Price_is_outlier'], inplace=True)
    elif 'delete' == 'add_tag':
        table_1['table_1_Price_is_outlier'] = table_1['table_1_Price_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Price", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Price'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Price']
    if _dtype == "datetime64":
        table_1['Price'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Price'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Price'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Price'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Flavor", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Flavor"] = table_1["Flavor"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Food", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Food"] = table_1["Food"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id_Part1", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"none", "null", "nan", ""}:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"none", "null", "nan", ""}:
            return None
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id_Part1"] = table_1["Id_Part1"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id_Part2", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"none", "null", "nan", ""}:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"none", "null", "nan", ""}:
            return None
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id_Part2"] = table_1["Id_Part2"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id_Part3", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"none", "null", "nan", ""}:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"none", "null", "nan", ""}:
            return None
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id_Part3"] = table_1["Id_Part3"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id_Part4", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"none", "null", "nan", ""}:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"none", "null", "nan", ""}:
            return None
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id_Part4"] = table_1["Id_Part4"].apply(_std_apply)

    # ---------------- Step 9 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Id_Part5", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in {"none", "null", "nan", ""}:
    #         return None
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in {"none", "null", "nan", ""}:
            return None
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Id_Part5"] = table_1["Id_Part5"].apply(_std_apply)

    # ---------------- Step 10 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Price', 'Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5', 'Flavor', 'Food'])
    # SelectCol
    _cols = [c for c in ['Price', 'Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5', 'Flavor', 'Food'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 11 ----------------
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
prepared_receipts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_catalog = prepared_table_2

# Assume prepared_receipts and prepared_catalog are provided as DataFrames
r = prepared_receipts.copy()
# Filter to item rows
r = r[r['Attribute'].str.lower() == 'item']

# Parse receipt item code in Value into up to 5 dash-separated parts
# e.g., '70-M-CH-DZ' -> parts[0]='70', parts[1]='M', parts[2]='CH', parts[3]='DZ', parts[4]=None
parts = r['Value'].astype(str).str.split('-', n=4, expand=True)
parts = parts.rename(columns={0:'Id_Part1',1:'Id_Part2',2:'Id_Part3',3:'Id_Part4',4:'Id_Part5'})
r_parsed = pd.concat([r[['Receipt','Value']], parts], axis=1)

# Normalize None-like strings to actual None for matching
for c in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    r_parsed[c] = r_parsed[c].where(r_parsed[c].notna(), None)

c = prepared_catalog.copy()
# Ensure catalog Id parts are strings; treat 'None' literal as missing
for ccol in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    c[ccol] = c[ccol].astype(object)
    c[ccol] = c[ccol].apply(lambda x: None if pd.isna(x) or str(x).strip().lower() in {'none','nan',''} else str(x))

# Align types for join by coercing receipt parts similarly
for rcol in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    r_parsed[rcol] = r_parsed[rcol].apply(lambda x: None if pd.isna(x) or str(x).strip().lower() in {'none','nan',''} else str(x))

# Perform composite join on all available parts (exact match including Nones)
merge_keys = ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']
linked = r_parsed.merge(c, how='inner', on=merge_keys)

# Filter for goods costing more than 13 dollars
linked = linked[linked['Price'] > 13]

# Get distinct receipt numbers
answer = linked['Receipt'].dropna().drop_duplicates().sort_values().astype(str).tolist()

result = {
    'answer': answer,
    'evidence_preview': linked[['Receipt','Value','Flavor','Food','Price']].head(10).to_dict(orient='records')
}

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
