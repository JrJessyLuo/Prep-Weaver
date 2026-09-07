import pandas as pd

# Access input tables from the provided `tables` dict
df_students = tables['table_1']
df_cities = tables['table_2']

# Left join students with cities on city_code = cid to bring in city_name
df_merged = df_students.merge(
    df_cities[['cid', 'city_name']],
    how='left',
    left_on='city_code',
    right_on='cid'
).drop(columns=['cid'])

# Group by city_name if available; otherwise fall back to city_code
group_key = df_merged['city_name'].fillna(df_merged['city_code'])

# Compute the count of StuID per group
city_counts = (
    df_merged
    .assign(group_city=group_key)
    .groupby('group_city', dropna=False)['StuID']
    .count()
    .reset_index(name='student_count')
    .rename(columns={'group_city': 'city_group'})
    .sort_values(['student_count', 'city_group'], ascending=[False, True])
    .reset_index(drop=True)
)

# Package the final result
result = {
    "students_per_city": city_counts
}