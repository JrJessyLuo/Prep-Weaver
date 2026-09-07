import pandas as pd

# The input tables are provided in scope as `tables` (a dict of DataFrames).
# We will construct DataFrames corresponding to the schema in the reference code
# using the available tables, then reproduce the same join logic in pandas.

# Map the provided tables to the schema names used in the reference SQL
# Assumptions based on typical column names:
# - activities: SUBJECT_OFFERED (table_10)
# - locations: DRUPAL_COURSE_CATALOG (table_5) [using 'location' or similar fields if present]
# - supervisors: SIS_COURSE_DESCRIPTION (table_9) [using instructor fields as supervisor proxy]
# - terms: ACADEMIC_TERMS_ALL (table_8)
# - assignments: IAP_SUBJECT_SESSION (table_3) [linking subjects to term and possibly instructor]
# - people: SUBJECT_ATTRIBUTE (table_7) [fallback for names if needed]
#
# Note: Column names may differ; we align/rename to the expected schema fields used in the reference.

# Load base tables
activities_raw = tables['table_10'].copy()  # SUBJECT_OFFERED
drupal_raw = tables['table_5'].copy()       # DRUPAL_COURSE_CATALOG (as locations proxy)
sessions_raw = tables['table_3'].copy()     # IAP_SUBJECT_SESSION (as assignments proxy)
terms_raw = tables['table_8'].copy()        # ACADEMIC_TERMS_ALL (terms)
supervisors_raw = tables['table_9'].copy()  # SIS_COURSE_DESCRIPTION (as supervisors proxy)
people_raw = tables['table_7'].copy()       # SUBJECT_ATTRIBUTE (as people proxy)

# Normalize/rename columns to emulate the expected schema
# Activities: need id, activity_type, title, location_id, term_start_date, supervisor_id
activities = activities_raw.copy()
# Heuristics for columns:
# - id: choose a subject identifier
for cand in ['SUBJECT_ID', 'subject_id', 'ID', 'id', 'Subject_ID']:
    if cand in activities.columns:
        activities = activities.rename(columns={cand: 'id'})
        break

# - activity_type: mark 'Independent' based on attributes or flags; if not present, create a placeholder.
if 'activity_type' not in activities.columns:
    # Use SUBJECT_ATTRIBUTE to infer 'Independent' if attribute like 'Independent Study' exists
    attrs = people_raw.copy()
    # Normalize columns for attributes
    subj_key = None
    for cand in ['SUBJECT_ID', 'subject_id', 'Subject_ID', 'id', 'ID']:
        if cand in attrs.columns:
            subj_key = cand
            break
    attr_name_col = None
    for cand in ['ATTRIBUTE', 'attribute', 'ATTR_NAME', 'NAME', 'name']:
        if cand in attrs.columns:
            attr_name_col = cand
            break
    if subj_key is not None and attr_name_col is not None and 'id' in activities.columns:
        ind_attr = attrs[[subj_key, attr_name_col]].copy()
        ind_attr['is_independent'] = ind_attr[attr_name_col].astype(str).str.contains('Independent', case=False, na=False)
        ind_subjects = ind_attr[ind_attr['is_independent']].drop_duplicates(subset=[subj_key])[[subj_key]]
        ind_subjects = ind_subjects.rename(columns={subj_key: 'id'})
        activities = activities.merge(ind_subjects.assign(activity_type='Independent'), on='id', how='left')
        activities['activity_type'] = activities['activity_type'].fillna('Other')
    else:
        activities['activity_type'] = 'Other'

# - title: prefer a title/name-like column
title_col = None
for cand in ['TITLE', 'Title', 'title', 'SUBJECT_TITLE', 'SUBJECT_NAME', 'NAME', 'name', 'COURSE_TITLE']:
    if cand in activities.columns:
        title_col = cand
        break
if title_col and title_col != 'title':
    activities = activities.rename(columns={title_col: 'title'})
elif 'title' not in activities.columns:
    activities['title'] = activities.get('id', pd.Series(range(len(activities)))).astype(str)

# - location_id: create a join key to "locations" using a catalog id if available
loc_key = None
for cand in ['CATALOG_ID', 'catalog_id', 'DRUPAL_ID', 'drupal_id', 'LOCATION_ID', 'location_id']:
    if cand in activities.columns:
        loc_key = cand
        break
if loc_key is None:
    # fallback: use id as key to join to drupal if possible
    loc_key = 'id'
activities = activities.rename(columns={loc_key: 'location_id'})

# - supervisor_id: attempt to use instructor/person id-like column
sup_key = None
for cand in ['INSTRUCTOR_ID', 'instructor_id', 'PERSON_ID', 'person_id', 'SUPERVISOR_ID', 'supervisor_id']:
    if cand in activities.columns:
        sup_key = cand
        break
if sup_key is None:
    # leave absent; will join via assignments
    pass
else:
    activities = activities.rename(columns={sup_key: 'supervisor_id'})

# - term_start_date: will be from terms or sessions; set if present
for cand in ['TERM_START_DATE', 'term_start_date', 'START_DATE', 'start_date']:
    if cand in activities.columns:
        activities = activities.rename(columns={cand: 'term_start_date'})
        break
