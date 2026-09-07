import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'IGG']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Admission', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Birthday', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'First Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Admission']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ID', 'Date', 'IGG']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Admission'] = tmp_1['Admission'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Birthday'] = pd.to_datetime(tmp_2['Birthday'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['First Date'] = pd.to_datetime(tmp_3['First Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['ID', 'Admission']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='ID', how='inner')
# Define what constitutes a 'normal' IGG. Without explicit reference ranges in data, use a broad adult reference: 700-1600 mg/dL.
# Keep robustness: include boundary values as normal.
normal_mask = integrated['IGG'].notna() & (integrated['IGG'] >= 700) & (integrated['IGG'] <= 1600)
normal_igg = integrated[normal_mask]
# Determine admissions. Normalize Admission text to handle common codings.
adm = normal_igg['Admission'].astype(str).str.strip().str.upper()
# Heuristics: treat values indicating admission/inpatient/yes/positive as admitted; '-' and 'NO' as not admitted.
admitted_mask = adm.isin(['Y','YES','ADMIT','ADMITTED','INPATIENT','IP','HOSPITALIZED','HOSPITALISED','1','TRUE','T','POSITIVE','+'])
# If no rows match admitted_mask due to coding like '+/-', fall back to match any '+' substring not equal to '-' only.
if admitted_mask.sum() == 0:
    admitted_mask = adm.str.contains('\+', regex=True) & (adm != '-')
# Count unique patients with normal IGG who were admitted.
count_admitted = normal_igg.loc[admitted_mask, 'ID'].nunique()
# Return as a one-row DataFrame
target = __import__('pandas').DataFrame({'patients_with_normal_IGG_and_admitted': [int(count_admitted)]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
