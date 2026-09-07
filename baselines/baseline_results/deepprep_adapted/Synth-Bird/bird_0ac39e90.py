import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'date', 'new_name': 'open_date'}])
    # Rename
    table_1 = table_1.rename(columns={'date': 'open_date'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="open_date", date_format="%Y-%m-%d")
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
    table_1['open_date'] = table_1['open_date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['open_date'] = table_1['open_date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['account_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['account_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'open_date', 'new_name': 'date'}])
    # Rename
    table_1 = table_1.rename(columns={'open_date': 'date'})

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'district_id', 'frequency', 'date'])
    # SelectCol
    _cols = [c for c in ['account_id', 'district_id', 'frequency', 'date'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="type", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().lower().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().lower().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["type"] = table_1["type"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['card_id', 'disp_id', 'type', 'year', 'month', 'day'])
    # SelectCol
    _cols = [c for c in ['card_id', 'disp_id', 'type', 'year', 'month', 'day'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_accounts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_cards = prepared_table_2

gold_cards = prepared_cards[prepared_cards['type'].str.lower() == 'gold']
# Join cards -> dispositions to get account_id
cards_with_accounts = gold_cards.merge(prepared_dispositions[['disp_id','account_id']], on='disp_id', how='inner')
# Join to accounts to get account details (optional for evidence)
result = cards_with_accounts.merge(prepared_accounts[['account_id']], on='account_id', how='inner').drop_duplicates(subset=['account_id'])
# Final answer: accounts that have gold credit cards
answer = result[['account_id']]

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
