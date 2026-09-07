import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="artist", func="""
    # import unicodedata, re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     s = re.sub(r'\s+', ' ', s)
    #     # normalize diacritics / encoding issues (e.g., "BaÇµa" -> "Baga" in many corrupted cases)
    #     s_norm = unicodedata.normalize('NFKD', s)
    #     s_norm = ''.join(ch for ch in s_norm if not unicodedata.combining(ch))
    #     return s_norm
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        s = re.sub(r'\s+', ' ', s)
        # normalize diacritics / encoding issues (e.g., "BaÇµa" -> "Baga" in many corrupted cases)
        s_norm = unicodedata.normalize('NFKD', s)
        s_norm = ''.join(ch for ch in s_norm if not unicodedata.combining(ch))
        return s_norm
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["artist"] = table_1["artist"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import re
    # def filter_func(row):
    #     a = row.get('artist', None)
    #     if a is None:
    #         return False
    #     s = str(a).strip().strip('\"').strip(\"'\")
    #     s = re.sub(r'\s+', ' ', s).lower()
    #     # match normalized form of \"Volkan BaÇµa\" after prior diacritic cleanup
    #     return s == \"volkan baga\" or s.replace('.', '') == \"volkan baga\"
    # """)
    # Filter
    def filter_func(row):
        a = row.get('artist', None)
        if a is None:
            return False
        s = str(a).strip().strip('\"').strip(\"'\")
        s = re.sub(r'\s+', ' ', s).lower()
        # match normalized form of \"Volkan BaÇµa\" after prior diacritic cleanup
        return s == \"volkan baga\" or s.replace('.', '') == \"volkan baga\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'artist'])
    # SelectCol
    _cols = [c for c in ['id', 'artist'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="language", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s2 = str(s).strip()
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["language"] = table_1["language"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'language'])
    # SelectCol
    _cols = [c for c in ['id', 'language'] if c in table_1.columns]
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
prepared_cards = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_languages = prepared_table_2

target = prepared_cards.merge(prepared_languages, on='id', how='inner')
result = target[(target['artist'].str.strip()=='Volkan BaÇµa') & (target['language'].str.strip().str.lower()=='french')]
answer = len(result)

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
