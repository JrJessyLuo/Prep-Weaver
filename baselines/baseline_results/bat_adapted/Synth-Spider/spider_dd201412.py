import pandas as pd
import numpy as np

def _prep_1(table_1):
    import pandas as pd
    import numpy as np
    import html
    df = table_1.copy()
    df['author_name'] = df['name_email_combined'].astype('string').str.split('|', n=1, expand=True)[0]
    df['author_name'] = df['author_name'].astype('string').str.strip()
    df['author_name'] = df['author_name'].replace({'nan': pd.NA, '': pd.NA, '<NA>': pd.NA})
    df['author_name'] = df['author_name'].apply(lambda x: pd.NA if pd.isna(x) else html.unescape(str(x)).strip())
    target = df[['author_id', 'author_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.rename(columns={'aid':'author_id'})[['paper_id','author_id']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.set_index('paper_id').T.reset_index().rename(columns={'index':'paper_id'})
    target = df[['paper_id','venue']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_authors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_authorship = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_papers = prepared_table_3

# prepared_authors: expects columns ['author_id','author_name'] with clean names
# prepared_authorship: expects columns ['paper_id','author_id']
# prepared_papers: expects columns ['paper_id','venue']

# Join authorship to papers to find ACL publications
auth_papers = prepared_authorship.merge(prepared_papers, on='paper_id', how='left')
acl_authors = auth_papers.loc[auth_papers['venue'].astype(str).str.upper()=='ACL', ['author_id']].dropna().drop_duplicates()

# All authors
all_authors = prepared_authors[['author_id','author_name']].drop_duplicates()

# Anti-join: authors with no ACL publications
result = all_authors.merge(acl_authors.assign(in_acl=True), on='author_id', how='left')
never_acl = result[result['in_acl'].isna()][['author_name']]

answer = never_acl.dropna().drop_duplicates().reset_index(drop=True)

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
