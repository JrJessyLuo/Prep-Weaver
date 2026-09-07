import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TIP_MATERIAL_STATUS_KEY', 'new_name': 'tip_material_status_key'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['tip_material_status_key', 'TIP_MATERIAL_KEY', 'TERM_CODE', 'subject_id', 'ISBN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['tip_material_status_key', 'TIP_MATERIAL_STATUS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'TERM_CODE', 'target_columns': ['PUB_YEAR', '_discard_termcode_tail'], 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    s = s.strip().upper()\n    if len(s) >= 4 and s[:4].isdigit():\n        return [int(s[:4]), s[4:]]\n    return [None, s]'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_discard_termcode_tail']}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SUBJECT_ID', 'new_name': 'subject_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['subject_id', 'TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'PUB_YEAR']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TIP_MATERIAL_STATUS_KEY': 'tip_material_status_key'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['tip_material_status_key'] = tmp_1['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['TIP_MATERIAL_KEY'] = tmp_2['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['TERM_CODE'] = tmp_3['TERM_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['subject_id'] = tmp_4['subject_id'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['ISBN'] = tmp_5['ISBN'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['RECORD_COUNT'] = pd.to_numeric(tmp_6['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['tip_material_status_key', 'TIP_MATERIAL_KEY', 'TERM_CODE', 'subject_id', 'ISBN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['tip_material_status_key'] = tmp_0['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_STATUS_CODE'] = tmp_1['TIP_MATERIAL_STATUS_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TIP_MATERIAL_STATUS'] = tmp_2['TIP_MATERIAL_STATUS'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['tip_material_status_key', 'TIP_MATERIAL_STATUS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_ID'] = tmp_0['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['DEPARTMENT_CODE'] = tmp_2['DEPARTMENT_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['DEPARTMENT_NAME'] = tmp_3['DEPARTMENT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    s = s.strip().upper()\n    if len(s) >= 4 and s[:4].isdigit():\n        return [int(s[:4]), s[4:]]\n    return [None, s]', globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_4['TERM_CODE'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['PUB_YEAR'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['_discard_termcode_tail'] = _split_values_5.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: DropColumn
    tmp_5 = tmp_4.drop(columns=['_discard_termcode_tail'], errors='ignore').copy()
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'SUBJECT_ID': 'subject_id'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['subject_id', 'TERM_CODE', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'PUB_YEAR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_3, how='left', on=['subject_id','TERM_CODE'])
integrated = integrated.merge(prepared_table_2, how='left', on='tip_material_status_key')
# Derive material identifier preference: use TIP_MATERIAL_KEY primarily, fallback to ISBN
integrated['material_id'] = integrated['TIP_MATERIAL_KEY'].where(integrated['TIP_MATERIAL_KEY'].notna() & (integrated['TIP_MATERIAL_KEY'].str.len()>0), integrated['ISBN'])
# Group by status key and label
grp_cols = ['tip_material_status_key','TIP_MATERIAL_STATUS']
agg = integrated.groupby(grp_cols).agg(
    total_materials = ('material_id', lambda s: s.dropna().astype(str).str.strip().replace({'': None}).dropna().nunique()),
    total_subjects = ('subject_id', lambda s: s.dropna().astype(str).str.strip().replace({'': None}).dropna().nunique()),
    total_schools = ('DEPARTMENT_NAME', lambda s: s.dropna().astype(str).str.strip().replace({'': None}).dropna().nunique()),
    most_recent_publication_year = ('PUB_YEAR', 'max')
).reset_index()
# Prepare final projection with readable material status; keep key for audit but prioritize label
target = agg[['TIP_MATERIAL_STATUS','total_materials','total_subjects','total_schools','most_recent_publication_year']].rename(columns={'TIP_MATERIAL_STATUS':'material_status'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
