import pandas as pd
import numpy as np

def _prep_1(table_1):
    parts = table_1['personal_info'].astype(str).str.split('#', n=2, expand=True)
    df = table_1.assign(gender=parts[0], birth_date=pd.to_datetime(parts[1], errors='coerce'), unknown_field=parts[2])
    df = df.assign(birth_year=df['birth_date'].dt.year.astype('Int64'))
    df = df[df['birth_year'].eq(1920)]
    target = df[['client_id','gender','birth_date','birth_year','unknown_field']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['client_id','account_id','type']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[:, ['account_id','district_id','frequency','date']].copy()
    target['frequency'] = target['frequency'].astype('string').str.strip()
    target['date'] = pd.to_datetime(target['date'], errors='coerce')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['district_id','okres','kraj']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_dispositions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_accounts = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_districts = prepared_table_4

# Assume prepared tables already created as per table_targets
# prepared_clients has columns [client_id, gender, birth_date, birth_year, unknown_field]
# prepared_dispositions has [client_id, account_id, type]
# prepared_accounts has [account_id, district_id, frequency, date]
# prepared_districts has [district_id, okres, kraj]

# Integrate
cd = prepared_clients.merge(prepared_dispositions, on='client_id', how='inner')
cdA = cd.merge(prepared_accounts, on='account_id', how='inner')
full = cdA.merge(prepared_districts, on='district_id', how='inner')

# Question-specific filtering: born in 1920 and region east Bohemia
filt = (full['birth_year'] == 1920) & (full['kraj'].str.lower() == 'east bohemia')
subset = full.loc[filt, ['client_id']].drop_duplicates()

answer = len(subset)
answer

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
