import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'GPT']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'GPT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['ID','SEX']].copy()
    df['SEX'] = df['SEX'].replace({'nan': pd.NA, 'None': pd.NA, '-': pd.NA})
    target = df.groupby('ID', as_index=False).agg({'SEX':'first'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_labs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_demographics = prepared_table_2

# prepared_labs and prepared_demographics are assumed to be materialized per the targets above
# Join labs with demographics on patient ID
joined = prepared_labs.merge(prepared_demographics, on='ID', how='inner')

# Determine normal GPT values. If a reference range is available elsewhere, plug it in.
# As a pragmatic default (common adult ref range), treat 7 <= GPT <= 56 U/L as normal.
# Adjust if domain metadata provides a different range.
normal_mask = joined['GPT'].notna() & (joined['GPT'] >= 7) & (joined['GPT'] <= 56)
normal_patients = joined.loc[normal_mask, ['ID', 'SEX']]

# Count unique patients with normal GPT that are male (SEX == 'M')
answer = normal_patients.loc[normal_patients['SEX'] == 'M', 'ID'].nunique()

result = pd.DataFrame({'male_with_normal_GPT_count': [int(answer)]})

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
