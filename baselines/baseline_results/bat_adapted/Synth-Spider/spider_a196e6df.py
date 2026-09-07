import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.rename(columns={'id':'song_id'})[['song_id','attribute','value']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['songs_id','participant_id','vsq']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
songs_attributes_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
song_scores_prepared = prepared_table_2

# Assume prepared tables are provided as DataFrames: songs_attributes_prepared, song_scores_prepared

# 1) Identify the song_id(s) for the song named ' The Balkan Girls ' with English language
# Normalize whitespace for robust matching while preserving original value filtering intent
attrs = songs_attributes_prepared.copy()
attrs['value_norm'] = attrs['value'].astype(str).str.strip()

# song ids where name matches exactly ' The Balkan Girls '
name_ids = set(attrs[(attrs['attribute'] == 'name') & (attrs['value'] == " The Balkan Girls ")]['song_id'].unique())

# song ids where language contains English (case-insensitive, comma-separated allowed)
language_mask = (attrs['attribute'] == 'language') & (attrs['value'].str.contains(r'(?i)\bEnglish\b'))
lang_ids = set(attrs[language_mask]['song_id'].unique())

# intersection: songs that satisfy both name and English language
target_song_ids = name_ids.intersection(lang_ids)

# 2) Filter scores to those song ids and select vsq
scores = song_scores_prepared[song_scores_prepared['songs_id'].isin(list(target_song_ids))][['songs_id','participant_id','vsq']].copy()

# 3) The requested output is the voice sound quality scores; return as a DataFrame (one row per participant score)
answer = scores.sort_values(['songs_id','participant_id']).reset_index(drop=True)

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
