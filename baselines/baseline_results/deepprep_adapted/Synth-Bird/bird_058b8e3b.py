import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['id'])
    # DropColumn
    table_1 = table_1.drop(columns=['id'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="language", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # strip surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # strip surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["language"] = table_1["language"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="set_info", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # strip surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # strip surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["set_info"] = table_1["set_info"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="set_info", target_columns=['set_code', 'set_name'], func="""
    # def split(val):
    #     if val is None:
    #         return {"set_code": None, "set_name": None}
    #     text = str(val)
    #     parts = text.split('|', 1)
    #     if len(parts) == 2:
    #         return {"set_code": parts[0].strip(), "set_name": parts[1].strip()}
    #     # fallback if delimiter missing
    #     return {"set_code": text.strip(), "set_name": None}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"set_code": None, "set_name": None}
        text = str(val)
        parts = text.split('|', 1)
        if len(parts) == 2:
            return {"set_code": parts[0].strip(), "set_name": parts[1].strip()}
        # fallback if delimiter missing
        return {"set_code": text.strip(), "set_name": None}
    for _c in ['set_code', 'set_name']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['set_info']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['set_code', 'set_name']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['set_info'])

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['set_code', 'set_name', 'language'])
    # SelectCol
    _cols = [c for c in ['set_code', 'set_name', 'language'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="language", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
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
    # SelectCol(table_name="table_1", columns=['name', 'language', 'uuid'])
    # SelectCol
    _cols = [c for c in ['name', 'language', 'uuid'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_sets_by_language = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_cards_by_language = prepared_table_2

# Assume input DataFrames are: prepared_sets_by_language, prepared_cards_by_language
# Goal: sets that lack Japanese translation but have Korean translation.

sets = prepared_sets_by_language.copy()

# Normalize language labels
lang_norm = {
    'Japanese': 'Japanese',
    'Korean': 'Korean',
}
sets['language_norm'] = sets['language']

# Identify sets with Korean and without Japanese
has_korean = sets.loc[sets['language_norm'].str.lower() == 'korean', ['set_code']].drop_duplicates()
has_japanese = sets.loc[sets['language_norm'].str.lower() == 'japanese', ['set_code']].drop_duplicates()

eligible_codes = has_korean.merge(has_japanese, on='set_code', how='left', indicator=True)
eligible_codes = eligible_codes.loc[eligible_codes['_merge'] == 'left_only', ['set_code']]

result = eligible_codes.merge(sets[['set_code', 'set_name']].drop_duplicates(), on='set_code', how='left').drop_duplicates()

# Final answer: list of set names
answer = result['set_name'].dropna().drop_duplicates().sort_values().tolist()
answer

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
