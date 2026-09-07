import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="author_id", mode="mode")
    # MissingValueImputation
    table_1["author_id"] = table_1["author_id"].fillna(table_1["author_id"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['affiliation_id'])
    # DropColumn
    table_1 = table_1.drop(columns=['affiliation_id'], errors='ignore')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['author_id', 'paper_id'])
    # SelectCol
    _cols = [c for c in ['author_id', 'paper_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['author_id', 'paper_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['author_id', 'paper_id'], keep='first').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['author_id', 'name_email_combined'])
    # SelectCol
    _cols = [c for c in ['author_id', 'name_email_combined'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="author_id", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove repeated quotes like ""0"" -> 0
    #     s = s.replace('""', '"')
    #     s = s.strip('"')
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove repeated quotes like ""0"" -> 0
        s = s.replace('""', '"')
        s = s.strip('"')
        return s
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
    # CastType(table_name="table_1", column="author_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['author_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['author_id']
    if _dtype == "datetime64":
        table_1['author_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['author_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['author_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['author_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['author_id', 'name_email_combined'])
    # SelectCol
    _cols = [c for c in ['author_id', 'name_email_combined'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_authorships = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_authors = prepared_table_2

# Join prepared tables on author_id
joined = prepared_authorships.merge(prepared_authors, on='author_id', how='left')

# Parse name from name_email_combined (format assumed: 'name|||email')
# If missing or malformed, use empty string for name
name_series = joined['name_email_combined'].fillna('').astype(str).str.split('|||').str[0].fillna('')
joined = joined.assign(author_name=name_series)

# Count distinct papers per author
paper_counts = joined[['author_id', 'author_name', 'paper_id']].dropna(subset=['paper_id']).drop_duplicates().groupby(['author_id', 'author_name'], as_index=False).agg(paper_count=('paper_id', 'nunique'))

# Filter authors with more than 50 papers and return their names
result = paper_counts.loc[paper_counts['paper_count'] > 50, ['author_name']].dropna().drop_duplicates().sort_values('author_name')

target = result['author_name'].tolist()

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
