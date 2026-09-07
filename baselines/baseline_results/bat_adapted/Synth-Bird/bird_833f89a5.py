import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['circuitId','circuitRef','name','guojia']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['year', 'url']].copy()
    target['year'] = pd.to_numeric(target['year'], errors='coerce')
    target['url'] = target['url'].astype('string').str.strip()
    target = target.dropna(subset=['year', 'url'])
    target = target[target['url'].ne('') & target['url'].str.match(r'^https?://', na=False)]
    target['year'] = target['year'].astype('int64')
    target = target.sort_values(['year', 'url']).drop_duplicates(subset=['year'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[table_1['attribute'].isin(['year','circuitId']), ['raceId','attribute','value']].copy()
    target['value'] = target['value'].astype(str).str.strip()
    target = target.dropna(subset=['raceId','attribute','value']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
circuits_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_12'])
seasons_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
races_long_prepared = prepared_table_3

# Start from prepared tables
circuits = circuits_prepared.copy()
seasons = seasons_prepared.copy()
races_long = races_long_prepared.copy()

# Pivot races_long to wide to expose 'year' and 'circuitId' as columns
races_wide = races_long.pivot_table(index='raceId', columns='attribute', values='value', aggfunc='first').reset_index()

# Ensure correct dtypes for join keys
if 'year' in races_wide.columns:
    races_wide['year'] = pd.to_numeric(races_wide['year'], errors='coerce')
if 'circuitId' in races_wide.columns:
    races_wide['circuitId'] = pd.to_numeric(races_wide['circuitId'], errors='coerce')

# Normalize circuit identification for Brands Hatch
circuits['name_l'] = circuits['name'].str.lower()
circuits['circuitRef_l'] = circuits['circuitRef'].str.lower()

brands_mask = circuits['name_l'].str.contains('brands hatch', na=False) | (circuits['circuitRef_l'] == 'brands_hatch') | (circuits['circuitRef_l'] == 'brandshatch') | (circuits['circuitRef_l'] == 'brands-hatch')
brands_circuits = circuits.loc[brands_mask, ['circuitId', 'name', 'circuitRef', 'guojia']].drop_duplicates()

# Join races to Brands Hatch circuits by circuitId
races_at_brands = races_wide.merge(brands_circuits, on='circuitId', how='inner')

# Join to seasons to validate the season exists and get URL evidence
races_at_brands = races_at_brands.merge(seasons, on='year', how='left')

# Find the last season year when Brands Hatch hosted the British GP
# If a 'name' or 'url' attribute of the race existed indicating 'British Grand Prix', we could filter further,
# but with available tables we assume any race at Brands Hatch corresponds to the British GP when applicable.
last_year = races_at_brands['year'].max()

# Prepare final result
answer = {
    'last_brands_hatch_british_gp_season': int(last_year) if pd.notnull(last_year) else None,
    'season_url': races_at_brands.loc[races_at_brands['year'] == last_year, 'url'].dropna().unique().tolist() if pd.notnull(last_year) else []
}

target = pd.DataFrame([answer])

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
