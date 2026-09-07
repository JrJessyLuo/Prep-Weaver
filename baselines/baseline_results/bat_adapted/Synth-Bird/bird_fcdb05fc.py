import pandas as pd
import numpy as np

def _prep_1(table_1):
    import numpy as np
    target = table_1.loc[:, ['id','superhero_name','gender_id','eye_colour_id','hair_colour_id','skin_colour_id','race_id','publisher_id','alignment_id','height_cm','weight_kg','first_name','last_name']].copy()
    target[['superhero_name','first_name','last_name']] = target[['superhero_name','first_name','last_name']].replace({'-': np.nan, '': np.nan}).apply(lambda s: s.astype('string').str.strip())
    target[['race_id','publisher_id','alignment_id']] = target[['race_id','publisher_id','alignment_id']].apply(lambda s: pd.to_numeric(s, errors='coerce').astype('Int64'))
    target[['id','gender_id','eye_colour_id','hair_colour_id','skin_colour_id']] = target[['id','gender_id','eye_colour_id','hair_colour_id','skin_colour_id']].apply(lambda s: pd.to_numeric(s, errors='coerce').astype('Int64'))
    target[['height_cm','weight_kg']] = target[['height_cm','weight_kg']].apply(lambda s: pd.to_numeric(s, errors='coerce'))
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import pandas as pd
    target = table_1.copy()
    target[['hero_id','aid','av']] = target[['hero_id','aid','av']].apply(pd.to_numeric, errors='coerce')
    target = target.dropna(subset=['hero_id','aid','av'])
    target = target.groupby(['hero_id','aid'], as_index=False).agg({'av':'max'})
    target = target[['hero_id','aid','av']].sort_values(['hero_id','aid']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    import ast
    df = table_1.copy()
    df['id'] = df['id'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df['attribute_name'] = df['attribute_name'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df = df.explode(['id','attribute_name']).reset_index(drop=True)
    target = df[['id','attribute_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.copy()
    target['gender'] = target['gender'].astype(str).str.strip()
    target['gender'] = target['gender'].replace({'N/A': pd.NA, 'NA': pd.NA, '': pd.NA, 'None': pd.NA, 'nan': pd.NA})
    target = target[['id','gender']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    target = table_1.loc[:, ['id', 'colour']].assign(colour=lambda d: d['colour'].astype('string').str.strip()).drop_duplicates(subset=['id']).sort_values('id').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_6(table_1):
    target = table_1.loc[:, ['id','race']].copy()
    target['race'] = target['race'].astype(str).str.strip()
    target = target[target['race'].notna() & (target['race'] != '') & (target['race'] != '-')].copy()
    target = target.drop_duplicates(subset=['id','race']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_7(table_1):
    target = table_1.copy()
    target['publisher_name'] = target['publisher_name'].astype('string').str.strip()
    target.loc[target['publisher_name'].eq(''), 'publisher_name'] = pd.NA
    target = target[['id','publisher_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_8(table_1):
    target = table_1.assign(alignment=table_1['alignment'].astype(str).str.strip()).loc[lambda d: d['alignment'].notna() & (d['alignment'] != '') & (~d['alignment'].str.upper().isin(['N/A','NA','NONE','NULL'])) , ['id','alignment']].drop_duplicates(subset=['id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_attribute_values = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_attribute_names = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
prepared_genders = prepared_table_4
prepared_table_5 = _prep_5(tables['table_5'])
prepared_colours = prepared_table_5
prepared_table_6 = _prep_6(tables['table_9'])
prepared_races = prepared_table_6
prepared_table_7 = _prep_7(tables['table_8'])
prepared_publishers = prepared_table_7
prepared_table_8 = _prep_8(tables['table_4'])
prepared_alignments = prepared_table_8

# Assume prepared_* DataFrames exist as per target schemas.

# 1) Normalize attribute names table (table_3 stores list-like strings in single row)
attr_row = prepared_attribute_names.iloc[0]
attr_ids = pd.Series(eval(attr_row['id']), name='id')
attr_names = pd.Series(eval(attr_row['attribute_name']), name='attribute_name')
attributes_long = pd.DataFrame({'id': attr_ids.astype(int), 'attribute_name': attr_names})

# 2) Select the hero row for 3-D Man
hero = prepared_heroes[prepared_heroes['superhero_name'] == '3-D Man']

# 3) Join scalar lookups
hero = hero.merge(prepared_genders.rename(columns={'id':'gender_id'}), on='gender_id', how='left') \
           .merge(prepared_colours.rename(columns={'id':'eye_colour_id','colour':'eye_colour'}), on='eye_colour_id', how='left') \
           .merge(prepared_colours.rename(columns={'id':'hair_colour_id','colour':'hair_colour'}), on='hair_colour_id', how='left') \
           .merge(prepared_colours.rename(columns={'id':'skin_colour_id','colour':'skin_colour'}), on='skin_colour_id', how='left') \
           .merge(prepared_races.rename(columns={'id':'race_id'}), on='race_id', how='left') \
           .merge(prepared_publishers.rename(columns={'id':'publisher_id'}), on='publisher_id', how='left') \
           .merge(prepared_alignments.rename(columns={'id':'alignment_id'}), on='alignment_id', how='left')

# 4) Gather power-stat attributes
hero_stats = prepared_attribute_values[prepared_attribute_values['hero_id'].isin(hero['id'])] \
    .merge(attributes_long.rename(columns={'id':'aid'}), on='aid', how='left')

# 5) Build attribute-name to value mapping rows
scalar_attrs = pd.melt(
    hero[['superhero_name','gender','eye_colour','hair_colour','skin_colour','race','publisher_name','alignment','height_cm','weight_kg','first_name','last_name']],
    id_vars=['superhero_name'],
    var_name='attribute_name',
    value_name='value'
)

stat_attrs = hero_stats[['attribute_name','av']].rename(columns={'av':'value'})
stat_attrs['superhero_name'] = '3-D Man'

all_attrs = pd.concat([scalar_attrs[['superhero_name','attribute_name','value']], stat_attrs[['superhero_name','attribute_name','value']]], ignore_index=True)

# 6) Final selection for answer: all attribute names and their values for 3-D Man
answer = all_attrs[all_attrs['superhero_name'] == '3-D Man'][['attribute_name','value']]

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
