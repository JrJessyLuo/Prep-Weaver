import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Count(table_name="table_1")
    # Count -> statistic_table
    _stat_row = pd.DataFrame({'operator': ['Count(table_name="table_1")'], 'statistic_name': ['count'], 'value': [len(table_1)]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['author_id'])
    # SelectCol
    _cols = [c for c in ['author_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # StandardizeString(table_name="table_1", column_name="conf", func="""
    # def transform_func(s: str):
    #     return s.strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        return s.strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["conf"] = table_1["conf"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['pid', 'title', 'conf', 'year'])
    # SelectCol
    _cols = [c for c in ['pid', 'title', 'conf', 'year'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="year", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['year'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['year']
    if _dtype == "datetime64":
        table_1['year'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['year'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['year'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['year'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['pid', 'year'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['pid', 'year'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['pid'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['pid'], keep='first').reset_index(drop=True)

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
