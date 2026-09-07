import pandas as pd

# Access pre-loaded tables
df_students = tables['table_1']
df_cities = tables['table_2']

# Inner merge on city_code to bring state (and other city info) into students table
df_merged = df_students.merge(df_cities[['city_code', 'state']], on='city_code', how='inner')

# Filter the merged DataFrame to rows where state == "MD"
df_filtered_md = df_merged[df_merged['state'] == "MD"]

# Select only the required columns: first name and last name
final_df = df_filtered_md[['first_name', 'last_name']]

# Assign to result as required
result = {"students_in_MD_names": final_df}