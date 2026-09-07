import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ID', 'Diagnosis'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ID', 'Diagnosis'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Diagnosis'])
    # SelectCol
    _cols = [c for c in ['ID', 'Diagnosis'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID', 'Diagnosis'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID', 'Diagnosis'], keep='first').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['ID', 'TP'])
    # SelectCol
    _cols = [c for c in ['ID', 'TP'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TP", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TP'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TP']
    if _dtype == "datetime64":
        table_1['TP'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TP'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TP'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TP'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="TP", mode="median")
    # MissingValueImputation
    table_1["TP"] = table_1["TP"].fillna(table_1["TP"].median())

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

prepared_table_1 = _prep_1(tables['table_3'])
patients_dx = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
lab_results = prepared_table_2

# Assume prepared tables already materialized as patients_dx and lab_results
# 1) Join on patient ID
joined = patients_dx.merge(lab_results, on='ID', how='inner')

# 2) Filter SJS diagnoses (case-insensitive, substring match)
sjs = joined[joined['Diagnosis'].astype(str).str.contains('SJS', case=False, na=False)]

# 3) Determine normal TP. If no explicit reference interval is provided, a common clinical range is ~6.0 to 8.3 g/dL.
# Convert TP to numeric
sjs['TP_num'] = pd.to_numeric(sjs['TP'], errors='coerce')
normal_tp = sjs[(sjs['TP_num'] >= 6.0) & (sjs['TP_num'] <= 8.3)]

# 4) Count unique patients with at least one normal TP measurement
result = pd.DataFrame({
    'count_normal_tp_in_SJS_patients': [normal_tp['ID'].dropna().astype(str).nunique()]
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
