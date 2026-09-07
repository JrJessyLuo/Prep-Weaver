import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TIP_SUBJECT_OFFERED_KEY', 'new_name': 'TIP_SUBJECT_OFFERED_KEY'}, {'old_name': 'MASTER_COURSE_NUMBER', 'new_name': 'MASTER_COURSE_NUMBER'}, {'old_name': 'MASTER_SUBJECT_ID', 'new_name': 'MASTER_SUBJECT_ID'}, {'old_name': 'OFFER_DEPT_NAME', 'new_name': 'OFFER_DEPT_NAME'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MASTER_COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MASTER_SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'MASTER_COURSE_NUMBER', 'MASTER_SUBJECT_ID', 'OFFER_DEPT_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NEW_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_KEY', 'NEW_SHELF_PRICE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TIP_SUBJECT_OFFERED_KEY': 'TIP_SUBJECT_OFFERED_KEY', 'MASTER_COURSE_NUMBER': 'MASTER_COURSE_NUMBER', 'MASTER_SUBJECT_ID': 'MASTER_SUBJECT_ID', 'OFFER_DEPT_NAME': 'OFFER_DEPT_NAME'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TIP_SUBJECT_OFFERED_KEY'] = tmp_1['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['MASTER_COURSE_NUMBER'] = tmp_2['MASTER_COURSE_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['MASTER_SUBJECT_ID'] = tmp_3['MASTER_SUBJECT_ID'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['OFFER_DEPT_NAME'] = tmp_4['OFFER_DEPT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'MASTER_COURSE_NUMBER', 'MASTER_SUBJECT_ID', 'OFFER_DEPT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_KEY'] = tmp_1['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TIP_MATERIAL_STATUS_KEY'] = tmp_2['TIP_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['TERM_CODE'] = tmp_3['TERM_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['subject_id'] = tmp_4['subject_id'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['ISBN'] = tmp_5['ISBN'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_MATERIAL_KEY'] = tmp_0['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['NEW_SHELF_PRICE'] = pd.to_numeric(tmp_1['NEW_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['TIP_MATERIAL_KEY', 'NEW_SHELF_PRICE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge all prepared tables
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='TIP_SUBJECT_OFFERED_KEY').merge(prepared_table_3, how='left', on='TIP_MATERIAL_KEY')

# Ensure key columns exist
integrated['SUBJECT_KEY'] = integrated['TIP_SUBJECT_OFFERED_KEY']

# Aggregate by department and master course
grp_cols = ['OFFER_DEPT_NAME', 'MASTER_COURSE_NUMBER']
agg = (
    integrated.groupby(grp_cols, dropna=False)
    .agg(
        num_subjects=('SUBJECT_KEY', 'nunique'),
        total_new_shelf_price=('NEW_SHELF_PRICE', 'sum'),
        num_unique_tip_materials=('TIP_MATERIAL_KEY', 'nunique')
    )
    .reset_index()
)

# Fill NaNs and coerce numeric
for c in ['total_new_shelf_price', 'num_subjects', 'num_unique_tip_materials']:
    agg[c] = agg[c].fillna(0)

# Sort by department then master course
agg = agg.sort_values(by=['OFFER_DEPT_NAME', 'MASTER_COURSE_NUMBER'], kind='stable').reset_index(drop=True)

# Department subtotals
dept_sub = (
    agg.groupby('OFFER_DEPT_NAME', dropna=False)
    .agg(
        num_subjects=('num_subjects', 'sum'),
        total_new_shelf_price=('total_new_shelf_price', 'sum'),
        num_unique_tip_materials=('num_unique_tip_materials', 'sum')
    )
    .reset_index()
)

# Grand total
grand = dept_sub.copy()
grand['OFFER_DEPT_NAME'] = 'Grand Total'
grand = grand.groupby('OFFER_DEPT_NAME', as_index=False).agg(
    num_subjects=('num_subjects', 'sum'),
    total_new_shelf_price=('total_new_shelf_price', 'sum'),
    num_unique_tip_materials=('num_unique_tip_materials', 'sum')
)

# Prepare display columns: blank repeats within department
agg_display = agg.copy()
agg_display['DEPARTMENT_DISPLAY'] = agg_display['OFFER_DEPT_NAME']
agg_display['MASTER_COURSE_DISPLAY'] = agg_display['MASTER_COURSE_NUMBER']
mask_same_dept_as_prev = agg_display['OFFER_DEPT_NAME'].eq(agg_display['OFFER_DEPT_NAME'].shift())
agg_display.loc[mask_same_dept_as_prev, 'DEPARTMENT_DISPLAY'] = ''
# Only show master course on first occurrence within department
agg_display.loc[mask_same_dept_as_prev, 'MASTER_COURSE_DISPLAY'] = ''

# Department subtotal display rows
dept_sub_disp = dept_sub.copy()
dept_sub_disp['DEPARTMENT_DISPLAY'] = dept_sub_disp['OFFER_DEPT_NAME'] + ' Subtotal'
dept_sub_disp['MASTER_COURSE_DISPLAY'] = ''

# Assemble rows per department with subtotal after each group
rows = []
for dept in agg_display['OFFER_DEPT_NAME'].dropna().unique().tolist() + ([] if agg_display['OFFER_DEPT_NAME'].isna().sum()==0 else [None]):
    if dept is None:
        part = agg_display[agg_display['OFFER_DEPT_NAME'].isna()]
        sub = dept_sub_disp[dept_sub_disp['OFFER_DEPT_NAME'].isna()].copy()
    else:
        part = agg_display[agg_display['OFFER_DEPT_NAME'] == dept]
        sub = dept_sub_disp[dept_sub_disp['OFFER_DEPT_NAME'] == dept].copy()
    if len(part) == 0 and len(sub) == 0:
        continue
    # Align columns for concatenation
    part = part[['DEPARTMENT_DISPLAY', 'MASTER_COURSE_DISPLAY', 'num_subjects', 'total_new_shelf_price', 'num_unique_tip_materials']]
    sub = sub[['DEPARTMENT_DISPLAY', 'MASTER_COURSE_DISPLAY', 'num_subjects', 'total_new_shelf_price', 'num_unique_tip_materials']]
    rows.append(part)
    rows.append(sub)

# Concatenate detailed rows
if rows:
    detailed = rows[0].iloc[0:0]
    for r in rows:
        detailed = pd.concat([detailed, r], axis=0, ignore_index=True)
else:
    detailed = agg_display[['DEPARTMENT_DISPLAY', 'MASTER_COURSE_DISPLAY', 'num_subjects', 'total_new_shelf_price', 'num_unique_tip_materials']].copy()

# Append grand total
grand_disp = grand.copy()
grand_disp['DEPARTMENT_DISPLAY'] = grand_disp['OFFER_DEPT_NAME']
grand_disp['MASTER_COURSE_DISPLAY'] = ''
grand_disp = grand_disp[['DEPARTMENT_DISPLAY', 'MASTER_COURSE_DISPLAY', 'num_subjects', 'total_new_shelf_price', 'num_unique_tip_materials']]

detailed = pd.concat([detailed, grand_disp], ignore_index=True)

# Round and format integers with thousands separators
for c in ['num_subjects', 'total_new_shelf_price', 'num_unique_tip_materials']:
    detailed[c] = detailed[c].fillna(0).round(0).astype('int64').map(lambda x: f"{x:,}")

# Final projection and rename
target = detailed.rename(columns={
    'DEPARTMENT_DISPLAY': 'Department',
    'MASTER_COURSE_DISPLAY': 'Master Course',
    'num_subjects': 'Number of Subjects',
    'total_new_shelf_price': 'Total New Shelf Price (TIP Materials)',
    'num_unique_tip_materials': 'Number of Unique TIP Materials'
})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
