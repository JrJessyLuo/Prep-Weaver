import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[table_1['aff_id'].notna(), ['paper_id', 'aff_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    filtered = table_1.loc[table_1['attribute'].eq('name'), ['affiliation_id', 'value']]
    filtered = filtered.rename(columns={'value': 'name'})
    target = filtered.groupby('affiliation_id', as_index=False)['name'].first()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
papers_affiliations = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
affiliation_metadata = prepared_table_2

# Prepared tables assumed available: papers_affiliations, affiliation_metadata
# Clean types and drop missing affiliations
pa = papers_affiliations.copy()
pa = pa[pa['aff_id'].notna()]
# Ensure integer-compatible join keys
pa['aff_id'] = pa['aff_id'].astype('int64')
aff = affiliation_metadata.copy()
aff['affiliation_id'] = aff['affiliation_id'].astype('int64')

# Join affiliations to get names
merged = pa.merge(aff, left_on='aff_id', right_on='affiliation_id', how='inner')

# Count distinct papers per affiliation (use nunique to avoid double-counting same paper multiple rows)
result = (
    merged.groupby(['aff_id', 'name'])['paper_id']
    .nunique()
    .reset_index(name='total_papers')
)

# Sort optionally by descending count and name
result = result.sort_values(['total_papers', 'name'], ascending=[False, True]).reset_index(drop=True)

target = result

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
