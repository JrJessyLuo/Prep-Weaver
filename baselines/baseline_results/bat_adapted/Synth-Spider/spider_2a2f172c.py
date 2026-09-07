import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['author_id', 'name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    split_cols = table_1['paper_author_combined'].astype(str).str.split('|', n=1, expand=True)
    target = split_cols.rename(columns={0: 'paper_id', 1: 'author_id'})[['paper_id', 'author_id']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['paper_id','year']].copy()
    df['year'] = df['year'].astype(str).str.strip().str.strip('"').str.strip("'")
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    target = df[['paper_id','year']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
authors_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
paper_authors_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
papers_prepared = prepared_table_3

# Assume prepped dataframes: authors_prepared, paper_authors_prepared, papers_prepared
# Ensure types are consistent (author_id often string-like numbers; year numeric)
authors_prepared['author_id'] = authors_prepared['author_id'].astype(str).str.strip().str.replace('"','', regex=False)
paper_authors_prepared['author_id'] = paper_authors_prepared['author_id'].astype(str).str.strip().str.replace('"','', regex=False)
paper_authors_prepared['paper_id'] = paper_authors_prepared['paper_id'].astype(str).str.strip()
papers_prepared['paper_id'] = papers_prepared['paper_id'].astype(str).str.strip()
papers_prepared['year'] = pd.to_numeric(papers_prepared['year'].astype(str).str.replace('"','', regex=False), errors='coerce')

# Join paper-author links to papers to filter by year 2009
pa_2009 = paper_authors_prepared.merge(papers_prepared[['paper_id','year']], on='paper_id', how='inner')
pa_2009 = pa_2009[pa_2009['year'] == 2009]

# Count papers per author in 2009
author_counts = pa_2009.groupby('author_id', as_index=False).size().rename(columns={'size':'paper_count'})

# Get the author_id with max papers
if not author_counts.empty:
    top_author_id = author_counts.sort_values(['paper_count','author_id'], ascending=[False, True]).iloc[0]['author_id']
    # Attach name
    top_author = authors_prepared.merge(author_counts, on='author_id', how='right')
    top_row = top_author[top_author['author_id'] == top_author_id].iloc[0]
    answer_name = top_row['name']
else:
    answer_name = None

result = pd.DataFrame({"author_name": [answer_name]})

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
