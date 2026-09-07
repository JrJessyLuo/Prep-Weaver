import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID', 'Date'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID', 'Date'], keep='last').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'RNP'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'RNP'] if c in table_1.columns]
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

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Examination Date', 'Diagnosis', 'Symptoms'])
    # SelectCol
    _cols = [c for c in ['ID', 'Examination Date', 'Diagnosis', 'Symptoms'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lab_immunology = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_admissions = prepared_table_2

# prepared_lab_immunology: columns [ID (int/str), Date, RNP]
# prepared_admissions: columns [ID (float/str), Examination Date, Diagnosis, Symptoms]

# Normalize ID types for join
left = prepared_lab_immunology.copy()
right = prepared_admissions.copy()

# Coerce IDs to string without decimals (some IDs in right are float-like strings)
left['ID'] = left['ID'].astype(str).str.replace('\.0$', '', regex=True)
right['ID'] = right['ID'].astype(str).str.replace('\.0$', '', regex=True)

# Join on patient ID
merged = pd.merge(left, right, on='ID', how='inner')

# Define helper to detect normal anti-RNP. Treat '-', 'neg', 'negative', 'normal', '0', '0.0', 'nan' (as missing) carefully.
# We consider explicit negative/normal markers as normal, positive markers ('+', 'pos', 'positive', '> cutoff') as abnormal.
# If RNP is numeric, assume 0 means negative; otherwise non-numeric text parsed.

def is_normal_rnp(val):
    if pd.isna(val):
        return False
    s = str(val).strip().lower()
    if s in {'-', 'neg', 'negative', 'normal', 'norm'}:
        return True
    if s in {'+', 'pos', 'positive'}:
        return False
    # Try numeric
    try:
        num = float(s)
        # assume zero equals negative; otherwise treat as not normal without reference range
        return num == 0.0
    except Exception:
        # look for patterns like '+-' treat as not normal conservatively
        if '+-' in s or '+' in s:
            return False
        return False

merged['rnp_normal'] = merged['RNP'].apply(is_normal_rnp)

# Determine admission: check if Diagnosis or Symptoms mention admission/hospitalization keywords
adm_keywords = ['admit', 'admitted', 'hospital', 'hospitalized', 'inpatient', 'ward']

def is_admitted(row):
    txt = ' '.join([
        '' if pd.isna(row.get('Diagnosis')) else str(row.get('Diagnosis')),
        '' if pd.isna(row.get('Symptoms')) else str(row.get('Symptoms'))
    ]).lower()
    return any(k in txt for k in adm_keywords)

merged['admitted'] = merged.apply(is_admitted, axis=1)

# Count distinct patients meeting both conditions
eligible = merged[(merged['rnp_normal']) & (merged['admitted'])]
result = eligible['ID'].nunique()

answer = result

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
