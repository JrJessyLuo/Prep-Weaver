import pandas as pd

# The input tables are provided in `tables` dict:
# tables['table_1'] -> TIP_DETAIL.pkl
# tables['table_2'] -> LIBRARY_RESERVE_MATRL_DETAIL.pkl
# tables['table_3'] -> LIBRARY_RESERVE_CATALOG.pkl
# tables['table_4'] -> TIP_MATERIAL.pkl
# tables['table_5'] -> TIP_MATERIAL_STATUS.pkl
# tables['table_6'] -> TIP_SUBJECT_OFFERED.pkl
# tables['table_7'] -> LIBRARY_COURSE_INSTRUCTOR.pkl
# tables['table_8'] -> LIBRARY_SUBJECT_OFFERED.pkl
# tables['table_9'] -> LIBRARY_MATERIAL_STATUS.pkl

# 1) Load from provided dict
tip_detail = tables['table_1'].copy()
lib_reserve_detail = tables['table_2'].copy()
lib_reserve_catalog = tables['table_3'].copy()
tip_material = tables['table_4'].copy()
tip_material_status = tables['table_5'].copy()
tip_subject_offered = tables['table_6'].copy()
lib_course_instructor = tables['table_7'].copy()
lib_subject_offered = tables['table_8'].copy()
lib_material_status = tables['table_9'].copy()

# 2) Standardize status key name (same as reference logic)
if 'tip_material_status_key' in tip_material_status.columns:
    tip_material_status = tip_material_status.rename(columns={"tip_material_status_key": "TIP_MATERIAL_STATUS_KEY"})

# 3) Select/retain only needed columns from material and status
mat_cols_keep = [
    "TIP_MATERIAL_KEY", "ISBN", "TITLE", "AUTHOR", "EDITION", "PUBLISHER", "YEAR",
    "NEW_SHELF_PRICE", "USED_SHELF_PRICE", "RENTAL_NEW_PRICE", "RENTAL_USED_PRICE", "MATERIAL_INFO_SOURCE"
]
tip_material_trim = tip_material.loc[:, [c for c in mat_cols_keep if c in tip_material.columns]].copy()

status_cols_keep = ["TIP_MATERIAL_STATUS_KEY", "TIP_MATERIAL_STATUS_CODE", "TIP_MATERIAL_STATUS"]
tip_material_status_trim = tip_material_status.loc[:, [c for c in status_cols_keep if c in tip_material_status.columns]].copy()

# 4) Join TIP_DETAIL -> TIP_MATERIAL on TIP_MATERIAL_KEY
merged = tip_detail.merge(
    tip_material_trim,
    how="left",
    on="TIP_MATERIAL_KEY",
    validate="m:1"
)

# 5) Join status attributes from TIP_MATERIAL_STATUS on TIP_MATERIAL_STATUS_KEY
merged = merged.merge(
    tip_material_status_trim,
    how="left",
    on="TIP_MATERIAL_STATUS_KEY",
    validate="m:1"
)

# 6) Determine department name
# Prefer TIP_SUBJECT_OFFERED if available, else fall back to LIBRARY_SUBJECT_OFFERED
# Harmonize subject key for joins
# TIP paths: TIP_DETAIL.subject_id -> TIP_SUBJECT_OFFERED.subject_id => department (e.g., DEPT or DEPARTMENT_NAME)
# Library paths: LIBRARY_RESERVE_DETAIL might link to LIBRARY_SUBJECT_OFFERED via subject/course keys; however,
# to satisfy question by department for TIP materials, we use TIP side department info.
dept_cols_candidates = ['DEPARTMENT', 'DEPT', 'DEPARTMENT_NAME', 'SCHOOL', 'DIVISION']
tip_dept_df = tip_subject_offered.copy()
dept_col = None
for c in dept_cols_candidates:
    if c in tip_dept_df.columns:
        dept_col = c
        break
if dept_col is None:
    # If no clear department column exists, fall back to subject_id itself as department proxy
    dept_col = 'subject_id'
if 'subject_id' not in tip_dept_df.columns and 'SUBJECT_ID' in tip_dept_df.columns:
    tip_dept_df = tip_dept_df.rename(columns={'SUBJECT_ID': 'subject_id'})

tip_dept_df = tip_dept_df[['subject_id', dept_col]].drop_duplicates()

merged = merged.merge(
    tip_dept_df,
    how='left',
    on='subject_id'
)

# 7) Map Library availability:
# Need to know if a TIP material (ISBN/title) is available in library reserves for a given term.
# Use LIBRARY_RESERVE_MATRL_DETAIL join to LIBRARY_RESERVE_CATALOG to get ISBN/title and term.
lib_cat = lib_reserve_catalog.copy()
lib_det = lib_reserve_detail.copy()

