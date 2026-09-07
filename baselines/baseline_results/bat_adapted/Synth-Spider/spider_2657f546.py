import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['CustomerId','Date','ReceiptNumber']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Id','xing','ming']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_visits = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_customers = prepared_table_2

# Assume prepared_visits and prepared_customers are already synthesized per targets.
# Normalize key types because sources show numeric ids stored as strings with possible quotes.
vis = prepared_visits.copy()
cust = prepared_customers.copy()

# Strip quotes and cast to int for robust joining
vis['CustomerId'] = vis['CustomerId'].astype(str).str.replace('"', '', regex=False).astype(int)
cust['Id'] = cust['Id'].astype(str).str.replace('"', '', regex=False).astype(int)

# Parse dates; source format like '17-Oct-2007'
vis['Date_parsed'] = pd.to_datetime(vis['Date'], format='%d-%b-%Y', errors='coerce')

# Find the earliest visit date
min_date = vis['Date_parsed'].min()
earliest_visits = vis[vis['Date_parsed'] == min_date]

# Join to customers to get names
joined = earliest_visits.merge(cust, left_on='CustomerId', right_on='Id', how='left')

# Select required output columns: first name (ming) and last name (xing)
# If multiple customers share the same earliest date, return all.
answer = joined[['ming', 'xing']].rename(columns={'ming': 'FirstName', 'xing': 'LastName'})

target = answer

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