if 'term_start_date' not in activities.columns:
    activities['term_start_date'] = pd.NaT

# Locations: need id, name
locations = drupal_raw.copy()
loc_id = None
for cand in ['ID', 'id', 'DRUPAL_ID', 'drupal_id', 'CATALOG_ID', 'catalog_id']:
    if cand in locations.columns:
        loc_id = cand
        break
if loc_id is None:
    # fabricate consistent key with activities.location_id if possible
    loc_id = 'ID' if 'ID' in locations.columns else 'id'
    if loc_id not in locations.columns and 'location_id' in activities.columns:
        locations[loc_id] = activities['location_id']
locations = locations.rename(columns={loc_id: 'id'})

loc_name = None
for cand in ['LOCATION_NAME', 'location_name', 'NAME', 'name', 'VENUE', 'venue', 'TITLE', 'title']:
    if cand in locations.columns:
        loc_name = cand
        break
if loc_name is None:
    locations['name'] = None
else:
    if loc_name != 'name':
        locations = locations.rename(columns={loc_name: 'name'})

locations = locations[['id', 'name']].drop_duplicates()

# Supervisors: need id, first_name, last_name, full_name
supervisors = supervisors_raw.copy()
sup_id = None
for cand in ['PERSON_ID', 'person_id', 'INSTRUCTOR_ID', 'instructor_id', 'ID', 'id']:
    if cand in supervisors.columns:
        sup_id = cand
        break
if sup_id is None:
    # fabricate placeholder id if necessary
    sup_id = 'ID' if 'ID' in supervisors.columns else 'id'
    if sup_id not in supervisors.columns:
        supervisors[sup_id] = range(len(supervisors))
supervisors = supervisors.rename(columns={sup_id: 'id'})

# Names
first_col = None
last_col = None
full_col = None
for cand in ['FULL_NAME', 'full_name', 'INSTRUCTOR_NAME', 'PERSON_NAME', 'NAME', 'name']:
    if cand in supervisors.columns:
        full_col = cand
        break
for cand in ['FIRST_NAME', 'first_name', 'GIVEN_NAME']:
    if cand in supervisors.columns:
        first_col = cand
        break
for cand in ['LAST_NAME', 'last_name', 'FAMILY_NAME', 'SURNAME']:
    if cand in supervisors.columns:
        last_col = cand
        break

if full_col and full_col != 'full_name':
    supervisors = supervisors.rename(columns={full_col: 'full_name'})
else:
    if 'full_name' not in supervisors.columns:
        supervisors['full_name'] = None
if first_col and first_col != 'first_name':
    supervisors = supervisors.rename(columns={first_col: 'first_name'})
elif 'first_name' not in supervisors.columns:
    supervisors['first_name'] = None
if last_col and last_col != 'last_name':
    supervisors = supervisors.rename(columns={last_col: 'last_name'})
elif 'last_name' not in supervisors.columns:
    supervisors['last_name'] = None

supervisors = supervisors[['id', 'first_name', 'last_name', 'full_name']].drop_duplicates()

# People fallback: id, name, role
people = people_raw.copy()
pid = None
for cand in ['PERSON_ID', 'person_id', 'ID', 'id', 'SUBJECT_ID', 'Subject_ID']:
    if cand in people.columns:
        pid = cand
        break
if pid is None:
    pid = 'id'
    if pid not in people.columns:
        people[pid] = activities['id']
pname = None
for cand in ['NAME', 'name', 'PERSON_NAME', 'VALUE', 'ATTRIBUTE']:
    if cand in people.columns:
        pname = cand
        break
prole = None
for cand in ['ROLE', 'role', 'TYPE', 'type']:
    if cand in people.columns:
        prole = cand
        break
people = people.rename(columns={pid: 'id'})
if pname and pname != 'name':
    people = people.rename(columns={pname: 'name'})
else:
    if 'name' not in people.columns:
        people['name'] = None
if prole and prole != 'role':
    people = people.rename(columns={prole: 'role'})
else:
    if 'role' not in people.columns:
        people['role'] = None
people = people[['id', 'name', 'role']].drop_duplicates()

# Assignments: activity_id, supervisor_id, term_id
assignments = sessions_raw.copy()
act_fk = None
for cand in ['SUBJECT_ID', 'subject_id', 'Subject_ID', 'ACTIVITY_ID', 'activity_id']:
    if cand in assignments.columns:
        act_fk = cand
        break
sup_fk = None
for cand in ['INSTRUCTOR_ID', 'instructor_id', 'PERSON_ID', 'person_id', 'SUPERVISOR_ID', 'supervisor_id']:
    if cand in assignments.columns:
        sup_fk = cand
        break
term_fk = None
for cand in ['TERM_ID', 'term_id', 'ACADEMIC_TERM_ID', 'academic_term_id']:
    if cand in assignments.columns:
        term_fk = cand
        break
rename_map = {}
if act_fk and act_fk != 'activity_id':
    rename_map[act_fk] = 'activity_id'
