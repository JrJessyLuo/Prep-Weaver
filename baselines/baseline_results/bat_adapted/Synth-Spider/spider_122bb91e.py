import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['PlanetID','Name_Part1','Name_Part2','Name_Part3']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Shipment','PackageNumber','Sender','Recipient']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['EmployeeID','Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['Employee','Planet','Level']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_planets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_shipments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_employees = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
prepared_employee_planets = prepared_table_4

# Assume dataframes: prepared_planets, prepared_shipments, prepared_employees, prepared_employee_planets

# Identify the planet ID for 'Omicron Persei 8'
omicron_mask = (
    prepared_planets['Name_Part1'].str.strip().str.lower() == 'omicron'
) & (
    prepared_planets['Name_Part2'].str.strip().str.lower() == 'persei'
) & (
    prepared_planets['Name_Part3'].astype(str).str.strip().str.lower() == '8'
)
omicron_ids = prepared_planets.loc[omicron_mask, 'PlanetID']

# Bridge: employees associated with Omicron Persei 8
emp_on_omicron = prepared_employee_planets.merge(
    prepared_planets[['PlanetID']], left_on='Planet', right_on='PlanetID', how='inner'
)
emp_on_omicron = emp_on_omicron[emp_on_omicron['Planet'].isin(omicron_ids)]
employees_on_omicron = emp_on_omicron['Employee'].unique()

# Shipments to/from Omicron via employees (either sender or recipient associated with the planet)
shipments_omicron = prepared_shipments[(
    prepared_shipments['Sender'].isin(employees_on_omicron)
) | (
    prepared_shipments['Recipient'].isin(employees_on_omicron)
)]

# Identify EmployeeID for Zapp Brannigan
zapp_ids = prepared_employees.loc[
    prepared_employees['Name'].str.strip().str.lower() == 'zapp brannigan', 'EmployeeID'
]

# Shipments sent by Zapp Brannigan (as Sender)
shipments_zapp = prepared_shipments[prepared_shipments['Sender'].isin(zapp_ids)]

# Union of package rows matching either condition
target_shipments = pd.concat([shipments_omicron, shipments_zapp], ignore_index=True).drop_duplicates(subset=['Shipment','PackageNumber'])

# Count packages (each row is a package)
answer = len(target_shipments)

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
