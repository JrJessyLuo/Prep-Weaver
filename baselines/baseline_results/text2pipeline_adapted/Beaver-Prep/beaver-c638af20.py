import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TIP_MATERIAL_STATUS_KEY', 'new_name': 'tip_material_status_key'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['subject_id', 'tip_material_status_key', 'RECORD_COUNT']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TIP_MATERIAL_STATUS', 'new_name': 'tip_material_status'}, {'old_name': 'TIP_MATERIAL_STATUS_CODE', 'new_name': 'tip_material_status_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_code', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['tip_material_status_key', 'tip_material_status']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SUBJECT_ID', 'new_name': 'subject_id'}, {'old_name': 'OFFER_DEPT_NAME', 'new_name': 'offer_dept_name'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s, float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'offer_dept_name', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s, float) and pd.isna(s)) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['subject_id', 'offer_dept_name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'new_name': 'library_material_status_key'}, {'old_name': 'SUBJECT_ID', 'new_name': 'subject_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'library_material_status_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['subject_id', 'library_material_status_key']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'new_name': 'library_material_status_key'}, {'old_name': 'LIBRARY_MATERIAL_STATUS', 'new_name': 'library_material_status'}, {'old_name': 'LIBRARY_MATERIAL_STATUS_CODE', 'new_name': 'library_material_status_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'library_material_status_key', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'library_material_status_code', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'library_material_status', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['library_material_status_key', 'library_material_status']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME', 'DEPT_BUDGET_CODE', 'IS_DEGREE_GRANTING', 'DEPT_NAME_IN_COMMENCEMENT_BK', 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'DEPARTMENT_NAME_HISTORY', 'DEPARTMENT_LAST_ACTIVITY_DATE', 'DLC_KEY', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

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
    tmp_2['subject_id'] = tmp_2['subject_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['TIP_SUBJECT_OFFERED_KEY'] = tmp_3['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['RECORD_COUNT'] = pd.to_numeric(tmp_4['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['subject_id', 'tip_material_status_key', 'RECORD_COUNT']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TIP_MATERIAL_STATUS': 'tip_material_status', 'TIP_MATERIAL_STATUS_CODE': 'tip_material_status_code'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['tip_material_status_key'] = tmp_1['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['tip_material_status_code'] = tmp_2['tip_material_status_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['tip_material_status'] = tmp_3['tip_material_status'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['tip_material_status_key', 'tip_material_status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'SUBJECT_ID': 'subject_id', 'OFFER_DEPT_NAME': 'offer_dept_name'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s, float) and pd.isna(s)) else str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['subject_id'] = tmp_1['subject_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s, float) and pd.isna(s)) else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['offer_dept_name'] = tmp_2['offer_dept_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['subject_id', 'offer_dept_name']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'LIBRARY_MATERIAL_STATUS_KEY': 'library_material_status_key', 'SUBJECT_ID': 'subject_id'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['library_material_status_key'] = tmp_1['library_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['subject_id'] = tmp_2['subject_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['subject_id', 'library_material_status_key']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_4', pd.DataFrame()))

def _prepare_table_5(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'LIBRARY_MATERIAL_STATUS_KEY': 'library_material_status_key', 'LIBRARY_MATERIAL_STATUS': 'library_material_status', 'LIBRARY_MATERIAL_STATUS_CODE': 'library_material_status_code'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['library_material_status_key'] = tmp_1['library_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['library_material_status_code'] = tmp_2['library_material_status_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['library_material_status'] = tmp_3['library_material_status'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['library_material_status_key', 'library_material_status']].copy()
    return result

prepared_table_5 = _prepare_table_5(tables.get('table_3', pd.DataFrame()))

def _prepare_table_6(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'department_full_name', 'SCHOOL_CODE', 'SCHOOL_NAME', 'DEPT_BUDGET_CODE', 'IS_DEGREE_GRANTING', 'DEPT_NAME_IN_COMMENCEMENT_BK', 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'DEPARTMENT_NAME_HISTORY', 'DEPARTMENT_LAST_ACTIVITY_DATE', 'DLC_KEY', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_6 = _prepare_table_6(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
## TIP: join fact to status and to offerings for department
_tip = prepared_table_1.copy()
# Join to TIP status for human-readable label
_tip = _tip.merge(prepared_table_2, how='left', on='tip_material_status_key')
# Join to offerings to get department
_tip = _tip.merge(prepared_table_3, how='left', on='subject_id')
# Aggregate TIP counts by department and material status
# Use RECORD_COUNT when available; if missing, count rows
if 'RECORD_COUNT' in _tip.columns:
    _tip['tip_count'] = _tip['RECORD_COUNT']
else:
    _tip['tip_count'] = 1
_tip_grouped = _tip.groupby(['offer_dept_name', 'tip_material_status'], dropna=False, as_index=False)['tip_count'].sum()

## Library: join fact to status and to offerings for department
_lib = prepared_table_4.copy()
_lib = _lib.merge(prepared_table_5, how='left', on='library_material_status_key')
_lib = _lib.merge(prepared_table_3, how='left', on='subject_id')
# Each row represents a library material; count rows per dept/status
_lib['library_count'] = 1
_lib_grouped = _lib.groupby(['offer_dept_name', 'library_material_status'], dropna=False, as_index=False)['library_count'].sum()

## Create a unified set of department x status labels
# We'll consider material status label as a common dimension by forming the union of labels from TIP and Library.
# To present side-by-side, align on department and a single status label column. Prefer non-null labels; if null, use a placeholder.
_tip_grouped['status_label'] = _tip_grouped['tip_material_status']
_lib_grouped['status_label'] = _lib_grouped['library_material_status']

# Build all combinations appearing in either side
_tip_sel = _tip_grouped[['offer_dept_name', 'status_label', 'tip_count']]
_lib_sel = _lib_grouped[['offer_dept_name', 'status_label', 'library_count']]
all_keys = (_tip_sel[['offer_dept_name', 'status_label']]
            .merge(_lib_sel[['offer_dept_name', 'status_label']], how='outer', on=['offer_dept_name','status_label']))

# Merge counts
combined = all_keys.merge(_tip_sel, how='left', on=['offer_dept_name','status_label']) \
                   .merge(_lib_sel, how='left', on=['offer_dept_name','status_label'])

# Fill missing counts with 0
combined['tip_count'] = combined['tip_count'].fillna(0).astype(int)
combined['library_count'] = combined['library_count'].fillna(0).astype(int)
combined['total_count'] = combined['tip_count'] + combined['library_count']

# For readability, rename columns to match requested output labels
combined = combined.rename(columns={'offer_dept_name': 'department_name', 'status_label': 'material_status'})

# Department subtotals
dept_subtotals = combined.groupby('department_name', as_index=False).agg({
    'tip_count':'sum', 'library_count':'sum', 'total_count':'sum'
})
dept_subtotals['material_status'] = 'Subtotal'

# Grand total
grand_total = combined[['tip_count','library_count','total_count']].sum().to_frame().T
grand_total['department_name'] = 'Grand Total'
grand_total['material_status'] = 'Grand Total'
# Reorder columns
grand_total = grand_total[['department_name','material_status','tip_count','library_count','total_count']]

# Concatenate detail, subtotals, and grand total
detail = combined[['department_name','material_status','tip_count','library_count','total_count']]
# Sort detail by department then material_status (placing Subtotal later when concatenated)
detail = detail.sort_values(['department_name','material_status'], kind='mergesort')

with_subtotals = (
    pd.concat([detail, dept_subtotals[['department_name','material_status','tip_count','library_count','total_count']]], ignore_index=True)
    .sort_values(['department_name', 'material_status'], kind='mergesort')
)

# Append grand total at the end
target = pd.concat([with_subtotals, grand_total], ignore_index=True)

# Final column order is already set

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
