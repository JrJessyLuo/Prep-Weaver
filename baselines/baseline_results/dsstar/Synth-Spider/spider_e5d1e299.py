import pandas as pd

# Use the provided tables dict
conf_df = tables['table_1']  # conferences
inst_df = tables['table_2']  # institutions
staff_df = tables['table_3']  # staff
part_df = tables['table_4']  # participation (huiyi_id–yuangong_id–role)

# Identify potential linkage from staff to institutions
inst_like_cols = [c for c in staff_df.columns if any(k in c.lower() for k in ["institution", "univ", "college", "school", "dept", "department"])]
fk_like_cols = [c for c in staff_df.columns if c.lower() in ("institution_id", "inst_id", "university_id", "college_id")]

# Extract 2004 conferences
conf_2004 = conf_df[conf_df['Conference_Info'].astype(str).str.contains("2004", na=False)].copy()
if 'Conference_ID' in conf_2004.columns:
    conf_2004 = conf_2004.rename(columns={'Conference_ID': 'huiyi_id'})

# Filter participation for 2004 conferences
merge_cols = ['huiyi_id'] + [c for c in ['Location', 'Conference_Info'] if c in conf_2004.columns]
part_2004 = part_df.merge(conf_2004[merge_cols], on='huiyi_id', how='inner')

# Join to staff by yuangong_id -> staff_ID (or close variant)
if 'staff_ID' in staff_df.columns:
    staff_id_col = 'staff_ID'
else:
    cand = [c for c in staff_df.columns if c.lower() in ('staff_id','id','employee_id','emp_id')]
    staff_id_col = cand[0] if cand else None

if not staff_id_col:
    participated_insts = pd.DataFrame(columns=['Institution_ID'])
else:
    part_staff = part_2004.merge(staff_df, left_on='yuangong_id', right_on=staff_id_col, how='left')

    # Attempt to map staff to institutions
    inst_joined = part_staff.copy()

    # Strategy A: direct FK in staff_df
    if 'Institution_ID' in staff_df.columns:
        inst_joined = part_staff.merge(inst_df, on='Institution_ID', how='left', suffixes=('', '_inst'))
    elif any(c.lower() == 'institution_id' for c in staff_df.columns):
        ik = [c for c in staff_df.columns if c.lower() == 'institution_id'][0]
        inst_joined = part_staff.merge(inst_df, left_on=ik, right_on='Institution_ID', how='left', suffixes=('', '_inst'))
    # Strategy B: exact name match if staff_df has institution-like name column
    elif inst_like_cols:
        name_pref = [c for c in inst_like_cols if any(k in c.lower() for k in ['name','institution','univ','college']) and 'id' not in c.lower()]
        if name_pref:
            name_col = name_pref[0]
            if 'Institution_Name' in inst_df.columns:
                right_cols = ['Institution_Name']
                for c in ['Institution_ID','Location','Founded']:
                    if c in inst_df.columns:
                        right_cols.append(c)
                inst_joined = part_staff.merge(
                    inst_df[right_cols],
                    left_on=name_col,
                    right_on='Institution_Name',
                    how='left',
                    suffixes=('', '_inst')
                )

    # Derive the set of participating Institution_IDs in 2004
    if 'Institution_ID' in inst_joined.columns:
        participated_insts = inst_joined[['Institution_ID']].dropna().drop_duplicates()
        if not participated_insts.empty and 'Institution_ID' in inst_df.columns:
            participated_insts['Institution_ID'] = participated_insts['Institution_ID'].astype(inst_df['Institution_ID'].dtype)
    else:
        participated_insts = pd.DataFrame(columns=['Institution_ID'])

# Left-anti join Institutions with participated_insts to find universities with no participation in 2004
inst_only_keys = inst_df[['Institution_ID']].copy()
if participated_insts.empty:
    no_part_ids = inst_only_keys.copy()
else:
    no_part_ids = inst_only_keys.merge(participated_insts.assign(_flag=1), on='Institution_ID', how='left')
    no_part_ids = no_part_ids[no_part_ids['_flag'].isna()][['Institution_ID']]

no_part_insts = inst_df.merge(no_part_ids, on='Institution_ID', how='inner')

# Select output columns: Institution_Name and Location
output_cols = [c for c in ['Institution_ID', 'Institution_Name', 'Location', 'Founded'] if c in no_part_insts.columns]
final_df = no_part_insts[output_cols].sort_values(by=['Institution_Name']).reset_index(drop=True)

result = {"universities_without_2004_participation": final_df}