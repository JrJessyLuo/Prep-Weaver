import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['ID'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['ID'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ID", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes and any stray whitespace
    #     s2 = str(s).strip()
    #     s2 = re.sub(r'^"+|"+$', '', s2)
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove surrounding quotes and any stray whitespace
        s2 = str(s).strip()
        s2 = re.sub(r'^"+|"+$', '', s2)
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ID"] = table_1["ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SEX", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip().upper()
    #     if s2 in ['F', 'FEMALE']:
    #         return 'F'
    #     if s2 in ['M', 'MALE']:
    #         return 'M'
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip().upper()
        if s2 in ['F', 'FEMALE']:
            return 'F'
        if s2 in ['M', 'MALE']:
            return 'M'
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SEX"] = table_1["SEX"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Diagnosis", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Diagnosis"] = table_1["Diagnosis"].apply(_std_apply)

    # ---------------- Step 5 ----------------
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

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Diagnosis', 'SEX', 'Birthday'])
    # SelectCol
    _cols = [c for c in ['ID', 'Diagnosis', 'SEX', 'Birthday'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID'], keep='first').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="PLT", mode="mean")
    # MissingValueImputation
    table_1["PLT"] = table_1["PLT"].fillna(table_1["PLT"].mean())

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
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'PLT'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'PLT'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_patients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_labs = prepared_table_2

target = prepared_patients.merge(prepared_labs, on='ID', how='inner')
# Filter to MCTD diagnosis (case-insensitive, allow variants)
mctd_mask = target['Diagnosis'].str.contains('MCTD', case=False, na=False)
ans = target[mctd_mask].copy()
# Define normal platelet range (e.g., 150-450 x10^9/L). Adjust if metadata provides reference intervals.
lower, upper = 150, 450
# Keep rows where PLT is numeric and within range
ans['PLT_numeric'] = pd.to_numeric(ans['PLT'], errors='coerce')
ans = ans[(ans['PLT_numeric'] >= lower) & (ans['PLT_numeric'] <= upper)]
# Select output columns (patient ID and platelet level, optionally date if needed for evidence)
answer = ans[['ID', 'Date', 'PLT_numeric']].rename(columns={'PLT_numeric': 'PLT'})

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
