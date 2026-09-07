import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'Birthday', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Description', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'First Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Admission', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Diagnosis_Part1', 'Diagnosis_Part2'], 'target_column': 'Diagnosis', 'func': 'def transform(row):\n    vals = []\n    for v in row:\n        s = "" if v is None else str(v)\n        s = s.strip()\n        if s.lower() in {"none", "nan", "-"}:\n            s = ""\n        vals.append(s)\n    out = " ".join([v for v in vals if v])\n    return out.strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'SEX', 'Birthday', 'Description', 'First Date', 'Admission', 'Diagnosis']}, 'table_indices': [0]}], [{'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'HGB', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'GOT', 'GPT', 'LDH', 'ALP', 'TP', 'ALB', 'UA', 'UN', 'CRE', 'T-BIL', 'T-CHO', 'TG', 'CPK', 'GLU', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PT', 'APTT', 'FG', 'PIC', 'TAT', 'TAT2', 'U-PRO', 'IGG', 'IGA', 'IGM', 'CRP', 'RA', 'RF', 'C3', 'C4', 'RNP', 'SM', 'SC170', 'SSA']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['Birthday'] = pd.to_datetime(tmp_0['Birthday'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Description'] = pd.to_datetime(tmp_1['Description'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['First Date'] = pd.to_datetime(tmp_2['First Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['Admission'] = pd.to_datetime(tmp_3['Admission'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(row):\n    vals = []\n    for v in row:\n        s = "" if v is None else str(v)\n        s = s.strip()\n        if s.lower() in {"none", "nan", "-"}:\n            s = ""\n        vals.append(s)\n    out = " ".join([v for v in vals if v])\n    return out.strip()', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_4['Diagnosis'] = tmp_4[['Diagnosis_Part1', 'Diagnosis_Part2']].apply(_concat_func_1, axis=1)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['ID', 'SEX', 'Birthday', 'Description', 'First Date', 'Admission', 'Diagnosis']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['Date'] = pd.to_datetime(tmp_0['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['HGB'] = pd.to_numeric(tmp_1['HGB'], errors='coerce').astype(float)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ID', 'Date', 'GOT', 'GPT', 'LDH', 'ALP', 'TP', 'ALB', 'UA', 'UN', 'CRE', 'T-BIL', 'T-CHO', 'TG', 'CPK', 'GLU', 'WBC', 'RBC', 'HGB', 'HCT', 'PLT', 'PT', 'APTT', 'FG', 'PIC', 'TAT', 'TAT2', 'U-PRO', 'IGG', 'IGA', 'IGM', 'CRP', 'RA', 'RF', 'C3', 'C4', 'RNP', 'SM', 'SC170', 'SSA']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge prepared tables on ID
integrated = prepared_table_2.merge(prepared_table_1, on='ID', how='inner')

# Parse dates safely
integrated = integrated.copy()
integrated['Date_parsed'] = pd.to_datetime(integrated['Date'], errors='coerce')
integrated['Birthday_parsed'] = pd.to_datetime(integrated['Birthday'], errors='coerce')

# Compute age at exam date where both dates are available
integrated['age_at_exam_years'] = (integrated['Date_parsed'] - integrated['Birthday_parsed']).dt.days / 365.25

# Identify highest HGB (ensure numeric)
integrated['HGB_num'] = pd.to_numeric(integrated['HGB'], errors='coerce')
max_hgb = integrated['HGB_num'].max()

# Select candidates with highest HGB; prefer rows with valid age, break ties by earliest exam date then ID
candidates = integrated[integrated['HGB_num'] == max_hgb]
# If all ages are NaN, we'll still pick deterministically by Date then ID
candidates = candidates.sort_values(['Date_parsed', 'ID']).copy()

# Prefer rows with non-null age; if none, keep as-is
valid_age = candidates[candidates['age_at_exam_years'].notna()]
if not valid_age.empty:
    top_row = valid_age.head(1)
else:
    top_row = candidates.head(1)

# Final projection
target = top_row[['age_at_exam_years', 'Diagnosis']].rename(columns={'Diagnosis': 'doctor_diagnosis'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
