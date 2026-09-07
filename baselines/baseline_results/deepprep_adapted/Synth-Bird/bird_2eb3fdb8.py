import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ID']
    if _dtype == "datetime64":
        table_1['ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="ID", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ID']
    if _dtype == "datetime64":
        table_1['ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Examination Date'])
    # SelectCol
    _cols = [c for c in ['ID', 'Examination Date'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Examination Date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['Examination Date'] = table_1['Examination Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Examination Date'] = table_1['Examination Date'].dt.strftime('%Y-%m-%d')

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lab_tests = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_exams = prepared_table_2

# Assume prepared tables are provided as DataFrames: prepared_lab_tests, prepared_exams
# 1) Filter lab tests to October 1991
lab = prepared_lab_tests.copy()
lab['Date'] = pd.to_datetime(lab['Date'], errors='coerce')
lab_oct91 = lab[(lab['Date'].dt.year == 1991) & (lab['Date'].dt.month == 10)]

# 2) If multiple lab rows per patient in Oct 1991, pick the first date per patient (arbitrary but consistent)
lab_oct91_first = lab_oct91.sort_values('Date').groupby('ID', as_index=False).first()

# 3) We do not have birth dates in the selected tables; age as of 1999 cannot be computed from these tables alone.
# Return indication of missing required data (e.g., date of birth). If there were a demographics table with DOB,
# we would join on ID, compute age in 1999, and then average across patients identified in lab_oct91_first.

result = pd.DataFrame({
    'error': ['Missing required data to compute ages (e.g., Date of Birth). Add a demographics table with DOB joined on ID).']
})

target = result

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
