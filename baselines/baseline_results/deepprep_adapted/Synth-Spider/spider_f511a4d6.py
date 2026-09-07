import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['name', 'nation_result'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['name', 'nation_result'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # collapse internal whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # collapse internal whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name"] = table_1["name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="nation_result", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     # normalize spacing around the pipe separator
    #     s = re.sub(r'\s*\|\s*', '|', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        # normalize spacing around the pipe separator
        s = re.sub(r'\s*\|\s*', '|', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["nation_result"] = table_1["nation_result"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'name', 'nation_result'])
    # SelectCol
    _cols = [c for c in ['id', 'name', 'nation_result'] if c in table_1.columns]
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
    # DropNulls(table_name="table_1", subset=['cyclist_id', 'bike_purchase_combined'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['cyclist_id', 'bike_purchase_combined'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="bike_purchase_combined", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"'')
    # 
    #     # normalize internal whitespace
    #     s = re.sub(r'\s+', '', s)
    # 
    #     # accept forms like "3_2017" (digits underscore 4-digit year)
    #     m = re.match(r'^(\d+)_((?:19|20)\d{2})$', s)
    #     if m:
    #         return f"{m.group(1)}_{m.group(2)}"
    # 
    #     # if already close but has extra characters, keep cleaned version
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().strip('"'')

        # normalize internal whitespace
        s = re.sub(r'\s+', '', s)

        # accept forms like "3_2017" (digits underscore 4-digit year)
        m = re.match(r'^(\d+)_((?:19|20)\d{2})$', s)
        if m:
            return f"{m.group(1)}_{m.group(2)}"

        # if already close but has extra characters, keep cleaned version
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["bike_purchase_combined"] = table_1["bike_purchase_combined"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="cyclist_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['cyclist_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['cyclist_id']
    if _dtype == "datetime64":
        table_1['cyclist_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['cyclist_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['cyclist_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['cyclist_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['cyclist_id', 'bike_purchase_combined'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['cyclist_id', 'bike_purchase_combined'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['cyclist_id', 'bike_purchase_combined'])
    # SelectCol
    _cols = [c for c in ['cyclist_id', 'bike_purchase_combined'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="product_name", mode="mode")
    # MissingValueImputation
    table_1["product_name"] = table_1["product_name"].fillna(table_1["product_name"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'product_name'])
    # SelectCol
    _cols = [c for c in ['id', 'product_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cyclists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_purchases = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_bikes = prepared_table_3

# prepared_cyclists: columns ['id','name','nation_result']
# prepared_purchases: columns ['cyclist_id','bike_purchase_combined'] where bike_purchase_combined like 'productId_year'
# prepared_bikes: columns ['id','product_name']

# Decompose purchase into product id to validate against bikes
pp = prepared_purchases.copy()
pp[['bike_id_str','year_str']] = pp['bike_purchase_combined'].str.split('_', n=1, expand=True)
pp['bike_id'] = pd.to_numeric(pp['bike_id_str'], errors='coerce')

# Validate bike_id exists in bike catalog (treat those as racing bikes)
pp_valid = pp.merge(prepared_bikes.rename(columns={'id':'bike_id'}), on='bike_id', how='inner')

# Find cyclists with no purchases (anti-join)
purchased_cyclist_ids = pp_valid['cyclist_id'].dropna().unique()
no_purchase = prepared_cyclists[~prepared_cyclists['id'].isin(purchased_cyclist_ids)].copy()

# Split nation and result from nation_result for output
no_purchase[['nation','result']] = no_purchase['nation_result'].str.split('|', n=1, expand=True)

answer = no_purchase[['name','nation','result']].reset_index(drop=True)

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
