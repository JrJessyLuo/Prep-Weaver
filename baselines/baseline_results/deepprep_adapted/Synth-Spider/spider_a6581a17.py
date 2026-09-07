import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['author_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['author_id'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="author_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove repeated double quotes like ""0""
    #     if s.startswith('""') and s.endswith('""') and len(s) >= 4:
    #         s = s[2:-2]
    #     # remove single wrapping quotes if any
    #     if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove repeated double quotes like ""0""
        if s.startswith('""') and s.endswith('""') and len(s) >= 4:
            s = s[2:-2]
        # remove single wrapping quotes if any
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["author_id"] = table_1["author_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name", func="""
    # def transform_func(s):
    #     import html, re
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ['nan', 'none', 'null', '']:
    #         return None
    #     # decode HTML entities like &#269; or &#x106;
    #     s = html.unescape(s)
    #     # collapse whitespace
    #     s = re.sub(r'\s+', ' ', s).strip()
    #     return s if s != '' else None
    # """)
    # StandardizeString
    def transform_func(s):
        import html, re
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ['nan', 'none', 'null', '']:
            return None
        # decode HTML entities like &#269; or &#x106;
        s = html.unescape(s)
        # collapse whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        return s if s != '' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name"] = table_1["name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="name_final", func="""
    # def compute(row):
    #     name = row.get('name')
    #     if name is None:
    #         return row.get('author_id')
    #     # if pandas carries NaN as float, guard via string check
    #     try:
    #         if str(name).strip().lower() == 'nan' or str(name).strip() == '':
    #             return row.get('author_id')
    #     except Exception:
    #         return row.get('author_id')
    #     return name
    # """)
    # AddNewColumn
    def compute(row):
        name = row.get('name')
        if name is None:
            return row.get('author_id')
        # if pandas carries NaN as float, guard via string check
        try:
            if str(name).strip().lower() == 'nan' or str(name).strip() == '':
                return row.get('author_id')
        except Exception:
            return row.get('author_id')
        return name
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["name_final"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['name', 'email'])
    # DropColumn
    table_1 = table_1.drop(columns=['name', 'email'], errors='ignore')

    # ---------------- Step 6 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'name_final', 'new_name': 'name'}])
    # Rename
    table_1 = table_1.rename(columns={'name_final': 'name'})

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['author_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['author_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['author_id', 'name'])
    # SelectCol
    _cols = [c for c in ['author_id', 'name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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
    # Deduplicate(table_name="table_1", subset=['paper_id', 'author_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['paper_id', 'author_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['paper_id', 'author_id'])
    # SelectCol
    _cols = [c for c in ['paper_id', 'author_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['paper_id', 'author_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['paper_id', 'author_id'], how='any').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="cited_paper_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return s.strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return s.strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["cited_paper_id"] = table_1["cited_paper_id"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="paper_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes and normalize whitespace
    #     return s.strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # remove surrounding quotes and normalize whitespace
        return s.strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["paper_id"] = table_1["paper_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Explode(table_name="table_1", column="paper_id", split_comma=True)
    # Explode
    _ex_cols = 'paper_id' if isinstance('paper_id', list) else ['paper_id']
    if all(_c in table_1.columns for _c in _ex_cols):
        try:
            for _col in _ex_cols:
                _nn = table_1[_col].dropna()
                _sample = _nn.iloc[0] if not _nn.empty else None
                if isinstance(_sample, str) or (pd.isna(_sample) and True):
                    if True:
                        table_1[_col] = table_1[_col].apply(lambda x: [i.strip() for i in str(x).split(',')] if pd.notna(x) and x != '' else [])
                    else:
                        def _ex_parse(x):
                            if pd.isna(x) or x == '':
                                return []
                            try:
                                _r = ast.literal_eval(str(x))
                                return _r if isinstance(_r, list) else [_r]
                            except Exception:
                                return [i.strip() for i in str(x).split()]
                        table_1[_col] = table_1[_col].apply(_ex_parse)
                elif not isinstance(_sample, list) and _sample is not None:
                    table_1[_col] = table_1[_col].apply(lambda x: [x] if pd.notna(x) else [])
            if len(_ex_cols) == 1:
                table_1 = table_1.explode(_ex_cols[0]).reset_index(drop=True)
            else:
                table_1 = table_1.explode(_ex_cols).reset_index(drop=True)
        except Exception:
            pass

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="paper_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # after splitting, trim each item
    #     return s.strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # after splitting, trim each item
        return s.strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["paper_id"] = table_1["paper_id"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['cited_paper_id'])
    # SelectCol
    _cols = [c for c in ['cited_paper_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
