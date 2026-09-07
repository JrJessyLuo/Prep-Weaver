import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="artist", mode="mode")
    # MissingValueImputation
    table_1["artist"] = table_1["artist"].fillna(table_1["artist"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="artist", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     # remove wrapping quotes if present
    #     s = re.sub(r'^(["\'])(.*)\1$', r'\2', s)
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        # remove wrapping quotes if present
        s = re.sub(r'^(["\'])(.*)\1$', r'\2', s)
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["artist"] = table_1["artist"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="setCode", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     s = re.sub(r'^(["\'])(.*)\1$', r'\2', s)
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        s = re.sub(r'^(["\'])(.*)\1$', r'\2', s)
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["setCode"] = table_1["setCode"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="setName", func="""
    # def compute(row):
    #     # setName not present in the provided table; preserve an identifier for later integration
    #     return row.get('setCode', None)
    # """)
    # AddNewColumn
    def compute(row):
        # setName not present in the provided table; preserve an identifier for later integration
        return row.get('setCode', None)
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["setName"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'artist', 'setCode', 'setName'])
    # SelectCol
    _cols = [c for c in ['id', 'artist', 'setCode', 'setName'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['name'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['code', 'name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['code', 'name'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['code', 'name'])
    # SelectCol
    _cols = [c for c in ['code', 'name'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_sets = prepared_table_2

target_sets = prepared_sets.copy()
# Identify the set code for the German-named set string
match = target_sets[target_sets['name'].str.lower() == 'hauptset zehnte edition'.lower()]
# If exact match fails, try contains (robust to extra text)
if match.empty:
    match = target_sets[target_sets['name'].str.lower().str.contains('hauptset zehnte edition'.lower(), na=False)]

# Join cards to the matched set(s) via set code
cards_in_set = prepared_cards.merge(match[['code']], left_on='setCode', right_on='code', how='inner')

# Filter by artist Adam Rex and count
answer_value = (cards_in_set['artist'].fillna('').str.strip().str.lower() == 'adam rex').sum()

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
