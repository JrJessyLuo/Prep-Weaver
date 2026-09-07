import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'MEET_PLACE', 'func': 'def transform(s):\n    import re\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'MEET_PLACE', 'target_columns': ['BUILDING'], 'func': 'def transform(s):\n    import re\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    s = s.strip()\n    if not s:\n        return [""]\n    # if contains comma, take substring before first comma\n    if "," in s:\n        part = s.split(",", 1)[0].strip()\n    else:\n        # split on 2+ spaces first\n        parts2 = re.split(r"\\s{2,}", s)\n        if len(parts2) > 1:\n            part = parts2[0].strip()\n        else:\n            # fallback: first token before first space\n            part = s.split(" ", 1)[0].strip()\n    # also strip trailing room numbers like -123 or 123\n    part = re.split(r"\\s*-\\s*\\d+", part)[0].strip()\n    return [part]'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING', 'func': 'def transform(s):\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    return s.strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    import re\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'COURSE_NUMBER', 'new_name': 'COURSE'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'RESPONSIBLE_FACULTY_NAME', 'new_name': 'INSTRUCTOR'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_ID', 'COURSE', 'MEET_PLACE', 'BUILDING', 'INSTRUCTOR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'COURSE', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return \'\'\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.upper()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'COURSE_LEVEL', 'target_columns': ['COURSE_LEVEL', 'COURSE_LEVEL_LABEL'], 'func': "def transform(s):\n    val = '' if s is None else str(s).strip().upper()\n    label = 'Graduate' if val == 'G' else ('Undergraduate' if val == 'U' else '')\n    return [val, label]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['COURSE', 'COURSE_LEVEL', 'COURSE_LEVEL_LABEL']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MEET_PLACE'] = tmp_0['MEET_PLACE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    s = s.strip()\n    if not s:\n        return [""]\n    # if contains comma, take substring before first comma\n    if "," in s:\n        part = s.split(",", 1)[0].strip()\n    else:\n        # split on 2+ spaces first\n        parts2 = re.split(r"\\s{2,}", s)\n        if len(parts2) > 1:\n            part = parts2[0].strip()\n        else:\n            # fallback: first token before first space\n            part = s.split(" ", 1)[0].strip()\n    # also strip trailing room numbers like -123 or 123\n    part = re.split(r"\\s*-\\s*\\d+", part)[0].strip()\n    return [part]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['MEET_PLACE'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['BUILDING'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    return s.strip().upper()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['BUILDING'] = tmp_2['BUILDING'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['COURSE_NUMBER'] = tmp_3['COURSE_NUMBER'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'COURSE_NUMBER': 'COURSE'})
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    s = "" if s is None or (isinstance(s,float) and str(s)==\'nan\') else str(s)\n    return s.strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_5['RESPONSIBLE_FACULTY_NAME'] = tmp_5['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'RESPONSIBLE_FACULTY_NAME': 'INSTRUCTOR'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['SUBJECT_ID', 'COURSE', 'MEET_PLACE', 'BUILDING', 'INSTRUCTOR']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return \'\'\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['COURSE'] = tmp_0['COURSE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    val = '' if s is None else str(s).strip().upper()\n    label = 'Graduate' if val == 'G' else ('Undergraduate' if val == 'U' else '')\n    return [val, label]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['COURSE_LEVEL'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['COURSE_LEVEL'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['COURSE_LEVEL_LABEL'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['COURSE', 'COURSE_LEVEL', 'COURSE_LEVEL_LABEL']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='COURSE')

# Keep only rows that have a building identifier present (class takes place in a building)
integrated['BUILDING'] = integrated['BUILDING'].fillna('').str.strip()
filtered = integrated[integrated['BUILDING'] != ''].copy()

# Derive level label with fallback to COURSE_LEVEL if label missing
filtered['LEVEL'] = filtered['COURSE_LEVEL_LABEL']
missing_level = filtered['LEVEL'].isna() | (filtered['LEVEL'].astype(str).str.strip() == '')
filtered.loc[missing_level & (filtered['COURSE_LEVEL'] == 'G'), 'LEVEL'] = 'Graduate'
filtered.loc[missing_level & (filtered['COURSE_LEVEL'] == 'U'), 'LEVEL'] = 'Undergraduate'
# If still missing, assign 'Unknown' so subtotals and totals include them
filtered['LEVEL'] = filtered['LEVEL'].fillna('Unknown')

# Clean instructor names for distinct counts
filtered['INSTRUCTOR_CLEAN'] = filtered['INSTRUCTOR'].fillna('').astype(str).str.strip()

# Aggregations per building and level
by_grp = filtered.groupby(['BUILDING', 'LEVEL'], dropna=False).agg(
    unique_courses=('SUBJECT_ID', lambda s: s.dropna().nunique()),
    total_instructors=('INSTRUCTOR_CLEAN', lambda s: s[s != ''].nunique())
).reset_index()

# Subtotals per building
b_subtot = filtered.groupby(['BUILDING'], dropna=False).agg(
    unique_courses=('SUBJECT_ID', lambda s: s.dropna().nunique()),
    total_instructors=('INSTRUCTOR_CLEAN', lambda s: s[s != ''].nunique())
).reset_index()
b_subtot['LEVEL'] = 'Subtotal'

# Grand total across all buildings and levels
grand_unique_courses = filtered['SUBJECT_ID'].dropna().nunique()
grand_total_instructors = filtered['INSTRUCTOR_CLEAN']
grand_total_instructors = grand_total_instructors[grand_total_instructors != ''].nunique()
grand_df = pd.DataFrame({
    'BUILDING': ['Grand Total'],
    'LEVEL': ['All'],
    'unique_courses': [int(grand_unique_courses)],
    'total_instructors': [int(grand_total_instructors)]
})

# Combine
subtot_expanded = b_subtot[['BUILDING', 'LEVEL', 'unique_courses', 'total_instructors']]
combined = pd.concat([by_grp, subtot_expanded, grand_df], ignore_index=True)

# Sort for readability
combined['is_grand'] = (combined['BUILDING'] == 'Grand Total')
combined['level_order'] = combined['LEVEL'].map({'Undergraduate': 0, 'Graduate': 1, 'Unknown': 2, 'Subtotal': 3, 'All': 4}).fillna(5).astype(int)
combined = combined.sort_values(by=['is_grand', 'BUILDING', 'level_order']).drop(columns=['is_grand', 'level_order'])

# Final projection and rename
combined = combined.rename(columns={'BUILDING': 'Building', 'LEVEL': 'Course Level', 'unique_courses': 'Total Unique Courses', 'total_instructors': 'Total Instructors'})

# Ensure non-empty target even if no buildings matched initially
if combined.empty or set(combined.columns.tolist()) != set(['Building', 'Course Level', 'Total Unique Courses', 'Total Instructors']):
    # Relax: include rows with MEET_PLACE containing building-like text if BUILDING empty
    relaxed = integrated.copy()
    relaxed['BUILDING'] = relaxed['BUILDING'].fillna('').astype(str).str.strip()
    relaxed['MEET_PLACE'] = relaxed['MEET_PLACE'].fillna('').astype(str)
    need_building = relaxed['BUILDING'] == ''
    # Heuristic: take token before first space or full string if short; still require some non-empty text
    inferred = relaxed.loc[need_building & (relaxed['MEET_PLACE'].str.strip() != ''), 'MEET_PLACE'].str.split().str[0].fillna('')
    relaxed.loc[need_building, 'BUILDING'] = inferred
    relaxed = relaxed[relaxed['BUILDING'].str.strip() != '']

    relaxed['LEVEL'] = relaxed['COURSE_LEVEL_LABEL']
    missing_level = relaxed['LEVEL'].isna() | (relaxed['LEVEL'].astype(str).str.strip() == '')
    relaxed.loc[missing_level & (relaxed['COURSE_LEVEL'] == 'G'), 'LEVEL'] = 'Graduate'
    relaxed.loc[missing_level & (relaxed['COURSE_LEVEL'] == 'U'), 'LEVEL'] = 'Undergraduate'
    relaxed['LEVEL'] = relaxed['LEVEL'].fillna('Unknown')
    relaxed['INSTRUCTOR_CLEAN'] = relaxed['INSTRUCTOR'].fillna('').astype(str).str.strip()

    by_grp = relaxed.groupby(['BUILDING', 'LEVEL'], dropna=False).agg(
        unique_courses=('SUBJECT_ID', lambda s: s.dropna().nunique()),
        total_instructors=('INSTRUCTOR_CLEAN', lambda s: s[s != ''].nunique())
    ).reset_index()

    b_subtot = relaxed.groupby(['BUILDING'], dropna=False).agg(
        unique_courses=('SUBJECT_ID', lambda s: s.dropna().nunique()),
        total_instructors=('INSTRUCTOR_CLEAN', lambda s: s[s != ''].nunique())
    ).reset_index()
    b_subtot['LEVEL'] = 'Subtotal'

    grand_unique_courses = relaxed['SUBJECT_ID'].dropna().nunique()
    grand_total_instructors = relaxed['INSTRUCTOR_CLEAN']
    grand_total_instructors = grand_total_instructors[grand_total_instructors != ''].nunique()
    grand_df = pd.DataFrame({
        'BUILDING': ['Grand Total'],
        'LEVEL': ['All'],
        'unique_courses': [int(grand_unique_courses)],
        'total_instructors': [int(grand_total_instructors)]
    })

    combined = pd.concat([by_grp, b_subtot[['BUILDING','LEVEL','unique_courses','total_instructors']], grand_df], ignore_index=True)
    combined['is_grand'] = (combined['BUILDING'] == 'Grand Total')
    combined['level_order'] = combined['LEVEL'].map({'Undergraduate': 0, 'Graduate': 1, 'Unknown': 2, 'Subtotal': 3, 'All': 4}).fillna(5).astype(int)
    combined = combined.sort_values(by=['is_grand', 'BUILDING', 'level_order']).drop(columns=['is_grand', 'level_order'])
    combined = combined.rename(columns={'BUILDING': 'Building', 'LEVEL': 'Course Level', 'unique_courses': 'Total Unique Courses', 'total_instructors': 'Total Instructors'})

# Assign final target
target = combined[['Building', 'Course Level', 'Total Unique Courses', 'Total Instructors']].reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
