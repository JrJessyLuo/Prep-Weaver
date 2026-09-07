import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'transcript_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'student_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date_of_transcript', 'date_format': '%Y-%m-%d %H:%M:%S.%f'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute_value_transcript_details', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['transcript_id', 'student_id', 'date_of_transcript', 'attribute_value_transcript_details']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'class_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'student_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'tid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'cd', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'tid', 'new_name': 'teacher_id'}, {'old_name': 'cd', 'new_name': 'class_desc'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['class_id', 'student_id', 'teacher_id', 'class_desc']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'teacher_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'detail_value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'prefix', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'suffix', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['teacher_id', 'detail_value', 'prefix', 'suffix']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['transcript_id'] = pd.to_numeric(tmp_0['transcript_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['student_id'] = pd.to_numeric(tmp_1['student_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date_of_transcript'] = pd.to_datetime(tmp_2['date_of_transcript'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S.%f')
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['attribute_value_transcript_details'] = tmp_3['attribute_value_transcript_details'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['transcript_id', 'student_id', 'date_of_transcript', 'attribute_value_transcript_details']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['class_id'] = pd.to_numeric(tmp_0['class_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['student_id'] = pd.to_numeric(tmp_1['student_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['tid'] = pd.to_numeric(tmp_2['tid'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['cd'] = tmp_3['cd'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'tid': 'teacher_id', 'cd': 'class_desc'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['class_id', 'student_id', 'teacher_id', 'class_desc']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['teacher_id'] = pd.to_numeric(tmp_0['teacher_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['detail_value'] = tmp_1['detail_value'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['prefix'] = tmp_2['prefix'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['suffix'] = tmp_3['suffix'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['teacher_id', 'detail_value', 'prefix', 'suffix']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='student_id').merge(prepared_table_3, how='left', on='teacher_id')
# Find the earliest transcript issuance date
if not integrated['date_of_transcript'].isna().all():
    min_date = integrated['date_of_transcript'].min()
    earliest = integrated[integrated['date_of_transcript'] == min_date]
else:
    earliest = integrated.copy()
# Select teacher details for the student(s) with earliest transcript
# If teacher details are coded with prefix/suffix, keep them; do not over-filter names
cols = [c for c in ['teacher_id','detail_value','prefix','suffix','student_id','transcript_id','date_of_transcript','class_id','class_desc'] if c in earliest.columns]
target = earliest[cols].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
