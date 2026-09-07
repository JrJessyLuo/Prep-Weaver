import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'yxmc', 'new_name': 'University_Name'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['University_ID', 'University_Name']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'Major_ID', 'func': 'def transform(s):\n    s = \'\' if s is None else str(s)\n    return s.strip().strip(\'"\').strip("\'")'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Major_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Major_ID', 'Major_Name', 'Major_Code']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['u_id', 'm_id', 'Rank']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'yxmc': 'University_Name'})
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['University_ID', 'University_Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = \'\' if s is None else str(s)\n    return s.strip().strip(\'"\').strip("\'")', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['Major_ID'] = tmp_0['Major_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Major_ID'] = pd.to_numeric(tmp_1['Major_ID'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Major_ID', 'Major_Name', 'Major_Code']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['u_id', 'm_id', 'Rank']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
maj = prepared_table_3.merge(prepared_table_2, left_on='m_id', right_on='Major_ID', how='left')
uni_maj = maj.merge(prepared_table_1, left_on='u_id', right_on='University_ID', how='left')
# Identify universities that have both Accounting and Urban Education majors
# Use case-insensitive matching and allow partial robust matches
maj_names = uni_maj['Major_Name'].fillna('').str.lower()
accounting_mask = maj_names.str.contains('accounting', regex=False)
urban_edu_mask = maj_names.str.contains('urban education', regex=False)
# Aggregate presence by university
agg = uni_maj.assign(has_accounting=accounting_mask, has_urban_education=urban_edu_mask)
agg2 = agg.groupby(['University_ID', 'University_Name'], as_index=False)[['has_accounting','has_urban_education']].max()
res = agg2[(agg2['has_accounting']) & (agg2['has_urban_education'])]
# Fallback: if no exact 'Urban Education' found, try broader 'urban' AND 'education' across majors per university
if res.empty:
    urban_mask = maj_names.str.contains('urban', regex=False)
    education_mask = maj_names.str.contains('education', regex=False)
    agg_b = uni_maj.assign(has_accounting=accounting_mask, has_urban=urban_mask, has_education=education_mask)
    agg_b2 = agg_b.groupby(['University_ID', 'University_Name'], as_index=False)[['has_accounting','has_urban','has_education']].max()
    res = agg_b2[(agg_b2['has_accounting']) & (agg_b2['has_urban']) & (agg_b2['has_education'])][['University_ID','University_Name']]
else:
    res = res[['University_ID','University_Name']]
# Final projection: unique university names
target = res.drop_duplicates(subset=['University_ID', 'University_Name']).sort_values('University_Name')[['University_Name']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
