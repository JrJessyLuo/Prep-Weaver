import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['PostId','bamt']].copy()
    df = df.dropna(subset=['bamt'])
    df['bamt'] = pd.to_numeric(df['bamt'], errors='coerce')
    df = df.dropna(subset=['bamt'])
    target = df.groupby('PostId', as_index=False)['bamt'].max()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    filtered = table_1[table_1['Id'].eq('Title')].copy()
    target = filtered[['record_id','value']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
post_bounties = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
post_titles = prepared_table_2

# Assume prepared tables are provided as dataframes: post_bounties, post_titles
# Filter titles to only Title rows
titles = post_titles.query("Id == 'Title' or Id.str.lower() == 'title' if 'Id' in post_titles.columns else True")
if 'Id' in titles.columns:
    titles = titles[['record_id','value']]

# Coerce join keys to string for safe merge
post_bounties['PostId'] = post_bounties['PostId'].astype(str)
titles['record_id'] = titles['record_id'].astype(str)

# Join bounties to titles
joined = post_bounties.merge(titles, left_on='PostId', right_on='record_id', how='inner')

# Filter posts whose title mentions 'data' (case-insensitive)
mask = joined['value'].astype(str).str.contains('data', case=True, regex=False) | joined['value'].astype(str).str.contains('data', case=False, regex=False)
filtered = joined[mask]

# Sum bounty amounts; coerce to numeric, ignore NaNs
filtered['bamt'] = pd.to_numeric(filtered['bamt'], errors='coerce')
result_value = float(filtered['bamt'].sum()) if not filtered.empty else 0.0

answer = {
    'total_bounty_amount': result_value,
}

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
