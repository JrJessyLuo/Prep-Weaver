import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['team_api_id','team_long_name','team_short_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    long_df = table_1.melt(id_vars=['id'], var_name='team_api_id', value_name='value')
    speed_df = long_df[long_df['id'].astype(str).str.strip().eq('buildUpPlaySpeed')].copy()
    speed_df['team_api_id'] = pd.to_numeric(speed_df['team_api_id'], errors='coerce')
    speed_df['buildUpPlaySpeed'] = pd.to_numeric(speed_df['value'], errors='coerce')
    speed_df = speed_df.dropna(subset=['team_api_id', 'buildUpPlaySpeed'])
    speed_df['team_api_id'] = speed_df['team_api_id'].astype('int64')
    speed_df = speed_df.sort_values(['team_api_id']).groupby('team_api_id', as_index=False)['buildUpPlaySpeed'].first()
    speed_df['buildUpPlaySpeedClass'] = pd.cut(speed_df['buildUpPlaySpeed'], bins=[-float('inf'), 33, 66, float('inf')], labels=['Slow', 'Balanced', 'Fast'], include_lowest=True).astype(str)
    target = speed_df[['team_api_id', 'buildUpPlaySpeedClass']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_teams = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_team_attributes = prepared_table_2

target = prepared_team_attributes.merge(prepared_teams, on='team_api_id', how='inner')
answer = target.loc[target['buildUpPlaySpeedClass'].str.lower() == 'fast', ['team_long_name']].dropna().drop_duplicates().sort_values('team_long_name')

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