# Try to align keys between detail and catalog (commonly a catalog key)
join_key_candidates = []
for k in ['CATALOG_KEY', 'LIBRARY_CATALOG_KEY', 'CATALOG_ID', 'CATALOG_ROW_ID', 'RESERVE_CATALOG_KEY']:
    if k in lib_det.columns and k in lib_cat.columns:
        join_key_candidates.append(k)
        break

if join_key_candidates:
    k = join_key_candidates[0]
    lib_joined = lib_det.merge(lib_cat, how='left', on=k)
else:
    # If no shared key, attempt a looser alignment via ISBN and TERM_CODE if present in both
    common_cols = [c for c in ['ISBN', 'TERM_CODE'] if c in lib_det.columns and c in lib_cat.columns]
    if common_cols:
        lib_joined = lib_det.merge(lib_cat, how='left', on=common_cols)
    else:
        # Fallback to using catalog alone for availability footprint
        lib_joined = lib_cat.copy()

# Normalize ISBN columns for matching
def std_isbn(s):
    if pd.isna(s):
        return pd.NA
    s = str(s)
    return ''.join(ch for ch in s if ch.isdigit() or ch.upper()=='X')

if 'ISBN' in merged.columns:
    merged['ISBN_STD'] = merged['ISBN'].map(std_isbn)
else:
    merged['ISBN_STD'] = pd.NA

lib_isbn_col = 'ISBN'
if lib_isbn_col not in lib_joined.columns:
    # see if another isbn-like column exists
    for c in lib_joined.columns:
        if c.upper() == 'ISBN':
            lib_isbn_col = c
            break
lib_joined['ISBN_STD'] = lib_joined[lib_isbn_col].map(std_isbn) if lib_isbn_col in lib_joined.columns else pd.NA

# Standardize term codes
tip_term_col = 'TERM_CODE' if 'TERM_CODE' in merged.columns else None
lib_term_col = None
for c in ['TERM_CODE', 'LIB_TERM_CODE', 'TERM', 'LIBRARY_TERM_CODE']:
    if c in lib_joined.columns:
        lib_term_col = c
        break

# Create a library availability frame keyed by ISBN_STD and term (if term available)
lib_avail_cols = ['ISBN_STD']
if lib_term_col:
    lib_avail_cols.append(lib_term_col)
lib_availability = lib_joined.dropna(subset=['ISBN_STD']) if 'ISBN_STD' in lib_joined.columns else lib_joined.copy()
lib_availability = lib_availability.loc[:, list(dict.fromkeys(lib_avail_cols))].drop_duplicates()
lib_availability['Available_in_Library_Flag'] = 1

# Join availability to merged on ISBN and term if both present, else on ISBN only
if tip_term_col and lib_term_col:
    merged = merged.merge(
        lib_availability,
        how='left',
        left_on=['ISBN_STD', tip_term_col],
        right_on=['ISBN_STD', lib_term_col]
    )
else:
    merged = merged.merge(
        lib_availability[['ISBN_STD', 'Available_in_Library_Flag']],
        how='left',
        on='ISBN_STD'
    )

# Availability label
merged['Library_Availability'] = merged['Available_in_Library_Flag'].fillna(0).astype(int).map({1: 'Available in Library', 0: 'Not Available in Library'})

# 8) Instructor counts per library book (by department and material)
# We need to count instructors per "library book" for the department.
# Use LIBRARY_COURSE_INSTRUCTOR; align department via LIBRARY_SUBJECT_OFFERED if possible.
lib_subj = lib_subject_offered.copy()

# Harmonize subject_id and department in library set
lib_dept_col = None
for c in dept_cols_candidates:
    if c in lib_subj.columns:
        lib_dept_col = c
        break
if lib_dept_col is None and 'subject_id' in lib_subj.columns:
    lib_dept_col = 'subject_id'
if 'subject_id' not in lib_subj.columns and 'SUBJECT_ID' in lib_subj.columns:
    lib_subj = lib_subj.rename(columns={'SUBJECT_ID': 'subject_id'})

lib_dept_map = lib_subj[['subject_id', lib_dept_col]].drop_duplicates() if lib_dept_col else pd.DataFrame(columns=['subject_id'])

# Link instructors to department via subject_id if present
instr = lib_course_instructor.copy()
# Try to find a subject_id/course key in instructor table to map department
subject_key_in_instr = None
for c in ['subject_id', 'SUBJECT_ID']:
    if c in instr.columns:
        subject_key_in_instr = c
        break
if subject_key_in_instr == 'SUBJECT_ID':
    instr = instr.rename(columns={'SUBJECT_ID': 'subject_id'})
    subject_key_in_instr = 'subject_id'

