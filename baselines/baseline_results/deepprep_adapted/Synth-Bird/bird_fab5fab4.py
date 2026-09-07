import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['attribute_name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['attribute_name'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute_name", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     # collapse repeated whitespace
    #     s = re.sub(r'\s+', ' ', s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        # collapse repeated whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute_name"] = table_1["attribute_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'attribute_name'])
    # SelectCol
    _cols = [c for c in ['id', 'attribute_name'] if c in table_1.columns]
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
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['xb', 'yc', 'skin_colour_id', 'race_id', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg', 'first_name', 'last_name'])
    # DropColumn
    table_1 = table_1.drop(columns=['xb', 'yc', 'skin_colour_id', 'race_id', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg', 'first_name', 'last_name'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="eye_colour_id", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     return None
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["eye_colour_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'superhero_name', 'hair_colour_id', 'eye_colour_id'])
    # SelectCol
    _cols = [c for c in ['id', 'superhero_name', 'hair_colour_id', 'eye_colour_id'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_4'])
prepared_colour_dim = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_table_3 = _prep_3(tables['table_2'])
prepared_heroes = prepared_table_3

hair_map = prepared_colour_dim.rename(columns={'id':'hair_colour_id','attribute_name':'hair_colour_name'})
eye_map = prepared_colour_dim.rename(columns={'id':'eye_colour_id','attribute_name':'eye_colour_name'})
with_hair = prepared_heroes.merge(hair_map, on='hair_colour_id', how='left')
with_both = with_hair.merge(eye_map, on='eye_colour_id', how='left')
target = with_both.loc[(with_both['hair_colour_name'].str.lower()=='black') & (with_both['eye_colour_name'].str.lower()=='black'), ['superhero_name']].drop_duplicates().sort_values('superhero_name')

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
