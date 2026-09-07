import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['author_id','paper_id']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['author_id','name_email_combined']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_authorships = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_authors = prepared_table_2

# Join prepared tables on author_id
joined = prepared_authorships.merge(prepared_authors, on='author_id', how='left')

# Parse name from name_email_combined (format assumed: 'name|||email')
# If missing or malformed, use empty string for name
name_series = joined['name_email_combined'].fillna('').astype(str).str.split('|||').str[0].fillna('')
joined = joined.assign(author_name=name_series)

# Count distinct papers per author
paper_counts = joined[['author_id', 'author_name', 'paper_id']].dropna(subset=['paper_id']).drop_duplicates().groupby(['author_id', 'author_name'], as_index=False).agg(paper_count=('paper_id', 'nunique'))

# Filter authors with more than 50 papers and return their names
result = paper_counts.loc[paper_counts['paper_count'] > 50, ['author_name']].dropna().drop_duplicates().sort_values('author_name')

target = result['author_name'].tolist()

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