if subject_key_in_instr and not lib_dept_map.empty:
    instr = instr.merge(lib_dept_map, how='left', on='subject_id')
else:
    # If no mapping possible, we won't be able to break out instructors by department accurately.
    # We'll proceed with no department on instructors; counts will be missing.
    instr[lib_dept_col if lib_dept_col else 'DEPARTMENT_FALLBACK'] = pd.NA

# Count instructors per department and ISBN (normalize ISBN in instructor side if present)
instr_isbn_col = None
for c in ['ISBN', 'isbn']:
    if c in instr.columns:
        instr_isbn_col = c
        break
if instr_isbn_col is not None:
    instr['ISBN_STD'] = instr[instr_isbn_col].map(std_isbn)
else:
    instr['ISBN_STD'] = pd.NA

# Choose department column name unified to 'DEPARTMENT_NAME'
dept_output_col = 'DEPARTMENT_NAME'
if dept_col != dept_output_col:
    merged = merged.rename(columns={dept_col: dept_output_col})
if lib_dept_col and lib_dept_col != dept_output_col:
    instr = instr.rename(columns={lib_dept_col: dept_output_col})

# Instructor unique id column candidates
instr_id_col = None
for c in ['INSTRUCTOR_ID', 'PERSON_ID', 'KERB_ID', 'EMAIL', 'INSTRUCTOR_NAME']:
    if c in instr.columns:
        instr_id_col = c
        break
# If none found, count distinct rows as instructors
if instr_id_col is None:
    instr['__instr_uid__'] = pd.util.hash_pandas_object(instr.astype(str), index=False)
    instr_id_col = '__instr_uid__'

instr_counts = (
    instr.dropna(subset=['ISBN_STD', dept_output_col])[
        [dept_output_col, 'ISBN_STD', instr_id_col]
    ].drop_duplicates()
    .groupby([dept_output_col, 'ISBN_STD'], as_index=False)
    .agg(Total_Instructors_Per_Book=('{}'.format(instr_id_col), 'nunique'))
)

# 9) Total number of materials available in library per department
avail_per_dept = (
    merged.assign(AvailFlag=(merged['Library_Availability'] == 'Available in Library').astype(int))
    .groupby(dept_output_col, as_index=False)
    .agg(Total_Materials_Available_in_Department=('AvailFlag', 'sum'))
)

# 10) Total number of available materials across all departments
total_available_across = int((merged['Library_Availability'] == 'Available in Library').sum())

# 11) Build final output table
# Fields required:
# - department name
# - title
# - author
# - ISBN
# - library term code
# - availability label
# - total number of instructors per library book for the department
# - total number of materials available in the department
# - total number of available materials across all departments
out_cols = []
for c in [dept_output_col, 'TITLE', 'AUTHOR', 'ISBN', 'TERM_CODE', 'Library_Availability']:
    if c in merged.columns:
        out_cols.append(c)

final = merged.loc[:, out_cols].copy()
# Attach normalized ISBN for joining instructor counts
final['ISBN_STD'] = merged['ISBN_STD']

# Join instructor counts
final = final.merge(
    instr_counts,
    how='left',
    left_on=[dept_output_col, 'ISBN_STD'],
    right_on=[dept_output_col, 'ISBN_STD']
)

# Join department availability totals
final = final.merge(
    avail_per_dept,
    how='left',
    on=dept_output_col
)

# Add total available materials across all departments as a constant column
final['Total_Available_Materials_All_Departments'] = total_available_across

# Clean up/rename output columns to match question phrasing
rename_map = {
    dept_output_col: 'Department',
    'TITLE': 'TIP_Material_Title',
    'AUTHOR': 'Author',
    'ISBN': 'ISBN',
    'TERM_CODE': 'Library_Term_Code',
    'Library_Availability': 'Library_Availability',
    'Total_Instructors_Per_Book': 'Total_Instructors_Per_Library_Book_in_Department',
    'Total_Materials_Available_in_Department': 'Total_Materials_Available_in_Department',
    'Total_Available_Materials_All_Departments': 'Total_Available_Materials_All_Departments'
}
final = final.rename(columns=rename_map)

# Select and order final columns
final_cols = [
    'Department',
    'TIP_Material_Title',
    'Author',
    'ISBN',
    'Library_Term_Code',
    'Library_Availability',
    'Total_Instructors_Per_Library_Book_in_Department',
    'Total_Materials_Available_in_Department',
    'Total_Available_Materials_All_Departments'
]
final = final.loc[:, [c for c in final_cols if c in final.columns]].drop_duplicates()

# Assign to result dict as required
result = {"department_tip_material_library_summary": final}