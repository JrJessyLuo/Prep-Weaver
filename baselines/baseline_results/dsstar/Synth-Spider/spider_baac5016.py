import pandas as pd

# Access pre-loaded tables
df_employees = tables['table_1']
df_planets = tables['table_2']
df_emp_planet_level = tables['table_3']

# Parse the matrix-like employee -> (Planet, Level) mapping into a tidy DataFrame
row0 = df_emp_planet_level.iloc[0].tolist()  # ['Planet', ...]
row1 = df_emp_planet_level.iloc[1].tolist()  # ['Level', ...]
planet_values = row0[1:]
level_values = row1[1:]
n = min(len(planet_values), len(level_values))
employee_ids = list(range(1, n + 1))
tidy_map = pd.DataFrame({
    'Employee': employee_ids,
    'PlanetID': planet_values[:n],
    'Level': level_values[:n]
})

# Find PlanetID for 'Omega III'
omega_row = df_planets[df_planets['Name'] == 'Omega III']
omega_planet_id = int(omega_row['PlanetID'].iloc[0])

# Employees mapped to Omega III, join to get names
employees_on_omega = tidy_map[tidy_map['PlanetID'] == omega_planet_id]
answer_df = employees_on_omega.merge(
    df_employees[['ygh', 'Name']],
    left_on='Employee',
    right_on='ygh',
    how='left'
)[['Name']].dropna().drop_duplicates().reset_index(drop=True)

# Prepare final result dict
result = {
    'employees_with_clearance_in_omega_iii': answer_df
}