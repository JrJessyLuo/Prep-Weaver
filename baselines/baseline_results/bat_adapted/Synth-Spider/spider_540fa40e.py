import pandas as pd
import numpy as np

def _prep_1(table_1):
    import ast
    import pandas as pd
    df = table_1.copy()
    df['shuxing_list'] = df['shuxing'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df['shuxing_zhi_list'] = df['shuxing_zhi'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    long_df = df.apply(lambda r: pd.DataFrame({'siji_id': [r['siji_id']]*len(r['shuxing_list']), 'attribute': [a for a,_ in zip(r['shuxing_list'], r['shuxing_zhi_list'])], 'value': [v for _,v in zip(r['shuxing_list'], r['shuxing_zhi_list'])]}), axis=1)
    long_df = pd.concat(long_df.tolist(), ignore_index=True)
    age_df = long_df.loc[long_df['attribute'].eq('Age'), ['siji_id','value']].copy()
    age_df['Age'] = pd.to_numeric(age_df['value'], errors='coerce')
    target = age_df.dropna(subset=['Age']).groupby('siji_id', as_index=False)['Age'].first()[['siji_id','Age']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Driver_ID','Road']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
race_participation = prepared_table_2

# Assume prepared tables already created as per target schemas:
# drivers columns: ['siji_id','Age']
# race_participation columns: ['Driver_ID','Road']

# Normalize key types to string for safe join
race_participation['Driver_ID'] = race_participation['Driver_ID'].astype(str)
drivers['siji_id'] = drivers['siji_id'].astype(str)

# Join participations to driver ages
joined = race_participation.merge(drivers, left_on='Driver_ID', right_on='siji_id', how='left')

# Compute race counts per driver
counts = joined.groupby('Driver_ID', as_index=False).agg(race_count=('Road','nunique'))

# Identify driver(s) with the maximum number of races
max_count = counts['race_count'].max()
top_drivers = counts[counts['race_count'] == max_count]

# Attach ages
result = top_drivers.merge(drivers, left_on='Driver_ID', right_on='siji_id', how='left')

# Final answer: show the age(s)
answer = result[['Age']].drop_duplicates()
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
