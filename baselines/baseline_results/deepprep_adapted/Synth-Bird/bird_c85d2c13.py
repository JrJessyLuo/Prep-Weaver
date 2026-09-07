import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="attribute_value", mode="mean")
    # MissingValueImputation
    table_1["attribute_value"] = table_1["attribute_value"].fillna(table_1["attribute_value"].mean())

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="hero_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['hero_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['hero_id']
    if _dtype == "datetime64":
        table_1['hero_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['hero_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['hero_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['hero_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="attribute_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['attribute_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['attribute_id']
    if _dtype == "datetime64":
        table_1['attribute_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['attribute_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['attribute_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['attribute_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="attribute_value", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['attribute_value'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['attribute_value']
    if _dtype == "datetime64":
        table_1['attribute_value'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['attribute_value'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['attribute_value'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['attribute_value'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['hero_id', 'attribute_id', 'attribute_value'])
    # SelectCol
    _cols = [c for c in ['hero_id', 'attribute_id', 'attribute_value'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_7'])
hero_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
attribute_dictionary = prepared_table_2

# Inputs: hero_attributes, attribute_dictionary, plus an external heroes table with names and species if available
# Step 1: Map attribute ids to names (not directly needed for vampire filtering but preserved as evidence)
attrs = hero_attributes.merge(attribute_dictionary, left_on='attribute_id', right_on='id', how='left')
# Step 2: Integrate with a heroes metadata table if present (expected columns: hero_id, full_name, species or type)
# This step assumes a table 'heroes' exists after BAT discovery; if not, cannot answer names of vampire heroes from given tables alone.
try:
    heroes  # noqa: F821
except NameError:
    # Without a heroes table containing names/species, we cannot produce full names of vampire heroes.
    target = pd.DataFrame(columns=['full_name']).drop_duplicates()
else:
    # Filter heroes to vampires using species/type column (case-insensitive contains 'vampire')
    vamp_heroes = heroes[heroes['species'].str.contains('vampire', case=False, na=False) | heroes.get('type', pd.Series(index=heroes.index, dtype='object')).str.contains('vampire', case=False, na=False)]
    # Ensure we only return distinct full names
    target = vamp_heroes[['full_name']].drop_duplicates()

# The final answer is the list of full_name values in 'target'

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
