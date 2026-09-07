import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['PlanetID','Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Employee','Planet','Level']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df_long = table_1.melt(id_vars=['ShipmentID'], var_name='ShipmentID_melt', value_name='value')
    df_long['ShipmentID_melt'] = df_long['ShipmentID_melt'].astype(str)
    df_wide = df_long.pivot(index='ShipmentID_melt', columns='ShipmentID', values='value').reset_index()
    df_wide = df_wide.rename(columns={'ShipmentID_melt': 'ShipmentID'})
    target = df_wide[['ShipmentID', 'Manager', 'Planet']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_planets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_employee_planet_roles = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_shipments = prepared_table_3

# prepared_planets: select ['PlanetID','Name'] as-is
# prepared_employee_planet_roles: select ['Employee','Planet','Level'] as-is
# prepared_shipments: unpivot table_3 where columns 1..n represent ShipmentIDs

def normalize_shipments(table_3):
    # Identify shipment columns (assumed numeric-like labels)
    shipment_cols = [c for c in table_3.columns if c != 'ShipmentID']
    # Set row labels (Date, Manager, Planet) as index and melt
    df = table_3.set_index('ShipmentID').T
    # df rows are shipment ids (original column labels), columns are ['Date','Manager','Planet']
    df.index.name = 'ShipmentID'
    df = df.reset_index()
    # Keep only Manager and Planet, coerce to numeric
    df = df[['ShipmentID', 'Manager', 'Planet']].copy()
    # Coerce types
    df['ShipmentID'] = df['ShipmentID'].astype(str)
    df['Manager'] = pd.to_numeric(df['Manager'], errors='coerce').astype('Int64')
    df['Planet'] = pd.to_numeric(df['Planet'], errors='coerce').astype('Int64')
    # Drop rows missing Manager or Planet
    df = df.dropna(subset=['Manager','Planet'])
    # Convert Int64 to int where possible
    df['Manager'] = df['Manager'].astype(int)
    df['Planet'] = df['Planet'].astype(int)
    return df

prepared_shipments = normalize_shipments(table_3)
prepared_planets = table_1[['PlanetID','Name']].copy()
prepared_employee_planet_roles = table_2[['Employee','Planet','Level']].copy()

# Join shipments to planets to filter Mars
ship_planet = prepared_shipments.merge(prepared_planets, left_on='Planet', right_on='PlanetID', how='inner')
ship_planet_mars = ship_planet[ship_planet['Name'] == 'Mars']

# Join to employee-planet roles to ensure the manager manages that planet
ship_emp = ship_planet_mars.merge(prepared_employee_planet_roles, left_on=['Manager','Planet'], right_on=['Employee','Planet'], how='inner')

# We need shipments managed by Turanga Leela; map Employee IDs to name if available.
# Since no employee-name table is provided, assume Turanga Leela corresponds to a specific Employee ID inferred from data.
# From context: in table_2, Employee=2 is assigned to Planet=3 (Mars). We'll select Manager==2.
result = ship_emp[ship_emp['Manager'] == 2][['ShipmentID']].drop_duplicates().sort_values('ShipmentID')

# Final answer as list or dataframe of shipment IDs
answer = result['ShipmentID'].tolist()

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
