import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ID', 'Date', 'ALB'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ID', 'Date', 'ALB'], how='any').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="ALB", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ALB'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ALB']
    if _dtype == "datetime64":
        table_1['ALB'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ALB'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ALB'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ALB'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'ALB'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'ALB'] if c in table_1.columns]
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
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Examination Date', 'new_name': 'exam_date'}])
    # Rename
    table_1 = table_1.rename(columns={'Examination Date': 'exam_date'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="exam_date", date_format="%Y-%m-%d")
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
    table_1['exam_date'] = table_1['exam_date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['exam_date'] = table_1['exam_date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'exam_date'])
    # SelectCol
    _cols = [c for c in ['ID', 'exam_date'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'exam_date', 'new_name': 'Examination Date'}])
    # Rename
    table_1 = table_1.rename(columns={'exam_date': 'Examination Date'})

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_labs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_patients = prepared_table_2

# Assumptions:
# - A separate demographics table with columns ['ID','Sex','Birthday'] must exist to satisfy the question's sex and birthday requirements.
# - Albumin normal range assumed as [3.5, 5.0] g/dL unless domain metadata provides exact ref range.
# The following pseudocode shows integration and filtering steps.

# Convert types
prepared_labs['ALB'] = pd.to_numeric(prepared_labs['ALB'], errors='coerce')
prepared_labs['Date'] = pd.to_datetime(prepared_labs['Date'], errors='coerce')
prepared_patients['Examination Date'] = pd.to_datetime(prepared_patients['Examination Date'], errors='coerce')

tmp = prepared_labs.merge(prepared_patients[['ID']], on='ID', how='left')

# Join in demographics providing Sex and Birthday (not available in selected tables)
# demographics has columns: ID, Sex, Birthday
full = tmp.merge(demographics[['ID','Sex','Birthday']], on='ID', how='left')

# Filter male and albumin not within range
low, high = 3.5, 5.0
mask = (full['Sex'].str.upper().str.startswith('M')) & (~full['ALB'].between(low, high, inclusive='both'))
res = full.loc[mask, ['ID','Birthday','ALB','Date']].dropna(subset=['Birthday'])

# Sort by birthday descending
res = res.sort_values(by='Birthday', ascending=False)

# If multiple lab rows per patient, keep latest lab row per patient (optional depending on intent)
# res = res.sort_values(['ID','Date']).groupby('ID', as_index=False).tail(1).sort_values('Birthday', ascending=False)

target = res

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
