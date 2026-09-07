import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Platform_ID','pn','md']].copy()
    target['pn'] = target['pn'].astype(str).str.strip()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Game_ID','Title',1,2,3,4]].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_platforms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_games = prepared_table_2

# Assume prepared_platforms and prepared_games already exist per targets.

# Normalize platform names and districts
prepared_platforms = prepared_platforms.assign(
    pn=prepared_platforms['pn'].astype(str).str.strip(),
    md=prepared_platforms['md'].astype(str).str.strip()
)

# Unpivot numeric platform ID columns in games to long format
platform_id_cols = [c for c in prepared_games.columns if str(c).isdigit()]
long_games = prepared_games.melt(
    id_vars=['Game_ID','Title'],
    value_vars=platform_id_cols,
    var_name='Platform_ID',
    value_name='value'
)
# Coerce Platform_ID to match platforms dtype and drop rows with no association (NaN)
long_games['Platform_ID'] = long_games['Platform_ID'].astype(int)
long_games = long_games.dropna(subset=['value'])

# Join with platforms on Platform_ID
joined = long_games.merge(
    prepared_platforms[['Platform_ID','pn','md']],
    on='Platform_ID', how='inner'
)

# Filter to Asia or USA market districts and get unique game titles
result_titles = (
    joined[joined['md'].isin(['Asia','USA'])]['Title']
    .drop_duplicates()
    .sort_values()
    .tolist()
)

answer = result_titles

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
