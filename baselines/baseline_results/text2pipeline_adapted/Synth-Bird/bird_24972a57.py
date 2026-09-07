import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'cds', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'cds', 'new_name': 'CDSCode'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NumTstTakr', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'enroll12', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CDSCode', 'rtype', 'NumTstTakr', 'school_name', 'district', 'county', 'enroll12']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'CDSCode', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MailCity', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'City', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CDSCode', 'School', 'District', 'County', 'MailCity']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['cds'] = tmp_0['cds'].astype(str)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'cds': 'CDSCode'})
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['NumTstTakr'] = pd.to_numeric(tmp_2['NumTstTakr'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['enroll12'] = pd.to_numeric(tmp_3['enroll12'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['CDSCode', 'rtype', 'NumTstTakr', 'school_name', 'district', 'county', 'enroll12']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CDSCode'] = tmp_0['CDSCode'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['MailCity'] = tmp_1['MailCity'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['City'] = tmp_2['City'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['CDSCode', 'School', 'District', 'County', 'MailCity']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='CDSCode')
# Focus on school-level rows and Fresno mailing city; use robust, case-insensitive matching with fallback
mask_school = integrated['rtype'].astype(str).str.upper().eq('S')
# Build a Fresno mask from MailCity when available; fall back to City not included in prepared_table_2 projection, so rely on MailCity only
mailcity = integrated['MailCity'].astype(str)
mask_fresno_mail = mailcity.str.strip().str.casefold().eq('fresno')
filtered = integrated[mask_school & mask_fresno_mail]
# If no rows after strict match, relax to contains 'fresno'
if filtered.empty:
    mask_relaxed = mailcity.str.strip().str.casefold().str.contains('fresno', na=False)
    filtered = integrated[mask_school & mask_relaxed]
# Aggregate total number of test takers across the Fresno-mailing-city schools
filtered['NumTstTakr'] = filtered['NumTstTakr'].astype('Int64')
result = filtered['NumTstTakr'].sum(min_count=1)
# Return as a one-row DataFrame with the answer
target = filtered[['CDSCode']].head(0).copy()
target['total_test_takers_fresno_mailcity'] = [int(result) if result is not pd.NA and pd.notnull(result) else 0]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
