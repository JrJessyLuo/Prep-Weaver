import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['address'])
    # DropColumn
    table_1 = table_1.drop(columns=['address'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="affiliation_id", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes including doubled quotes like ""0""
    #     s = re.sub(r'^(?:"")+|(?:"")+$', '', s)   # strip leading/trailing double-quotes
    #     s = re.sub(r'^"+|"+$', '', s)             # strip any remaining quotes
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes including doubled quotes like ""0""
        s = re.sub(r'^(?:"")+|(?:"")+$', '', s)   # strip leading/trailing double-quotes
        s = re.sub(r'^"+|"+$', '', s)             # strip any remaining quotes
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["affiliation_id"] = table_1["affiliation_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['affiliation_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['affiliation_id'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     v = row.get(\"affiliation_id\")
    #     if v is None:
    #         return False
    #     s = str(v).strip()
    #     return s != \"\" and s.lower() != \"nan\"
    # """)
    # Filter
    def filter_func(row):
        v = row.get(\"affiliation_id\")
        if v is None:
            return False
        s = str(v).strip()
        return s != \"\" and s.lower() != \"nan\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="paper_author_combined", target_columns=['paper_id', 'author_id'], func="""
    # def split(val):
    #     if val is None:
    #         return {"paper_id": None, "author_id": None}
    #     s = str(val).strip().strip('"').strip("'")
    #     parts = s.split("||", 1)
    #     paper_id = parts[0].strip() if len(parts) > 0 else None
    #     author_id = parts[1].strip() if len(parts) > 1 else None
    #     return {"paper_id": paper_id, "author_id": author_id}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"paper_id": None, "author_id": None}
        s = str(val).strip().strip('"').strip("'")
        parts = s.split("||", 1)
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
    # CastType(table_name="table_1", column="affiliation_id", dtype="str")
    # CastType
    _dtype = 'str'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['affiliation_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['affiliation_id']
    if _dtype == "datetime64":
        table_1['affiliation_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['affiliation_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['affiliation_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['affiliation_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['paper_author_combined'])
    # DropColumn
    table_1 = table_1.drop(columns=['paper_author_combined'], errors='ignore')

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['affiliation_id', 'paper_id', 'author_id'])
    # SelectCol
    _cols = [c for c in ['affiliation_id', 'paper_id', 'author_id'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['paper_info'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['paper_info'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="paper_info", target_columns=['paper_id', 'venue', 'year'], func="""
    # def split(val):
    #     parts = [p.strip() for p in str(val).split('|')]
    #     return {
    #         "paper_id": parts[0] if len(parts) > 0 else None,
    #         "venue": parts[1] if len(parts) > 1 else None,
    #         "year": parts[2] if len(parts) > 2 else None
    #     }
    # """)
    # SplitColumn
    def split(val):
        parts = [p.strip() for p in str(val).split('|')]
        return {
            "paper_id": parts[0] if len(parts) > 0 else None,
            "venue": parts[1] if len(parts) > 1 else None,
            "year": parts[2] if len(parts) > 2 else None
        }
    for _c in ['paper_id', 'venue', 'year']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['paper_info']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['paper_id', 'venue', 'year']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['paper_info'])

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
    # SelectCol(table_name="table_1", columns=['paper_id', 'venue', 'year', 'title'])
    # SelectCol
    _cols = [c for c in ['paper_id', 'venue', 'year', 'title'] if c in table_1.columns]
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
