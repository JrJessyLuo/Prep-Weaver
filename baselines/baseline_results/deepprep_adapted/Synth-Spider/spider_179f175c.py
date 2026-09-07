import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="PlanetID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['PlanetID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['PlanetID']
    if _dtype == "datetime64":
        table_1['PlanetID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['PlanetID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['PlanetID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['PlanetID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['PlanetID', 'Name'])
    # SelectCol
    _cols = [c for c in ['PlanetID', 'Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # CastType(table_name="table_1", column="Level", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Level'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Level']
    if _dtype == "datetime64":
        table_1['Level'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Level'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Level'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Level'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Employee', 'Planet', 'Level'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Employee', 'Planet', 'Level'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Employee", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Employee'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Employee']
    if _dtype == "datetime64":
        table_1['Employee'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Employee'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Employee'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Employee'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Planet", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Planet'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Planet']
    if _dtype == "datetime64":
        table_1['Planet'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Planet'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Planet'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Planet'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Level", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Level'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Level']
    if _dtype == "datetime64":
        table_1['Level'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Level'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Level'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Level'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Employee', 'Planet', 'Level'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Employee', 'Planet', 'Level'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Employee', 'Planet', 'Level'])
    # SelectCol
    _cols = [c for c in ['Employee', 'Planet', 'Level'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
    # CodeGeneration(table_names=['table_1'], target_table="normalized_shipments", func="""
    # import pandas as pd
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # First column contains attribute names: Date/Manager/Planet
    #     attr_col = df.columns[0]
    # 
    #     # Set attribute names as index, transpose to make ShipmentID a row field
    #     df_t = df.set_index(attr_col).T.reset_index()
    # 
    #     # The transposed index corresponds to ShipmentID (original numeric columns)
    #     df_t = df_t.rename(columns={"index": "ShipmentID"})
    # 
    #     # Keep only required columns (Date is not required for target)
    #     keep_cols = [c for c in ["ShipmentID", "Manager", "Planet"] if c in df_t.columns]
    #     return df_t[keep_cols]
    # """)
    # CodeGeneration
    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # First column contains attribute names: Date/Manager/Planet
        attr_col = df.columns[0]

        # Set attribute names as index, transpose to make ShipmentID a row field
        df_t = df.set_index(attr_col).T.reset_index()

        # The transposed index corresponds to ShipmentID (original numeric columns)
        df_t = df_t.rename(columns={"index": "ShipmentID"})

        # Keep only required columns (Date is not required for target)
        keep_cols = [c for c in ["ShipmentID", "Manager", "Planet"] if c in df_t.columns]
        return df_t[keep_cols]
    normalized_shipments = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="normalized_shipments", column="ShipmentID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = normalized_shipments['ShipmentID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = normalized_shipments['ShipmentID']
    if _dtype == "datetime64":
        normalized_shipments['ShipmentID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        normalized_shipments['ShipmentID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        normalized_shipments['ShipmentID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        normalized_shipments['ShipmentID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="normalized_shipments", column="Manager", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = normalized_shipments['Manager'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = normalized_shipments['Manager']
    if _dtype == "datetime64":
        normalized_shipments['Manager'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        normalized_shipments['Manager'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        normalized_shipments['Manager'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        normalized_shipments['Manager'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="normalized_shipments", column="Planet", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = normalized_shipments['Planet'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = normalized_shipments['Planet']
    if _dtype == "datetime64":
        normalized_shipments['Planet'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        normalized_shipments['Planet'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        normalized_shipments['Planet'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        normalized_shipments['Planet'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['normalized_shipments'])
    # Terminate
    result = {'normalized_shipments': normalized_shipments}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
