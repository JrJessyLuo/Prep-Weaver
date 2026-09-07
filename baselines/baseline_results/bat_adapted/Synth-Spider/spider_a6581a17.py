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
    target = table_1[['paper_id','author_id']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['paper_id'] = df['paper_id'].fillna('')
    df['paper_id_list'] = df['paper_id'].astype(str).str.split(',')
    df = df.explode('paper_id_list')
    df['paper_id_list'] = df['paper_id_list'].astype(str).str.strip()
    df = df[df['paper_id_list'].ne('')]
    target = df[['cited_paper_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
authors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
authorship = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
paper_citations_expanded = prepared_table_3

# Assume prepared tables are provided as dataframes: authors, authorship, paper_citations_expanded
# 1) Count citations per paper from the expanded citations table
paper_cite_counts = paper_citations_expanded.groupby('cited_paper_id').size().reset_index(name='paper_citations')

# 2) Map paper citation counts to authors via authorship (papers -> authors)
author_paper_cites = authorship.merge(paper_cite_counts, left_on='paper_id', right_on='cited_paper_id', how='left')
author_paper_cites['paper_citations'] = author_paper_cites['paper_citations'].fillna(0)

# 3) Aggregate to citations per author (sum of citations of their papers)
author_cites = author_paper_cites.groupby('author_id', as_index=False)['paper_citations'].sum()

# 4) Attach author names
author_cites_named = author_cites.merge(authors[['author_id','name']], on='author_id', how='left')

# 5) Select author with maximum citations
idx = author_cites_named['paper_citations'].idxmax()
result = author_cites_named.loc[[idx], ['name','paper_citations']]
result.rename(columns={'paper_citations':'citations'}, inplace=True)

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
