import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="isStorySpotlight", mode="mode")
    # MissingValueImputation
    table_1["isStorySpotlight"] = table_1["isStorySpotlight"].fillna(table_1["isStorySpotlight"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'isStorySpotlight'])
    # SelectCol
    _cols = [c for c in ['id', 'isStorySpotlight'] if c in table_1.columns]
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
    # Deduplicate(table_name="table_1", subset=['id', 'language_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id', 'language_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['id', 'language_name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['id', 'language_name'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'language_name'])
    # SelectCol
    _cols = [c for c in ['id', 'language_name'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_localizations = prepared_table_2

# prepared_cards and prepared_localizations are synthesized from table_1 and table_2 respectively
merged = prepared_cards.merge(prepared_localizations, on='id', how='left')
# Keep only Story Spotlight cards
spotlight = merged[merged['isStorySpotlight'] == 1]
# Determine French localizations; language_name formatted like 'French|Name'
is_french = spotlight['language_name'].fillna('').str.startswith('French|')
num_spotlight = spotlight['id'].nunique()
num_french_spotlight = spotlight.loc[is_french, 'id'].nunique()
percentage = (num_french_spotlight / num_spotlight * 100.0) if num_spotlight > 0 else 0.0
result = pd.DataFrame({
    'percentage_french_story_spotlight': [percentage],
    'count_french_story_spotlight': [num_french_spotlight],
    'count_story_spotlight_total': [num_spotlight]
})
answer = result

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
