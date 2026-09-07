import pandas as pd
import numpy as np

def _prep_1(table_1):
    import pandas as pd
    import numpy as np
    import html
    df = table_1.copy()
    df.columns = [str(c) for c in df.columns]
    id_col = 'author_id'
    candidate_cit_cols = [c for c in df.columns if c.lower() in ['total_citations','citations','totalcitation','total_citation','n_citations','num_citations','citation_count','cited_by','citedby']]
    cit_col = candidate_cit_cols[0] if len(candidate_cit_cols) > 0 else None
    glyph_cols = [c for c in df.columns if c != id_col and c != cit_col]
    long = df.melt(id_vars=[id_col] + ([cit_col] if cit_col is not None else []), value_vars=glyph_cols, var_name='pos', value_name='glyph')
    long['glyph'] = long['glyph'].replace(['nan','NaN','None',''], np.nan)
    long = long[long['glyph'].notna()].copy()
    long['pos_num'] = pd.to_numeric(long['pos'], errors='coerce')
    long = long.sort_values([id_col, 'pos_num', 'pos'])
    name_parts = long.groupby(id_col, as_index=False).agg(author_name=('glyph', lambda s: ''.join(s.astype(str).tolist())))
    name_parts['author_name'] = name_parts['author_name'].map(lambda x: html.unescape(x) if isinstance(x, str) else x)
    citations = df[[id_col]].drop_duplicates()
    citations['total_citations'] = np.nan
    citations = citations if cit_col is None else df.groupby(id_col, as_index=False).agg(total_citations=(cit_col, 'max'))
    target = pd.merge(citations, name_parts, on=id_col, how='inner')[['author_id','author_name','total_citations']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    author_row = df[df.iloc[:, 0].astype(str).str.strip().eq('author_id')].iloc[0:1]
    wide = author_row.drop(columns=author_row.columns[0])
    long = wide.T.reset_index()
    long.columns = ['paper_id', 'author_id']
    long['author_id'] = long['author_id'].replace({'nan': pd.NA, 'NaN': pd.NA, 'None': pd.NA, '': pd.NA})
    long = long.dropna(subset=['author_id'])
    long['author_id'] = long['author_id'].astype(str).str.strip()
    long = long[long['author_id'].ne('') & long['author_id'].ne('nan') & long['author_id'].ne('NaN')]
    target = long[['paper_id', 'author_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
authors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
paper_authors = prepared_table_2

# Join authorship mapping to author info
joined = paper_authors.merge(authors, on='author_id', how='inner')

# If authors.total_citations is already the per-author metric, just pick the max by that field
best = authors.loc[authors['total_citations'].astype('float64').idxmax(), ['author_name', 'total_citations']]
result = pd.DataFrame([{'author_name': best['author_name'], 'total_citations': best['total_citations']}])

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
