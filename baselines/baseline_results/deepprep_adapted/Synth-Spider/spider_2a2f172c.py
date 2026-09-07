import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name", func="""
    # import html
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s)
    #     if s.lower().strip() == 'nan':
    #         return None
    #     # decode HTML entities like &#269;
    #     return html.unescape(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s)
        if s.lower().strip() == 'nan':
            return None
        # decode HTML entities like &#269;
        return html.unescape(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name"] = table_1["name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="author_id", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() == 'nan' or s == '':
    #         return None
    #     # remove wrapping quotes like '""0""' -> '0' (also handles '"0"' etc.)
    #     s = s.replace('"', '').replace("'", "").strip()
    #     # keep only the first integer-like token if present
    #     m = re.search(r'-?\d+', s)
    #     return m.group(0) if m else (s if s != '' else None)
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() == 'nan' or s == '':
            return None
        # remove wrapping quotes like '""0""' -> '0' (also handles '"0"' etc.)
        s = s.replace('"', '').replace("'", "").strip()
        # keep only the first integer-like token if present
        m = re.search(r'-?\d+', s)
        return m.group(0) if m else (s if s != '' else None)
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
    # DropNulls(table_name="table_1", subset=['author_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['author_id'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['author_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['author_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['email'])
    # DropColumn
    table_1 = table_1.drop(columns=['email'], errors='ignore')

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['author_id', 'name'])
    # SelectCol
    _cols = [c for c in ['author_id', 'name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
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
    # ErrorDetection(table_name="table_1", column_name="paper_author_combined", func="""
    # import re
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip().strip('"').strip("'")
    #     return bool(re.match(r'^.+\|.+$', s))
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip().strip('"').strip("'")
        return bool(re.match(r'^.+\|.+$', s))
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['paper_author_combined'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="paper_author_combined", target_columns=['paper_id', 'author_id'], func="""
    # def split(val):
    #     if val is None:
    #         return {"paper_id": None, "author_id": None}
    #     s = str(val).strip()
    #     # strip matching surrounding quotes
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     parts = s.split('|', 1)
    #     paper_id = parts[0].strip() if len(parts) > 0 else None
    #     author_id = parts[1].strip() if len(parts) > 1 else None
    #     return {"paper_id": paper_id, "author_id": author_id}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"paper_id": None, "author_id": None}
        s = str(val).strip()
        # strip matching surrounding quotes
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        parts = s.split('|', 1)
        paper_id = parts[0].strip() if len(parts) > 0 else None
        author_id = parts[1].strip() if len(parts) > 1 else None
        return {"paper_id": paper_id, "author_id": author_id}
    for _c in ['paper_id', 'author_id']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['paper_author_combined']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['paper_id', 'author_id']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['paper_author_combined'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['paper_id', 'author_id'])
    # SelectCol
    _cols = [c for c in ['paper_id', 'author_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # ErrorDetection(table_name="table_1", column_name="year", func="""
    # import re
    # def is_valid_year(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip().strip('"')
    #     return re.fullmatch(r'\d{4}', s) is not None
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_year(val):
        if val is None:
            return False
        s = str(val).strip().strip('"')
        return re.fullmatch(r'\d{4}', s) is not None
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_year(val))
        except Exception:
            return False
    table_1 = table_1[table_1['year'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="year", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     # remove surrounding quotes repeatedly and trim
    #     t = str(s).strip()
    #     while len(t) >= 2 and ((t[0] == '"' and t[-1] == '"') or (t[0] == "'" and t[-1] == "'")):
    #         t = t[1:-1].strip()
    #     return t
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        # remove surrounding quotes repeatedly and trim
        t = str(s).strip()
        while len(t) >= 2 and ((t[0] == '"' and t[-1] == '"') or (t[0] == "'" and t[-1] == "'")):
            t = t[1:-1].strip()
        return t
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["year"] = table_1["year"].apply(_std_apply)

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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row['year'] == 2009
    # """)
    # Filter
    def filter_func(row):
        return row['year'] == 2009
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['paper_id', 'year'])
    # SelectCol
    _cols = [c for c in ['paper_id', 'year'] if c in table_1.columns]
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
