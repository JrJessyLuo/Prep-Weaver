import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SEX', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Birthday', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'SEX', 'Birthday']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GOT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Date', 'new_name': 'LabDate'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'LabDate', 'GOT']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SEX'] = tmp_1['SEX'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['Birthday'] = pd.to_datetime(tmp_2['Birthday'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ID', 'SEX', 'Birthday']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['GOT'] = pd.to_numeric(tmp_2['GOT'], errors='coerce').astype(float)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'Date': 'LabDate'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['ID', 'LabDate', 'GOT']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='ID', how='inner')
# Define normal range for GOT (AST). A common adult reference range is ~10-40 U/L; use inclusive bounds.
normal_low, normal_high = 10.0, 40.0
# Filter for lab exams in 1994 with GOT within normal range
mask_1994 = (integrated['LabDate'].astype('datetime64[ns]').dt.year == 1994)
mask_normal = integrated['GOT'].between(normal_low, normal_high, inclusive='both')
filtered = integrated[mask_1994 & mask_normal]
# Project required output: patient with sex and date of birthday
target = filtered[['ID', 'SEX', 'Birthday']].drop_duplicates().sort_values(['ID'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
