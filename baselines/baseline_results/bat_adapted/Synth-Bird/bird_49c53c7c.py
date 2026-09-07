import pandas as pd
import numpy as np

def _prep_1(table_1):
    import numpy as np
    import pandas as pd
    table_1 = table_1.rename(columns=lambda c: c.strip() if isinstance(c, str) else c)
    table_1['home_team_goal'] = table_1['home_team_goal'] if 'home_team_goal' in table_1.columns else table_1[[c for c in ['home_goal','home_goals','home_team_goals','home_team_score','home_score'] if c in table_1.columns]].bfill(axis=1).iloc[:,0] if any(c in table_1.columns for c in ['home_goal','home_goals','home_team_goals','home_team_score','home_score']) else np.nan
    prepared = table_1[['country_id','season','home_team_goal','match_api_id','date','league_id','stage','home_team_api_id','away_team_api_id']].copy()
    prepared['date'] = pd.to_datetime(prepared['date'], errors='coerce')
    target = prepared[['country_id','season','home_team_goal','match_api_id','date','league_id','stage','home_team_api_id','away_team_api_id']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['country_id','name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_matches = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_leagues = prepared_table_2

# prepared_matches and prepared_leagues are the synthesized per-table outputs
integrated = prepared_matches.merge(prepared_leagues, on='country_id', how='inner')

# Filter for Poland by league name containing 'Poland' (or exact match depending on data), and the target season
poland_matches_2010 = integrated[(integrated['name'].str.contains('Poland', case=False, na=False)) & (integrated['season'] == '2010/2011')]

# Compute average home team goals
result = poland_matches_2010['home_team_goal'].mean()

answer = float(result) if pd.notnull(result) else None

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
