import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="superhero_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     if (len(s2) >= 2) and ((s2[0] == '"' and s2[-1] == '"') or (s2[0] == "'" and s2[-1] == "'")):
    #         s2 = s2[1:-1].strip()
    #     return s2.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip()
        if (len(s2) >= 2) and ((s2[0] == '"' and s2[-1] == '"') or (s2[0] == "'" and s2[-1] == "'")):
            s2 = s2[1:-1].strip()
        return s2.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["superhero_name"] = table_1["superhero_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="superhero_name", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if len(s2) >= 2 and ((s2[0] == '"' and s2[-1] == '"') or (s2[0] == "'" and s2[-1] == "'")):
    #         s2 = s2[1:-1].strip()
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip()
        # remove surrounding single/double quotes if present
        if len(s2) >= 2 and ((s2[0] == '"' and s2[-1] == '"') or (s2[0] == "'" and s2[-1] == "'")):
            s2 = s2[1:-1].strip()
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["superhero_name"] = table_1["superhero_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['id', 'superhero_name'])
    # SelectCol
    _cols = [c for c in ['id', 'superhero_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['id'], keep='first').reset_index(drop=True)

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
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
hero_attributes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
attribute_dict = prepared_table_3

# Assume prepared tables: heroes, hero_attributes, attribute_dict
merged = heroes.merge(hero_attributes, left_on='id', right_on='hero_id', how='inner')\
               .merge(attribute_dict, left_on='attribute_id', right_on='id', how='inner')

# Filter to the requested superhero
abomination_attrs = merged[merged['superhero_name'].str.lower() == 'abomination']

# Select the attribute values (with names) for the superhero
# Normalize attribute_value by stripping surrounding quotes if present
abomination_attrs = abomination_attrs.assign(
    attribute_value=abomination_attrs['attribute_value'].astype(str).str.strip('"')
)[['superhero_name', 'attribute_name', 'attribute_value']].sort_values(['attribute_name'])

target = abomination_attrs

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
