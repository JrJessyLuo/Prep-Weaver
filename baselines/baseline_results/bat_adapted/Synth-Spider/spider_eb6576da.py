import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['author_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    target = df[['pid', 'title', 'conf', 'year']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
authors_papers_wide = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
papers = prepared_table_2

# prepared inputs assumed: authors_papers_wide (columns: author_id plus many paper ID columns), papers (pid,title,conf,year)

# 1) Unpivot the wide author-paper matrix to long form (author_id, pid)
apw = authors_papers_wide.copy()
value_cols = [c for c in apw.columns if c != 'author_id']
long_links = apw.melt(id_vars=['author_id'], value_vars=value_cols, var_name='pid', value_name='has_authorship')
# Many wide matrices encode authorship with non-null/non-empty markers. Keep rows that indicate authorship.
long_links = long_links[long_links['has_authorship'].notna()]

# 2) Normalize pid column names that may be quoted as strings (e.g., '"A00-1001"'). Remove surrounding quotes if present.
long_links['pid'] = long_links['pid'].astype(str).str.strip('"')

# 3) Join with papers to get year, then filter to 2009
links_2009 = long_links.merge(papers[['pid','year']], on='pid', how='inner')
links_2009 = links_2009[links_2009['year'].astype(int) == 2009]

# 4) Count papers per author and select the author with the maximum count
counts = links_2009.groupby('author_id', as_index=False).size().rename(columns={'size':'paper_count'})
if len(counts) == 0:
    target = pd.DataFrame(columns=['author_id','paper_count']).head(0)
else:
    max_count = counts['paper_count'].max()
    target = counts[counts['paper_count'] == max_count].sort_values(['paper_count','author_id'], ascending=[False, True]).head(1)

# target contains the author_id with the most papers in 2009 and their count

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
