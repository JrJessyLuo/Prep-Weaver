import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['University_ID'] = (df['ID_Tens'].astype(str) + df['ID_Units'].astype(str)).astype(int)
    target = df.groupby('University_ID', as_index=False)['Research_point'].max()
    target = target[['University_ID', 'Research_point']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['University_ID','Uni_Name_Prefix','Uni_Name_Suffix']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_scores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_universities = prepared_table_2

# prepared_scores: expects columns [ID_Tens, ID_Units, Research_point] from table_1
prepared_scores = table_1.copy()
prepared_scores['University_ID'] = (prepared_scores['ID_Tens'].astype(str) + prepared_scores['ID_Units'].astype(str)).astype(int)
prepared_scores = prepared_scores[['University_ID', 'Research_point']]

# prepared_universities: expects columns [University_ID, Uni_Name_Prefix, Uni_Name_Suffix] from table_2
prepared_universities = table_2[['University_ID', 'Uni_Name_Prefix', 'Uni_Name_Suffix']].copy()
prepared_universities['University_ID'] = prepared_universities['University_ID'].astype(int)

# Integrate on University_ID
merged = prepared_scores.merge(prepared_universities, on='University_ID', how='inner')

# Find university with the maximum Research_point
max_row = merged.loc[merged['Research_point'].astype(int).idxmax()]

# Construct full name (handle missing suffix/prefix gracefully)
prefix = str(max_row.get('Uni_Name_Prefix', '') or '').strip()
suffix = str(max_row.get('Uni_Name_Suffix', '') or '').strip()
full_name = (prefix + (' ' + suffix if suffix else '')).strip()

answer = full_name

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
