import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="name_email_combined", func="""
    # import pandas as pd
    # def is_valid(val):
    #     if val is None or (isinstance(val, float) and pd.isna(val)):
    #         return False
    #     s = str(val)
    #     # expect at least a 'name|email' pattern (even if email may be nan)
    #     return '|' in s
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return False
        s = str(val)
        # expect at least a 'name|email' pattern (even if email may be nan)
        return '|' in s
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['name_email_combined'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="name_email_combined", func="""
    # import re
    # import html
    # 
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     # Decode HTML entities like &#269; or &#x106; (semicolon may be missing in data)
    #     # Add missing semicolons to numeric entities where needed
    #     s = re.sub(r'&#(x?[0-9A-Fa-f]+)(?!;)', r'&#\1;', s)
    #     s = html.unescape(s)
    #     return s
    # """)
    # StandardizeString

    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip().strip('"').strip("'")
        # Decode HTML entities like &#269; or &#x106; (semicolon may be missing in data)
        # Add missing semicolons to numeric entities where needed
        s = re.sub(r'&#(x?[0-9A-Fa-f]+)(?!;)', r'&#\1;', s)
        s = html.unescape(s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["name_email_combined"] = table_1["name_email_combined"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="name_email_combined", target_columns=['author_name'], func="""
    # import pandas as pd
    # 
    # def split(val):
    #     if val is None or (isinstance(val, float) and pd.isna(val)):
    #         return {"author_name": None}
    #     s = str(val)
    #     name_part = s.split('|', 1)[0].strip()
    #     # Treat 'nan' (any casing) as missing name
    #     if name_part.lower() == 'nan' or name_part == '':
    #         return {"author_name": None}
    #     return {"author_name": name_part}
    # """)
    # SplitColumn

    def split(val):
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return {"author_name": None}
        s = str(val)
        name_part = s.split('|', 1)[0].strip()
        # Treat 'nan' (any casing) as missing name
        if name_part.lower() == 'nan' or name_part == '':
            return {"author_name": None}
        return {"author_name": name_part}
    for _c in ['author_name']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['name_email_combined']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['author_name']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['name_email_combined'])

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['author_id', 'author_name'])
    # SelectCol
    _cols = [c for c in ['author_id', 'author_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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
    # SelectCol(table_name="table_1", columns=['paper_id', 'aid', 'afid'])
    # SelectCol
    _cols = [c for c in ['paper_id', 'aid', 'afid'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['paper_id', 'aid'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['paper_id', 'aid'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'aid', 'new_name': 'author_id'}])
    # Rename
    table_1 = table_1.rename(columns={'aid': 'author_id'})

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['afid'])
    # DropColumn
    table_1 = table_1.drop(columns=['afid'], errors='ignore')

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['paper_id', 'author_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['paper_id', 'author_id'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="paper_long", func="""
    # import pandas as pd
    # def process_tables(table_1: pd.DataFrame):
    #     # Alternative: treat first column values as index then transpose
    #     key_col = table_1.columns[0]
    #     df = table_1.set_index(key_col).T.reset_index().rename(columns={"index": "paper_id"})
    #     # Ensure venue exists
    #     if "venue" in df.columns:
    #         return df[["paper_id", "venue"]]
    #     # If venue field is missing, still return paper_id for later integration
    #     return df[["paper_id"]]
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame):
        # Alternative: treat first column values as index then transpose
        key_col = table_1.columns[0]
        df = table_1.set_index(key_col).T.reset_index().rename(columns={"index": "paper_id"})
        # Ensure venue exists
        if "venue" in df.columns:
            return df[["paper_id", "venue"]]
        # If venue field is missing, still return paper_id for later integration
        return df[["paper_id"]]
    paper_long = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="paper_long", columns=['paper_id', 'venue'])
    # SelectCol
    _cols = [c for c in ['paper_id', 'venue'] if c in paper_long.columns]
    paper_long = paper_long[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="paper_long", subset=['paper_id'], keep="first")
    # Deduplicate
    paper_long = paper_long.drop_duplicates(subset=['paper_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['paper_long'])
    # Terminate
    result = {'paper_long': paper_long}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
