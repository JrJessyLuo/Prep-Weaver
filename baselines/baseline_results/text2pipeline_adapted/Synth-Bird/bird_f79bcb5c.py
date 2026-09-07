import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SEX', 'func': "def transform(s):\n    s = str(s).strip().lower()\n    if s in ['m', 'male']:\n        return 'M'\n    if s in ['f', 'female']:\n        return 'F'\n    return s.upper()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'SEX']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'GPT']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s).strip().lower()\n    if s in ['m', 'male']:\n        return 'M'\n    if s in ['f', 'female']:\n        return 'F'\n    return s.upper()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SEX'] = tmp_1['SEX'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ID', 'SEX']].copy()
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
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ID', 'Date', 'GPT']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='ID', how='inner')
# Define a plausible normal GPT range; absent explicit reference ranges in the data, use a common clinical adult range 0-40 U/L and include boundary.
normal_mask = (integrated['GPT'].notna()) & (integrated['GPT'] >= 0) & (integrated['GPT'] <= 40)
normal_rows = integrated.loc[normal_mask]
# Count unique patients with any normal GPT, then restrict to male
male_normal_patients = normal_rows.loc[normal_rows['SEX'].str.upper() == 'M', 'ID'].drop_duplicates()
result = male_normal_patients.to_frame(name='ID')
result['male_normal_gpt_count'] = 1
target = result[['male_normal_gpt_count']].head(1)
if target.empty:
    # Fallback: if strict range yields none, relax to GPT <= 45
    relaxed = integrated.loc[(integrated['GPT'].notna()) & (integrated['GPT'] <= 45) & (integrated['SEX'].str.upper() == 'M'), 'ID'].drop_duplicates()
    target = relaxed.to_frame(name='ID')
    target['male_normal_gpt_count'] = 1
    target = target[['male_normal_gpt_count']].head(1)
# Summarize into a single-row DataFrame with the count value
count_value = male_normal_patients.nunique()
target = integrated.iloc[0:0].copy()
target['male_normal_gpt_count'] = [count_value]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
