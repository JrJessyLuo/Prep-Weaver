import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['client_id','detail_part1','detail_part2','sic_code','agency_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.sort_values(['client_id','invoice_id']).drop_duplicates(subset=['client_id'], keep='last')[['invoice_id','client_id','invoice_details_Finish','invoice_details_Starting','invoice_details_Working']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['meeting_id','client_id','meeting_outcome','meeting_type','start_date_time','end_date_time','purpose_of_meeting']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_invoices = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_meetings = prepared_table_3

clients = prepared_clients
inv = prepared_invoices
mtg = prepared_meetings
# Determine clients who have either an invoice or a meeting
clients_with_activity = clients.merge(inv[['client_id','invoice_id']], on='client_id', how='left')\
    .merge(mtg[['client_id','meeting_id']], on='client_id', how='left')
mask = clients_with_activity['invoice_id'].notna() | clients_with_activity['meeting_id'].notna()
result_clients = clients_with_activity.loc[mask]
# Build a details field from available client details (non-aggregating)
result = result_clients.assign(details=(result_clients['detail_part1'].fillna('') + ' ' + result_clients['detail_part2'].fillna('')).str.strip())
# Return ids and details of clients
answer = result[['client_id','details']].drop_duplicates()

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
