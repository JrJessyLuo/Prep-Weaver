import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['id','original_artist','name','language','english_translation']].copy()
    df['original_artist'] = df['original_artist'].astype(str).str.strip()
    df['name'] = df['name'].astype(str).str.strip()
    df['language'] = df['language'].astype(str).str.strip()
    df['english_translation'] = df['english_translation'].astype(str).str.strip()
    target = df[['id','original_artist','name','language','english_translation']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['participant_id','voice_sound_quality','rhythm_tempo','stage_presence']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
songs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
performance_metrics = prepared_table_2

target = songs.merge(performance_metrics, left_on='id', right_on='participant_id', how='inner')
filtered = target[target['rhythm_tempo'] > 5]
# If multiple metric rows per song exist, keep the best voice_sound_quality per artist/song
best = (filtered.sort_values('voice_sound_quality', ascending=False)
               .drop_duplicates(subset=['id']))
result = best[['original_artist', 'voice_sound_quality']].sort_values('voice_sound_quality', ascending=False)

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
