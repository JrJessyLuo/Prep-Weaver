import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['affiliation_id','name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df = df[df['affiliation_id'].notna()]
    df['affiliation_id'] = df['affiliation_id'].astype('int64').astype('string')
    df[['paper_id','author_id']] = df['paper_author_combined'].astype('string').str.split('\|\|', n=1, expand=True)
    target = df[['affiliation_id','paper_id','author_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    parts = table_1['paper_info'].str.split('|', expand=True)
    target = table_1.assign(paper_id=parts[0], venue=parts[1], year=parts[2].astype(int))[['paper_id','venue','year','title']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
affiliations = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
paper_author_affiliations = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
papers = prepared_table_3

# Assume prepared tables exist: affiliations, paper_author_affiliations, papers
# Ensure types align
paper_author_affiliations['affiliation_id'] = paper_author_affiliations['affiliation_id'].astype(str)
affiliations['affiliation_id'] = affiliations['affiliation_id'].astype(str)

# Join author-affiliation links to papers to get year
paa_papers = paper_author_affiliations.merge(papers[['paper_id','year']], on='paper_id', how='inner')

# Filter to 2009
paa_2009 = paa_papers[paa_papers['year'] == 2009]

# Count distinct papers per affiliation (avoid multiple authors from same affiliation on same paper inflating counts)
counts = paa_2009.dropna(subset=['affiliation_id']).drop_duplicates(subset=['paper_id','affiliation_id']).groupby('affiliation_id').size().reset_index(name='paper_count')

# Bring affiliation names
counts = counts.merge(affiliations[['affiliation_id','name']], on='affiliation_id', how='left')

# Top 3 by paper_count
target = counts.sort_values(['paper_count','name'], ascending=[False, True]).head(3)

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
