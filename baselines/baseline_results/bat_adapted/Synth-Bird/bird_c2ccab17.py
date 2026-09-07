import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    parts = df['CustomerID_Segment'].astype(str).str.split('-', n=1, expand=True)
    df['CustomerID'] = pd.to_numeric(parts[0], errors='coerce').astype('Int64')
    df['Segment'] = parts[1]
    target = df[['CustomerID', 'Segment', 'Currency', 'CustomerID_Segment']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['CustomerID','Consumption','Year','Month']].copy()
    df['Year'] = df['Year'].astype(str)
    df['Month'] = df['Month'].astype(str).str.zfill(2)
    df['Consumption'] = pd.to_numeric(df['Consumption'], errors='coerce')
    target = df.groupby(['CustomerID','Year','Month'], as_index=False, dropna=False)['Consumption'].sum()[['CustomerID','Consumption','Year','Month']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_consumption = prepared_table_2

# prepared_clients: split composite key
clients = prepared_clients.copy()
# Ensure types
clients['CustomerID'] = pd.to_numeric(clients['CustomerID'], errors='coerce')

# prepared_consumption: ensure types and filter September 2013
cons = prepared_consumption.copy()
cons['CustomerID'] = pd.to_numeric(cons['CustomerID'], errors='coerce')
cons['Year'] = cons['Year'].astype(str)
cons['Month'] = cons['Month'].astype(str).str.zfill(2)

# Join on CustomerID to attach Segment
joined = cons.merge(clients[['CustomerID', 'Segment', 'Currency', 'CustomerID_Segment']], on='CustomerID', how='inner')

# Filter to September 2013
sept13 = joined[(joined['Year'] == '2013') & (joined['Month'] == '09')]

# Aggregate consumption by segment
seg_sum = sept13.groupby('Segment', dropna=False, as_index=False)['Consumption'].sum()

# Find segment with least consumption
least_row = seg_sum.sort_values('Consumption', ascending=True).head(1)

# Prepare final answer output (segment name and value)
answer = {
    'segment': None if least_row.empty else least_row.iloc[0]['Segment'],
    'consumption': None if least_row.empty else float(least_row.iloc[0]['Consumption'])
}

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
