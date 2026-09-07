import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['participant_id', 'voice_sound_quality', 'rhythm_tempo', 'stage_presence'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['participant_id', 'voice_sound_quality', 'rhythm_tempo', 'stage_presence'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['participant_id', 'voice_sound_quality', 'rhythm_tempo', 'stage_presence'])
    # SelectCol
    _cols = [c for c in ['participant_id', 'voice_sound_quality', 'rhythm_tempo', 'stage_presence'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
