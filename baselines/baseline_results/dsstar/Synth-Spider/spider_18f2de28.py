import pandas as pd

# Access preloaded tables
df_students = tables['table_1']
df_cities = tables['table_2']
df_dist = tables['table_3']

# Reproduce the same logic as the reference code, sourcing from `tables`
unique_attrs = df_students['Attribute'].unique()

# Identify which student attribute represents city_code
city_codes = set(df_cities['city_code'].astype(str).unique())
attr_city_like_counts = []
for attr in unique_attrs:
    vals = df_students.loc[df_students['Attribute'] == attr, 'Value'].astype(str)
    match_count = vals.isin(city_codes).sum()
    total = len(vals)
    if match_count > 0:
        attr_city_like_counts.append((attr, match_count, total))
attr_city_like_counts.sort(key=lambda x: (-x[1], x[0]))

if 'city_code' in set(unique_attrs):
    student_city_attr = 'city_code'
else:
    student_city_attr = attr_city_like_counts[0][0] if attr_city_like_counts else None

result_df = pd.DataFrame(columns=['StuID', 'FName', 'Major'])
if student_city_attr is not None:
    # Filter to students living in Baltimore => city_code == 'BAL'
    stu_in_bal_ids = set(
        df_students[(df_students['Attribute'] == student_city_attr) & (df_students['Value'].astype(str) == 'BAL')]['StuID']
    )

    df_bal_students = df_students[df_students['StuID'].isin(stu_in_bal_ids)].copy()

    # Normalize attribute names for first name and major following the reference logic
    fname_attrs = [a for a in unique_attrs if a in {'FName', 'FirstName', 'First_Name', 'GivenName'}]
    major_attrs = [a for a in unique_attrs if a in {'Major', 'MajorName', 'Major_Field'}]

    if not fname_attrs:
        fname_attrs = ['FName'] if 'FName' in set(unique_attrs) else (['FirstName'] if 'FirstName' in set(unique_attrs) else [])
    if not major_attrs:
        major_attrs = ['Major'] if 'Major' in set(unique_attrs) else []

    keep_attrs = set([student_city_attr]) | set(fname_attrs) | set(major_attrs)
    df_bal_students_reduced = df_bal_students[df_bal_students['Attribute'].isin(keep_attrs)].copy()

    # Pivot to wide format
    df_bal_students_reduced['rank'] = df_bal_students_reduced.groupby(['StuID', 'Attribute']).cumcount()
    df_wide = df_bal_students_reduced.pivot_table(
        index='StuID',
        columns='Attribute',
        values='Value',
        aggfunc='first'
    ).reset_index()

    def coalesce_cols(row, cols):
        for c in cols:
            if c in row and pd.notna(row[c]):
                return row[c]
        return pd.NA

    df_wide['FName_out'] = df_wide.apply(lambda r: coalesce_cols(r, fname_attrs), axis=1) if fname_attrs else pd.NA
    df_wide['Major_out'] = df_wide.apply(lambda r: coalesce_cols(r, major_attrs), axis=1) if major_attrs else pd.NA

    result_df = df_wide[['StuID', 'FName_out', 'Major_out']].rename(columns={'FName_out': 'FName', 'Major_out': 'Major'})

# Prepare final answer as required
result = {
    "students_in_baltimore_firstname_major": result_df[['FName', 'Major']]
}