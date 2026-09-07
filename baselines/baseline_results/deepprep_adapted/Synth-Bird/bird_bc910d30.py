import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'ALP'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'ALP'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # CastType(table_name="table_1", column="ALP", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ALP'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ALP']
    if _dtype == "datetime64":
        table_1['ALP'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ALP'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ALP'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ALP'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ALP'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ALP'], how='any').reset_index(drop=True)

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
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     # keep only the Admission attribute row for each patient
    #     return str(row['attribute']).strip().lower() == 'admission'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # keep only the Admission attribute row for each patient
        return str(row['attribute']).strip().lower() == 'admission'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'value', 'new_name': 'Admission'}])
    # Rename
    table_1 = table_1.rename(columns={'value': 'Admission'})

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Admission'])
    # SelectCol
    _cols = [c for c in ['ID', 'Admission'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_labs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_demographics = prepared_table_2

# prepared_labs: columns ['ID','Date','ALP'] with ALP as numeric
# prepared_demographics: columns ['ID','Admission'] with Admission like '+' (inpatient) or '-' (outpatient)

# Integrate on patient ID
integrated = prepared_labs.merge(prepared_demographics, on='ID', how='inner')

# Define ALP normal range (example adult reference: 44-147 U/L; adjust if dataset-specific ranges are known)
ALP_LOW, ALP_HIGH = 44, 147

# Filter to records with ALP within normal range
normal_alp = integrated[(integrated['ALP'].notna()) & (integrated['ALP'] >= ALP_LOW) & (integrated['ALP'] <= ALP_HIGH)]

# Map Admission flag to categories
# Assumption: '+' indicates inpatient (admitted), '-' indicates outpatient; other/null treated as unknown
normal_alp['care_setting'] = normal_alp['Admission'].map({'+': 'inpatient', '-': 'outpatient'}).fillna('unknown')

# Derive answer: distribution of inpatient vs outpatient among normal-ALP patients
answer = normal_alp['care_setting'].value_counts().to_frame('count').reset_index().rename(columns={'index': 'care_setting'})

# Optionally, if a single label is needed (e.g., which setting they were treated in most):
# predominant = answer.sort_values('count', ascending=False).head(1)

target = answer

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
