import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Name_Part1", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Name_Part1"] = table_1["Name_Part1"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Name_Part2", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Name_Part2"] = table_1["Name_Part2"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Name_Part3", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     return str(s).strip().strip('"').strip("'")
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        return str(s).strip().strip('"').strip("'")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Name_Part3"] = table_1["Name_Part3"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['PlanetID', 'Name_Part1', 'Name_Part2', 'Name_Part3'])
    # SelectCol
    _cols = [c for c in ['PlanetID', 'Name_Part1', 'Name_Part2', 'Name_Part3'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Shipment', 'PackageNumber', 'Sender', 'Recipient'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Shipment', 'PackageNumber', 'Sender', 'Recipient'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Shipment', 'PackageNumber', 'Sender', 'Recipient'])
    # SelectCol
    _cols = [c for c in ['Shipment', 'PackageNumber', 'Sender', 'Recipient'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Shipment", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Shipment'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Shipment']
    if _dtype == "datetime64":
        table_1['Shipment'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Shipment'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Shipment'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Shipment'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="PackageNumber", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['PackageNumber'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['PackageNumber']
    if _dtype == "datetime64":
        table_1['PackageNumber'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['PackageNumber'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['PackageNumber'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['PackageNumber'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Sender", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Sender'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Sender']
    if _dtype == "datetime64":
        table_1['Sender'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Sender'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Sender'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Sender'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Recipient", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Recipient'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Recipient']
    if _dtype == "datetime64":
        table_1['Recipient'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Recipient'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Recipient'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Recipient'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['Name'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['Name'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['EmployeeID', 'Name'])
    # SelectCol
    _cols = [c for c in ['EmployeeID', 'Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['EmployeeID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['EmployeeID'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
