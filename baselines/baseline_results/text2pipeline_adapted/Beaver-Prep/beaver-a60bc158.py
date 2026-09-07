import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ACADEMIC_YEAR'] = tmp_0['ACADEMIC_YEAR'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['SUBJECT_ID'] = tmp_2['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()

# Ensure correct dtypes
df['ACADEMIC_YEAR'] = df['ACADEMIC_YEAR'].astype(str)
df['TERM_CODE'] = df['TERM_CODE'].astype(str)
df['SUBJECT_ID'] = df['SUBJECT_ID'].astype(str)

# Count distinct subjects introduced per academic year-term
term_counts = (
    df.drop_duplicates(subset=['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID'])
      .groupby(['ACADEMIC_YEAR','TERM_CODE'], as_index=False)
      .agg(NEW_SUBJECTS=('SUBJECT_ID','nunique'))
)

# Sort by academic year then term code for sequential display
term_counts = term_counts.sort_values(['ACADEMIC_YEAR','TERM_CODE']).reset_index(drop=True)

# Suppress repeated academic year display by blanking consecutive duplicates
term_counts['DISPLAY_ACADEMIC_YEAR'] = term_counts['ACADEMIC_YEAR']
term_counts.loc[
    term_counts['DISPLAY_ACADEMIC_YEAR'].eq(term_counts['DISPLAY_ACADEMIC_YEAR'].shift()),
    'DISPLAY_ACADEMIC_YEAR'
] = ''

# Compute grand total across all rows
grand_total = term_counts['NEW_SUBJECTS'].sum()

# Build total row without using deprecated append
total_row = pd.DataFrame({
    'DISPLAY_ACADEMIC_YEAR': ['TOTAL'],
    'TERM_CODE': [''],
    'NEW_SUBJECTS': [grand_total]
})

result = pd.concat([
    term_counts[['DISPLAY_ACADEMIC_YEAR','TERM_CODE','NEW_SUBJECTS']],
    total_row[['DISPLAY_ACADEMIC_YEAR','TERM_CODE','NEW_SUBJECTS']]
], ignore_index=True)

# Final projection
target = result.rename(columns={'DISPLAY_ACADEMIC_YEAR':'ACADEMIC_YEAR'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
