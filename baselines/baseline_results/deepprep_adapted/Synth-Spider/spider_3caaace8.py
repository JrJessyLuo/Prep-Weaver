import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="kehu_id", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['kehu_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['kehu_id']
    if _dtype == "datetime64":
        table_1['kehu_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['kehu_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['kehu_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['kehu_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['kehu_id', 'kehu_xinxi'])
    # SelectCol
    _cols = [c for c in ['kehu_id', 'kehu_xinxi'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['kehu_id', 'kehu_xinxi'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['kehu_id', 'kehu_xinxi'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['kehu_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['kehu_id'], keep='last').reset_index(drop=True)

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
    # OutlierDetection(table_name="table_1", column_name="Customer_ID", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['Customer_ID'].quantile(0.25)
    _q3 = table_1['Customer_ID'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_Customer_ID_is_outlier'] = table_1['Customer_ID'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_Customer_ID_is_outlier'] == False]
        table_1.drop(columns=['table_1_Customer_ID_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_Customer_ID_is_outlier'] = table_1['table_1_Customer_ID_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="xiangxi", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().lower()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["xiangxi"] = table_1["xiangxi"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Customer_Interaction_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Customer_Interaction_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Customer_Interaction_ID']
    if _dtype == "datetime64":
        table_1['Customer_Interaction_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Customer_Interaction_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Customer_Interaction_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Customer_Interaction_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Customer_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Customer_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Customer_ID']
    if _dtype == "datetime64":
        table_1['Customer_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Customer_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Customer_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Customer_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Service_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Service_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Service_ID']
    if _dtype == "datetime64":
        table_1['Service_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Service_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Service_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Service_ID'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Customer_Interaction_ID', 'Customer_ID', 'Service_ID', 'xiangxi'])
    # SelectCol
    _cols = [c for c in ['Customer_Interaction_ID', 'Customer_ID', 'Service_ID', 'xiangxi'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Service_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Service_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Service_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Service_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Service_ID']
    if _dtype == "datetime64":
        table_1['Service_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Service_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Service_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Service_ID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Service_Type", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Service_Type"] = table_1["Service_Type"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Details", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Details"] = table_1["Details"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Service_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Service_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Service_ID', 'Service_Type', 'Details'])
    # SelectCol
    _cols = [c for c in ['Service_ID', 'Service_Type', 'Details'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row.get('Attribute', '')).strip() == 'Customers_and_Services_ID'
    # """)
    # Filter
    def filter_func(row):
        return str(row.get('Attribute', '')).strip() == 'Customers_and_Services_ID'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Customer_ID', 'Service_ID'])
    # SelectCol
    _cols = [c for c in ['Customer_ID', 'Service_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Customer_ID', 'Service_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Customer_ID', 'Service_ID'], keep='first').reset_index(drop=True)

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
customers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
interactions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
services = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
customer_services = prepared_table_4

# Assume prepared tables: customers, interactions, services, customer_services

# Filter to the target customer by name
cust = customers[customers['kehu_xinxi'] == 'Hardy Kutch']

# Services used by the customer via direct mapping
cust_used = (
    cust.merge(customer_services, left_on='kehu_id', right_on='Customer_ID', how='inner')
        .merge(services, on='Service_ID', how='inner')
        [['Service_ID','Service_Type','Details']]
        .drop_duplicates()
)

# Services from interactions that are rated as 'good'
inter_good = (
    interactions[interactions['xiangxi'].str.lower() == 'good']
        .merge(services, on='Service_ID', how='inner')
        [['Service_ID','Service_Type','Details']]
        .drop_duplicates()
)

# Union of both criteria
result = pd.concat([cust_used, inter_good], ignore_index=True).drop_duplicates().reset_index(drop=True)

target = result

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
