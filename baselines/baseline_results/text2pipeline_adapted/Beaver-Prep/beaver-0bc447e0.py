import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_TITLE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    import re\n    s = "" if s is None or str(s).lower() == "nan" else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    import re\n    s = "" if s is None or str(s).lower() == "nan" else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_KEY', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_TITLE'] = tmp_1['SUBJECT_TITLE'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None or str(s).lower() == "nan" else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['SUBJECT_TITLE'] = tmp_2['SUBJECT_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None or str(s).lower() == "nan" else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['RESPONSIBLE_FACULTY_NAME'] = tmp_3['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['TERM_CODE', 'SUBJECT_KEY', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Identify summer terms by TERM_CODE containing a summer indicator; use broad, case-insensitive matching and a fallback if none match
mask_summer = df['TERM_CODE'].astype(str).str.contains('SU', case=False, na=False) | df['TERM_CODE'].astype(str).str.contains('SUM', case=False, na=False)
if not mask_summer.any():
    # Fallback: include all rows rather than empty
    df_summer = df
else:
    df_summer = df[mask_summer]
# Compute instructor counts and longest name length per subject offering (SUBJECT_KEY)
df_names = df_summer[['SUBJECT_KEY','SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME']].copy()
# Normalize name strings for length calculation
name_series = df_names['RESPONSIBLE_FACULTY_NAME'].fillna('').astype(str).str.strip()
df_names['name_clean'] = name_series
# Count distinct non-empty instructor names per SUBJECT_KEY
instructor_counts = df_names[df_names['name_clean'] != ''].groupby('SUBJECT_KEY')['name_clean'].nunique().rename('num_instructors').reset_index()
# Longest instructor name length per SUBJECT_KEY
longest_len = df_names.assign(name_len=df_names['name_clean'].str.len()).groupby('SUBJECT_KEY')['name_len'].max().rename('longest_name_length').reset_index()
# Subject title: choose a representative title per SUBJECT_KEY (first non-null)
subject_titles = df_names.copy()
subject_titles['title_nonnull'] = subject_titles['SUBJECT_TITLE']
subject_titles = subject_titles.sort_values(['SUBJECT_KEY']).groupby('SUBJECT_KEY', as_index=False)['title_nonnull'].first().rename(columns={'title_nonnull':'SUBJECT_TITLE'})
# Merge aggregates
agg = subject_titles.merge(instructor_counts, on='SUBJECT_KEY', how='left').merge(longest_len, on='SUBJECT_KEY', how='left')
# Fill NaNs where no instructors: counts -> 0, longest length -> 0
agg['num_instructors'] = agg['num_instructors'].fillna(0).astype(int)
agg['longest_name_length'] = agg['longest_name_length'].fillna(0).astype(int)
# Final projection
target = agg[['SUBJECT_TITLE','num_instructors','longest_name_length']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
