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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Planet', 'new_name': 'employee_id'}, {'old_name': 'Level', 'new_name': 'omega_level'}])
    # Rename
    table_1 = table_1.rename(columns={'Planet': 'employee_id', 'Level': 'omega_level'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['employee_id', 'omega_level'])
    # SelectCol
    _cols = [c for c in ['employee_id', 'omega_level'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="employee_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['employee_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['employee_id']
    if _dtype == "datetime64":
        table_1['employee_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['employee_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['employee_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['employee_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="omega_level", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['omega_level'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['omega_level']
    if _dtype == "datetime64":
        table_1['omega_level'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['omega_level'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['omega_level'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['omega_level'] = _series.astype(str)

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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'ygh', 'new_name': 'employee_id'}])
    # Rename
    table_1 = table_1.rename(columns={'ygh': 'employee_id'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Name', 'new_name': 'name'}])
    # Rename
    table_1 = table_1.rename(columns={'Name': 'name'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['employee_id', 'name'])
    # SelectCol
    _cols = [c for c in ['employee_id', 'name'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
employee_clearance_levels = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
employees = prepared_table_2

target = employee_clearance_levels.merge(employees, on='employee_id', how='inner'); result = target[target['omega_level'] == 3][['name']].drop_duplicates().sort_values(by='name').reset_index(drop=True)

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
