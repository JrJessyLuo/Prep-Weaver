import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_CATEGORY_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SPONSOR_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SESSION_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SPONSOR_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SPONSOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPONSOR_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'iap_subject_session_key', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_START_TIME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'iap_subject_session_key', 'new_name': 'IAP_SUBJECT_SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY', 'SESSION_START_TIME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['IAP_SUBJECT_SPONSOR_KEY'] = tmp_1['IAP_SUBJECT_SPONSOR_KEY'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['IAP_SUBJECT_SESSION_KEY'] = tmp_2['IAP_SUBJECT_SESSION_KEY'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['TERM_CODE'] = tmp_3['TERM_CODE'].astype(str)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['IAP_SUBJECT_CATEGORY_KEY'] = tmp_4['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['IAP_SUBJECT_SPONSOR_KEY'] = tmp_5['IAP_SUBJECT_SPONSOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_SPONSOR_KEY'] = tmp_0['IAP_SUBJECT_SPONSOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SPONSOR_NAME'] = tmp_1['SPONSOR_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['iap_subject_session_key'] = tmp_0['iap_subject_session_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SESSION_START_TIME'] = tmp_1['SESSION_START_TIME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'iap_subject_session_key': 'IAP_SUBJECT_SESSION_KEY'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_SESSION_KEY', 'SESSION_START_TIME']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
merged = prepared_table_1.merge(prepared_table_2, on='IAP_SUBJECT_CATEGORY_KEY', how='left').merge(prepared_table_3, on='IAP_SUBJECT_SPONSOR_KEY', how='left').merge(prepared_table_4, on='IAP_SUBJECT_SESSION_KEY', how='left')
# Compute beginning and end term per category
term_agg = merged.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], dropna=False)['TERM_CODE'].agg(['min','max']).reset_index().rename(columns={'min':'begin_term','max':'end_term'})
term_agg['active_period'] = term_agg.apply(lambda r: (str(r['begin_term']) + '-' + str(r['end_term'])) if (r['begin_term'] is not None and r['end_term'] is not None) else None, axis=1)
# Unique sessions per category: count distinct IAP_SUBJECT_SESSION_KEY
sess_counts = merged.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], dropna=False)['IAP_SUBJECT_SESSION_KEY'].nunique().reset_index().rename(columns={'IAP_SUBJECT_SESSION_KEY':'num_unique_sessions'})
# Total attendees proxy: count of rows (attendee records unavailable); use number of activity-person rows if duplicates exist; fall back to counting rows per category
att_counts = merged.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], dropna=False).size().reset_index(name='total_attendees')
# Most common sponsor name per category
sponsor_mode = merged.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','SPONSOR_NAME'], dropna=False).size().reset_index(name='cnt')
sponsor_mode = sponsor_mode.sort_values(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','cnt','SPONSOR_NAME'], ascending=[True,True,False,True]).groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], as_index=False).first()[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','SPONSOR_NAME']].rename(columns={'SPONSOR_NAME':'most_common_sponsor'})
# Most common session start time per category
start_mode = merged.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','SESSION_START_TIME'], dropna=False).size().reset_index(name='cnt')
start_mode = start_mode.sort_values(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','cnt','SESSION_START_TIME'], ascending=[True,True,False,True]).groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], as_index=False).first()[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','SESSION_START_TIME']].rename(columns={'SESSION_START_TIME':'most_common_start_time'})
# Combine per-category results
cat = sess_counts.merge(att_counts, on=['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], how='left')\
          .merge(term_agg[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME','active_period']], on=['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], how='left')\
          .merge(sponsor_mode, on=['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], how='left')\
          .merge(start_mode, on=['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME'], how='left')
# Final projection per category
cat = cat[['IAP_CATEGORY_NAME','num_unique_sessions','total_attendees','active_period','most_common_sponsor','most_common_start_time']]
# Grand total row
total_sessions = sess_counts['num_unique_sessions'].sum()
total_attendees = att_counts['total_attendees'].sum()
grand = cat.iloc[0:0].copy()
grand.loc[0,'IAP_CATEGORY_NAME'] = 'TOTAL'
grand.loc[0,'num_unique_sessions'] = total_sessions
grand.loc[0,'total_attendees'] = total_attendees
grand.loc[0,'active_period'] = None
grand.loc[0,'most_common_sponsor'] = None
grand.loc[0,'most_common_start_time'] = None
# Append total
target = pd.concat([cat, grand], ignore_index=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
