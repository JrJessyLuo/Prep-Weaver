import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_OWNER_KEY', 'MOIRA_LIST_KEY', 'moira_list_member'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_OWNER_KEY', 'MOIRA_LIST_KEY', 'moira_list_member'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="moira_list_member", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # keep original casing; just normalize whitespace for stable downstream joins/counts
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # keep original casing; just normalize whitespace for stable downstream joins/counts
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["moira_list_member"] = table_1["moira_list_member"].apply(_std_apply)

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
    # StandardizeDatetime(table_name="table_1", column_name="WAREHOUSE_LOAD_DATE", date_format="%d-%b-%y")
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
    table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].apply(_sd_parse)
    if '%d-%b-%y':
        table_1['WAREHOUSE_LOAD_DATE'] = table_1['WAREHOUSE_LOAD_DATE'].dt.strftime('%d-%b-%y')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'])
    # SelectCol
    _cols = [c for c in ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['MOIRA_LIST_OWNER_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['MOIRA_LIST_OWNER_KEY'], keep='last').reset_index(drop=True)

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
prepared_memberships = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_owners = prepared_table_2

target = prepared_memberships.merge(prepared_owners, on='MOIRA_LIST_OWNER_KEY', how='inner')
filtered = target[target['MOIRA_LIST_OWNER_KEY'] == 'LIST69.377-keeper-xenon']
owner_name = filtered['OWNER'].dropna().iloc[0] if not filtered.empty else None
total_lists = filtered['MOIRA_LIST_KEY'].nunique()
total_members = filtered.shape[0]
answer = {'owner': owner_name, 'total_mailing_lists': int(total_lists), 'total_members': int(total_members)}

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
