import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['agency_id','agency_details']].drop_duplicates(subset=['agency_id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['client_id','agency_id','sic_client_combined']].copy()
    target['client_id'] = pd.to_numeric(target['client_id'], errors='coerce').astype('Int64')
    target['agency_id'] = pd.to_numeric(target['agency_id'], errors='coerce').astype('Int64')
    target['sic_client_combined'] = target['sic_client_combined'].astype(str).str.strip()
    target = target.dropna(subset=['client_id','agency_id','sic_client_combined']).drop_duplicates(subset=['client_id','agency_id','sic_client_combined']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
