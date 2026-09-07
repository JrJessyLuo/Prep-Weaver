import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['agency_id', 'agency_details'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['agency_id', 'agency_details'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['agency_id', 'agency_details'])
    # SelectCol
    _cols = [c for c in ['agency_id', 'agency_details'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # StandardizeString(table_name="table_1", column_name="sic_client_combined", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = s.replace(' || ', '|').replace('||', '|')
    #     s = s.replace(' | ', '|')
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = s.replace(' || ', '|').replace('||', '|')
        s = s.replace(' | ', '|')
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["sic_client_combined"] = table_1["sic_client_combined"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'agency_id', 'sic_client_combined'])
    # SelectCol
    _cols = [c for c in ['client_id', 'agency_id', 'sic_client_combined'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     val = row.get('sic_client_combined', None)
    #     if val is None:
    #         return False
    #     return 'Mac' in str(val)
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        val = row.get('sic_client_combined', None)
        if val is None:
            return False
        return 'Mac' in str(val)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

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
prepared_agencies = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_clients_agencies = prepared_table_2

target = prepared_clients_agencies.merge(prepared_agencies, on='agency_id', how='inner')
# Filter clients whose sic_client_combined contains 'Mac' as a token or substring
filtered = target[target['sic_client_combined'].str.contains('Mac', case=False, na=False)]
# Select agency details for those clients
answer = filtered[['client_id', 'agency_id', 'agency_details']].drop_duplicates()

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
