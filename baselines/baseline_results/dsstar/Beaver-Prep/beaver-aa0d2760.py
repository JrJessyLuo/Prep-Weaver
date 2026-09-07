import pandas as pd

# Source tables from provided `tables` dict
tip_detail = tables['table_1'].copy()
tip_status = tables['table_2'].copy()
tip_subject = tables['table_5'].copy()

# Normalize keys for joining TIP_DETAIL to TIP_MATERIAL_STATUS (replicating reference logic)
td = tip_detail.copy()
ts = tip_status.copy()

td['__key_norm__'] = td['TIP_MATERIAL_STATUS_KEY'].astype(str).str.strip().str.upper()
ts['__key_norm__'] = ts['tip_material_status_key'].astype(str).str.strip().str.upper()

# Bring in status labels
merged_status = td.merge(
    ts[['__key_norm__', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS']],
    on='__key_norm__',
    how='left',
    suffixes=('', '_status')
)

# Join to bring in NUM_ENROLLED_STUDENTS from TIP_SUBJECT_OFFERED
merged_status['TIP_SUBJECT_OFFERED_KEY'] = merged_status['TIP_SUBJECT_OFFERED_KEY'].astype(object)
tip_subject = tip_subject.copy()
tip_subject['TIP_SUBJECT_OFFERED_KEY'] = tip_subject['TIP_SUBJECT_OFFERED_KEY'].astype(object)

merged_full = merged_status.merge(
    tip_subject[['TIP_SUBJECT_OFFERED_KEY', 'NUM_ENROLLED_STUDENTS']],
    on='TIP_SUBJECT_OFFERED_KEY',
    how='left'
)

# Prepare fields
# Unique materials proxy: TIP_MATERIAL_KEY distinct within status
# Total records: row count within status
# Total enrollment: sum NUM_ENROLLED_STUDENTS with NaN treated as 0 (as in reference)
merged_full['NUM_ENROLLED_STUDENTS_FILL'] = merged_full['NUM_ENROLLED_STUDENTS'].fillna(0)

# Replace NaN status with "No material status" for reporting
status_col = 'TIP_MATERIAL_STATUS'
merged_full[status_col] = merged_full[status_col].fillna('No material status')

# Aggregate
agg_df = (
    merged_full
    .groupby(status_col, dropna=False)
    .agg(
        unique_materials=('TIP_MATERIAL_KEY', pd.Series.nunique),
        total_records=('TIP_MATERIAL_KEY', 'size'),
        total_enrollment=('NUM_ENROLLED_STUDENTS_FILL', 'sum')
    )
    .reset_index()
)

# Grand total row
grand_total = pd.DataFrame({
    status_col: ['Grand Total'],
    'unique_materials': [merged_full['TIP_MATERIAL_KEY'].nunique()],
    'total_records': [len(merged_full)],
    'total_enrollment': [merged_full['NUM_ENROLLED_STUDENTS_FILL'].sum()]
})

# Combine and sort (optional: keep Grand Total as last row)
final_df = pd.concat([agg_df.sort_values(status_col), grand_total], ignore_index=True)

# Ensure column order
final_df = final_df[[status_col, 'unique_materials', 'total_records', 'total_enrollment']]

# Assign to result dict as required
result = {
    'materials_records_enrollment_by_status': final_df
}