if sup_fk and sup_fk != 'supervisor_id':
    rename_map[sup_fk] = 'supervisor_id'
if term_fk and term_fk != 'term_id':
    rename_map[term_fk] = 'term_id'
assignments = assignments.rename(columns=rename_map)
if 'activity_id' not in assignments.columns and 'id' in activities.columns:
    assignments['activity_id'] = activities['id']
if 'supervisor_id' not in assignments.columns:
    assignments['supervisor_id'] = pd.NA
if 'term_id' not in assignments.columns:
    assignments['term_id'] = pd.NA
assignments = assignments[['activity_id', 'supervisor_id', 'term_id']].drop_duplicates()

# Terms: id, start_date
terms = terms_raw.copy()
term_id_col = None
for cand in ['TERM_ID', 'term_id', 'ACADEMIC_TERM_ID', 'academic_term_id', 'ID', 'id']:
    if cand in terms.columns:
        term_id_col = cand
        break
start_col = None
for cand in ['START_DATE', 'start_date', 'TERM_START_DATE', 'term_start_date', 'BEGIN_DATE']:
    if cand in terms.columns:
        start_col = cand
        break
if term_id_col and term_id_col != 'id':
    terms = terms.rename(columns={term_id_col: 'id'})
else:
    if 'id' not in terms.columns:
        terms['id'] = range(len(terms))
if start_col and start_col != 'start_date':
    terms = terms.rename(columns={start_col: 'start_date'})
elif 'start_date' not in terms.columns:
    terms['start_date'] = pd.NaT
# Ensure datetime
terms['start_date'] = pd.to_datetime(terms['start_date'], errors='coerce')
terms = terms[['id', 'start_date']].drop_duplicates()

# Build direct path result (activities joined to locations and supervisors directly)
a = activities.copy()
# Left join locations by location_id
direct = a.merge(locations.add_prefix('l_'), left_on='location_id', right_on='l_id', how='left')
# Join supervisors by supervisor_id
direct = direct.merge(supervisors.add_prefix('s_'), left_on='supervisor_id', right_on='s_id', how='left')
# People fallback using supervisor_id
people_sup = people.add_prefix('p_')
if 'supervisor_id' in direct.columns:
    direct = direct.merge(people_sup, left_on='supervisor_id', right_on='p_id', how='left')
else:
    # no supervisor_id, keep people nulls
    for c in ['p_id', 'p_name', 'p_role']:
        if c not in direct.columns:
            direct[c] = pd.NA

# Compose supervisor_name per SQL COALESCE logic
fn = direct['s_full_name']
concat_name = (direct['s_first_name'].fillna('') + ' ' + direct['s_last_name'].fillna('')).str.strip()
concat_name = concat_name.where(concat_name.str.len() > 0, None)
sup_name = fn.fillna(concat_name).fillna(direct['p_name'])
direct_result = pd.DataFrame({
    'title': direct['title'],
    'location_name': direct['l_name'],
    'term_start_date': pd.to_datetime(direct['term_start_date'], errors='coerce'),
    'supervisor_name': sup_name
})
# Filter activity_type = 'Independent'
direct_result = direct_result.loc[a['activity_type'] == 'Independent']

# Build indirect path via assignments -> terms and supervisors
a2 = activities[['id', 'title', 'location_id', 'activity_type']].copy()
indirect = a2.merge(assignments, left_on='id', right_on='activity_id', how='inner')
indirect = indirect.merge(terms.add_prefix('t_'), left_on='term_id', right_on='t_id', how='left')
indirect = indirect.merge(locations.add_prefix('l_'), left_on='location_id', right_on='l_id', how='left')
indirect = indirect.merge(supervisors.add_prefix('s_'), left_on='supervisor_id', right_on='s_id', how='left')
indirect = indirect.merge(people.add_prefix('p_'), left_on='supervisor_id', right_on='p_id', how='left')

fn2 = indirect['s_full_name']
concat_name2 = (indirect['s_first_name'].fillna('') + ' ' + indirect['s_last_name'].fillna('')).str.strip()
concat_name2 = concat_name2.where(concat_name2.str.len() > 0, None)
sup_name2 = fn2.fillna(concat_name2).fillna(indirect['p_name'])

indirect_result = pd.DataFrame({
    'title': indirect['title'],
    'location_name': indirect['l_name'],
    'term_start_date': indirect['t_start_date'],
    'supervisor_name': sup_name2
})
indirect_result = indirect_result.loc[indirect['activity_type'] == 'Independent']

# UNION results and DISTINCT
combined = pd.concat([direct_result, indirect_result], ignore_index=True)
# Drop duplicates on all columns
combined = combined.drop_duplicates(subset=['title', 'location_name', 'term_start_date', 'supervisor_name'])

# Sort by ascending term_start_date
combined = combined.sort_values(by=['term_start_date', 'title', 'location_name', 'supervisor_name'], kind='mergesort').reset_index(drop=True)

# Final answer mapping
result = {
    'independent_activities': combined[['title', 'location_name', 'term_start_date', 'supervisor_name']]
}