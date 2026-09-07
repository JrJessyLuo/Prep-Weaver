import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'ALB']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    prepared['ALB'] = pd.to_numeric(prepared['ALB'], errors='coerce')
    target = prepared[['ID', 'Date', 'ALB']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['ID']].copy()
    df = df[df['ID'].notna()]
    df['ID'] = df['ID'].astype('float64').astype('int64').astype('string')
    target = df.drop_duplicates(subset=['ID']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_table_2 = _prep_2(tables['table_3'])

# Assume prepared_table_1 and prepared_table_2 are dataframes produced per targets above.
# 1) Ensure ID types align for join
l = prepared_table_1.copy()
r = prepared_table_2.copy()

# Coerce IDs to string to handle float IDs like '14872.0' consistently across tables
l['ID'] = l['ID'].astype(str)
r['ID'] = r['ID'].astype(str)

# 2) Integrate on ID
merged = pd.merge(l, r[['ID']].drop_duplicates(), on='ID', how='inner')

# 3) Parse dates (Date is used as birthday proxy per question phrasing; if an actual birthday column existed, use that instead)
merged['Date'] = pd.to_datetime(merged['Date'], errors='coerce')

# 4) Determine albumin out-of-range flag
# Define a general adult reference range for serum albumin (g/dL): 3.5 to 5.0
# Adjust if dataset-specific reference is provided elsewhere.
merged['ALB'] = pd.to_numeric(merged['ALB'], errors='coerce')
merged['alb_out_of_range'] = ~merged['ALB'].between(3.5, 5.0, inclusive='both')

# 5) Filter to male patients if sex data were available; since no sex column exists in selected tables,
# this step is omitted. If a demographics table with Sex were provided, join it on ID and filter Sex == 'Male'.

# 6) Sort patients by birthday (here, using Date) in descending order and keep those with albumin not within range
result = merged.loc[merged['alb_out_of_range']].sort_values(by='Date', ascending=False)

# 7) Select output columns (ID, Date, ALB)
answer = result[['ID', 'Date', 'ALB']]

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
