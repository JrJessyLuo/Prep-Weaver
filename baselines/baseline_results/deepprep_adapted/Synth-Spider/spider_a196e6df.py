import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="value", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # trim and collapse internal whitespace
    #     return re.sub(r'\s+', ' ', str(s)).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # trim and collapse internal whitespace
        return re.sub(r'\s+', ' ', str(s)).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["value"] = table_1["value"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'id', 'new_name': 'song_id'}])
    # Rename
    table_1 = table_1.rename(columns={'id': 'song_id'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['song_id', 'attribute', 'value'])
    # SelectCol
    _cols = [c for c in ['song_id', 'attribute', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
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
    # SelectCol(table_name="table_1", columns=['songs_id', 'participant_id', 'vsq'])
    # SelectCol
    _cols = [c for c in ['songs_id', 'participant_id', 'vsq'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['songs_id', 'participant_id', 'vsq'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['songs_id', 'participant_id', 'vsq'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['participant_id', 'songs_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['participant_id', 'songs_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
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
