import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Transpose(table_name="table_1")
    # Transpose
    if table_1.empty or len(table_1.columns) == 0:
        table_1 = table_1.transpose()
    else:
        _t = table_1.transpose()
        _newcols = _t.iloc[0].tolist()
        _t = _t.iloc[1:]
        _first = table_1.columns[0]
        _t.insert(0, _first, _t.index)
        _t.columns = [_first] + _newcols
        table_1 = _t.reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Concatenate(table_name="table_1", concatenate_columns=['lname_part1', 'lname_part2'], target_column="last_name", func="""
    # import pandas as pd
    # def concat(row: pd.Series) -> str:
    #     p1 = row.get('lname_part1', None)
    #     p2 = row.get('lname_part2', None)
    #     p1 = None if pd.isna(p1) else str(p1).strip()
    #     p2 = None if pd.isna(p2) else str(p2).strip()
    #     if p1 and p2:
    #         return f"{p1} {p2}"
    #     if p1:
    #         return p1
    #     if p2:
    #         return p2
    #     return None
    #  """)
    # Concatenate
    def concat(row: pd.Series) -> str:
        p1 = row.get('lname_part1', None)
        p2 = row.get('lname_part2', None)
        p1 = None if pd.isna(p1) else str(p1).strip()
        p2 = None if pd.isna(p2) else str(p2).strip()
        if p1 and p2:
            return f"{p1} {p2}"
        if p1:
            return p1
        if p2:
            return p2
        return None
    def _cat_apply(row):
        try:
            return concat(row)
        except Exception:
            return None
    table_1["last_name"] = table_1[['lname_part1', 'lname_part2']].apply(_cat_apply, axis=1)
    table_1 = table_1.drop(columns=['lname_part1', 'lname_part2'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fname", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove surrounding/doubled quotes like ""1859"" style (defensive)
    #     return s.replace('""', '').strip('"').strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove surrounding/doubled quotes like ""1859"" style (defensive)
        return s.replace('""', '').strip('"').strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fname"] = table_1["fname"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="last_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     return s.replace('""', '').strip('"').strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        return s.replace('""', '').strip('"').strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["last_name"] = table_1["last_name"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'fname', 'new_name': 'first_name'}])
    # Rename
    table_1 = table_1.rename(columns={'fname': 'first_name'})

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['artistID', 'first_name', 'last_name'])
    # SelectCol
    _cols = [c for c in ['artistID', 'first_name', 'last_name'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="paintingID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['paintingID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['paintingID']
    if _dtype == "datetime64":
        table_1['paintingID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['paintingID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['paintingID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['paintingID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['paintingID', 'painterID', 'medium'])
    # SelectCol
    _cols = [c for c in ['paintingID', 'painterID', 'medium'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_artists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_paintings = prepared_table_2

# prepared_artists: columns [artistID, first_name, last_name]
# prepared_paintings: columns [paintingID, painterID, medium]

# Join artists to their paintings
ap = prepared_artists.merge(prepared_paintings, left_on='artistID', right_on='painterID', how='inner')

# Normalize medium text for robust matching
m = ap.copy()
m['medium_norm'] = m['medium'].astype(str).str.strip().str.lower()

# Identify artists with at least one oil painting and at least one lithographic work
has_oil = m[m['medium_norm'].str.contains('\boil\b', na=False)].groupby('artistID').size().rename('oil_cnt')
has_litho = m[m['medium_norm'].str.contains('lithograph|lithographic|lithography', na=False)].groupby('artistID').size().rename('litho_cnt')

both = (pd.concat([has_oil, has_litho], axis=1).fillna(0))
both = both[(both['oil_cnt'] > 0) & (both['litho_cnt'] > 0)].reset_index()[['artistID']]

# Return first and last names of matched artists
result = both.merge(prepared_artists[['artistID','first_name','last_name']], on='artistID', how='left')
answer = result[['first_name','last_name']].drop_duplicates().reset_index(drop=True)

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
