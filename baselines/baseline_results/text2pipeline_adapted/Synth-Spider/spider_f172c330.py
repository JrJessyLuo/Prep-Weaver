import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Concatenate', 'params': {'concatenate_columns': ['First_part', 'Last_part'], 'target_column': 'Full_Name', 'func': "def transform(row):\n    first = str(row['First_part']).strip() if row.get('First_part', None) is not None else ''\n    last = str(row['Last_part']).strip() if row.get('Last_part', None) is not None else ''\n    if last == '' or last == '*':\n        return first\n    return (first + ' ' + last).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Player_ID', 'Rank_of_the_year', 'Position', 'College', 'First_part', 'Last_part', 'Full_Name']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': 'fallback_passthrough_after_pipeline_generation_failure: Your previous one-table transform_chain was invalid: ValueError: operation(s) outside benchmark dc_ops space: CodeGeneration. Use only table_indices [0], correct the chain, and return JSON only.', 'source_table': 'table_2'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    first = str(row['First_part']).strip() if row.get('First_part', None) is not None else ''\n    last = str(row['Last_part']).strip() if row.get('Last_part', None) is not None else ''\n    if last == '' or last == '*':\n        return first\n    return (first + ' ' + last).strip()", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['Full_Name'] = tmp_0[['First_part', 'Last_part']].apply(_concat_func_1, axis=1)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['Player_ID', 'Rank_of_the_year', 'Position', 'College', 'First_part', 'Last_part', 'Full_Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
pt1 = prepared_table_1.copy()
pt1['Full_Name'] = (pt1['First_part'].fillna('') + ' ' + pt1['Last_part'].fillna('')).str.replace('\s+', ' ', regex=True).str.strip()
pt2 = prepared_table_2.copy()
# Normalize activity flags into Any_Active
flag_cols = [c for c in pt2.columns if c.startswith('If_active_')]
long = pt2.melt(id_vars=['Player_ID'], value_vars=flag_cols, var_name='flag_col', value_name='Active_Flag')
long['Active_Flag'] = long['Active_Flag'].astype(str).str.strip().str.upper()
long.loc[long['Active_Flag'].isin(['NAN', 'NONE', 'NULL', '']), 'Active_Flag'] = None
long['is_true'] = long['Active_Flag'].eq('T')
long['is_false'] = long['Active_Flag'].eq('F')
agg = long.groupby('Player_ID', as_index=False).agg(any_true=('is_true', 'any'))
agg.rename(columns={'any_true': 'Any_Active'}, inplace=True)
# Default missing players in table_2 to Any_Active=False after merge
integrated = pt1.merge(agg, on='Player_ID', how='left')
integrated['Any_Active'] = integrated['Any_Active'].fillna(False)
# Players that do not play any game = Any_Active == False
result = integrated[integrated['Any_Active'] == False]
# Final projection: player names
target = result[['Full_Name']].rename(columns={'Full_Name': 'Player_Name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
