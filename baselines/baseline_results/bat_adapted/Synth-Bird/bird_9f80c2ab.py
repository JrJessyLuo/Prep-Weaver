import pandas as pd
import numpy as np

def _prep_1(table_1):
    crime_row = table_1.loc[table_1['district_id'].eq('A4'), ['district_id', 3]].copy()
    crime_row = crime_row.rename(columns={3: 'crime_1995'})
    crime_row['crime_1995'] = pd.to_numeric(crime_row['crime_1995'], errors='coerce')
    target = crime_row[['district_id', 'crime_1995']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['district_id','fdm']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_crime_by_district = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_accounts_by_district = prepared_table_2

# prepared_crime_by_district has columns: district_id, crime_1995
# prepared_accounts_by_district has columns: district_id, fdm

# Ensure date type
prepared_accounts_by_district = prepared_accounts_by_district.copy()
prepared_accounts_by_district['fdm'] = pd.to_datetime(prepared_accounts_by_district['fdm'], errors='coerce')

# Filter accounts opened starting from 1997-01-01
acct_1997_plus = prepared_accounts_by_district[prepared_accounts_by_district['fdm'] >= pd.Timestamp('1997-01-01')]

# Get districts that have at least one such account
districts_with_1997_accounts = acct_1997_plus[['district_id']].drop_duplicates()

# Join crimes to those districts
eligible = prepared_crime_by_district.merge(districts_with_1997_accounts, on='district_id', how='inner')

# Filter regions where 1995 crimes exceed 4000
eligible = eligible[eligible['crime_1995'] > 4000]

# Compute the average number of crimes committed in 1995 across these regions
result_value = eligible['crime_1995'].mean()

answer = {'average_crimes_1995': float(result_value) if pd.notnull(result_value) else None}

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
