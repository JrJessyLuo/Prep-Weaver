import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['IAP_SUBJECT_CATEGORY_KEY','IAP_SUBJECT_SPONSOR_KEY','ACTIVITY_TITLE','FEE']].copy()
    df['FEE'] = pd.to_numeric(df['FEE'].replace(['nan','NaN','None','', ' '], pd.NA), errors='coerce')
    target = df.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_SUBJECT_SPONSOR_KEY','ACTIVITY_TITLE'], as_index=False).agg(FEE=('FEE','first'))
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
iap_activities = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_categories = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
iap_sponsors = prepared_table_3

# Assume prepared tables already loaded as DataFrames: iap_activities, iap_categories, iap_sponsors
# Join activities to category and sponsor dimensions
fact_dim = (
    iap_activities
    .merge(iap_categories, on='IAP_SUBJECT_CATEGORY_KEY', how='left')
    .merge(iap_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')
)

# Clean fee to numeric and drop NaNs for averaging
fact_dim['FEE'] = pd.to_numeric(fact_dim['FEE'], errors='coerce')

# Group by category name and sponsor name
agg = (
    fact_dim
    .groupby(['IAP_CATEGORY_NAME', 'SPONSOR_NAME'], dropna=False)
    .agg(
        activities_offered=('ACTIVITY_TITLE', 'nunique'),
        avg_fee_per_activity=('FEE', 'mean')
    )
    .reset_index()
)

# Sort by number of activities descending
result = agg.sort_values(by='activities_offered', ascending=False)

target = result[['IAP_CATEGORY_NAME', 'SPONSOR_NAME', 'activities_offered', 'avg_fee_per_activity']]

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
