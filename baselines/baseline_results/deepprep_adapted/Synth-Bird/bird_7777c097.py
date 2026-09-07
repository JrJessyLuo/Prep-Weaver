import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SEX", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'").upper()
    #     # normalize common variants
    #     if s in ["F", "FEMALE"]:
    #         return "F"
    #     if s in ["M", "MALE"]:
    #         return "M"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'").upper()
        # normalize common variants
        if s in ["F", "FEMALE"]:
            return "F"
        if s in ["M", "MALE"]:
            return "M"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SEX"] = table_1["SEX"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Birthday", date_format="%Y-%m-%d")
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
    table_1['Birthday'] = table_1['Birthday'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Birthday'] = table_1['Birthday'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'SEX', 'Birthday'])
    # SelectCol
    _cols = [c for c in ['ID', 'SEX', 'Birthday'] if c in table_1.columns]
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
    # DropNulls(table_name="table_1", subset=['ID', 'Date', 'GOT'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ID', 'Date', 'GOT'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # Date is standardized like 'YYYY-MM-DD'
    #     return str(row[\"Date\"])[:4] == \"1994\"
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # Date is standardized like 'YYYY-MM-DD'
        return str(row[\"Date\"])[:4] == \"1994\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'GOT'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'GOT'] if c in table_1.columns]
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
patients_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs_prepared = prepared_table_2

# Assume patients_prepared and labs_prepared are the synthesized per-table outputs

# 1) Integrate on patient ID
merged = patients_prepared.merge(labs_prepared, on='ID', how='inner')

# 2) Keep exams from calendar year 1994
merged['Date'] = pd.to_datetime(merged['Date'], errors='coerce')
merged_1994 = merged[merged['Date'].dt.year == 1994]

# 3) Determine normal range for GOT (AST). If the dataset has no explicit reference ranges,
#    use a common clinical reference range for AST (GOT): 10–40 U/L inclusive.
#    Adjust if local reference is known elsewhere.
merged_1994['GOT'] = pd.to_numeric(merged_1994['GOT'], errors='coerce')
normal = merged_1994[(merged_1994['GOT'] >= 10) & (merged_1994['GOT'] <= 40)]

# 4) List unique patients meeting the criterion with required fields
answer = normal[['ID', 'SEX', 'Birthday']].drop_duplicates().sort_values(['ID'])

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
