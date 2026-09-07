import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['First_Name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['First_Name'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Driver_ID', 'First_Name', 'Last_Name'])
    # SelectCol
    _cols = [c for c in ['Driver_ID', 'First_Name', 'Last_Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Driver_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Driver_ID'], keep='last').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="table_1_unique_driver_cols", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    #     # ensure unique column names (keeps driver id as prefix)
    #     new_cols = []
    #     counts = {}
    #     for c in df.columns:
    #         key = str(c)
    #         counts[key] = counts.get(key, 0) + 1
    #         new_cols.append(key if counts[key] == 1 else f"{key}_{counts[key]}")
    #     df.columns = new_cols
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()
        # ensure unique column names (keeps driver id as prefix)
        new_cols = []
        counts = {}
        for c in df.columns:
            key = str(c)
            counts[key] = counts.get(key, 0) + 1
            new_cols.append(key if counts[key] == 1 else f"{key}_{counts[key]}")
        df.columns = new_cols
        return df
    table_1_unique_driver_cols = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1_unique_driver_cols'], target_table="driver_vehicle_long", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1_unique_driver_cols: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1_unique_driver_cols.copy()
    # 
    #     # all columns except the redundant first one are driver columns
    #     driver_cols = [c for c in df.columns if str(c) != "Driver_ID"]
    # 
    #     long_df = df.melt(
    #         value_vars=driver_cols,
    #         var_name="Driver_ID",
    #         value_name="Vehicle_ID"
    #     )
    # 
    #     # normalize Driver_ID by removing suffixes like _2, _3...
    #     long_df["Driver_ID"] = long_df["Driver_ID"].astype(str).str.split("_").str[0]
    # 
    #     # drop blanks/nulls in Vehicle_ID
    #     long_df["Vehicle_ID"] = pd.to_numeric(long_df["Vehicle_ID"], errors="coerce")
    # 
    #     long_df = long_df.dropna(subset=["Vehicle_ID"])
    # 
    #     # cast Driver_ID numeric too (optional but usually desired)
    #     long_df["Driver_ID"] = pd.to_numeric(long_df["Driver_ID"], errors="coerce")
    #     long_df = long_df.dropna(subset=["Driver_ID"])
    # 
    #     # final column order
    #     return long_df[["Driver_ID", "Vehicle_ID"]]
    # """)
    # CodeGeneration

    def process_tables(table_1_unique_driver_cols: pd.DataFrame) -> pd.DataFrame:
        df = table_1_unique_driver_cols.copy()

        # all columns except the redundant first one are driver columns
        driver_cols = [c for c in df.columns if str(c) != "Driver_ID"]

        long_df = df.melt(
            value_vars=driver_cols,
            var_name="Driver_ID",
            value_name="Vehicle_ID"
        )

        # normalize Driver_ID by removing suffixes like _2, _3...
        long_df["Driver_ID"] = long_df["Driver_ID"].astype(str).str.split("_").str[0]

        # drop blanks/nulls in Vehicle_ID
        long_df["Vehicle_ID"] = pd.to_numeric(long_df["Vehicle_ID"], errors="coerce")

        long_df = long_df.dropna(subset=["Vehicle_ID"])

        # cast Driver_ID numeric too (optional but usually desired)
        long_df["Driver_ID"] = pd.to_numeric(long_df["Driver_ID"], errors="coerce")
        long_df = long_df.dropna(subset=["Driver_ID"])

        # final column order
        return long_df[["Driver_ID", "Vehicle_ID"]]
    driver_vehicle_long = process_tables(table_1_unique_driver_cols)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="driver_vehicle_long", column="Driver_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = driver_vehicle_long['Driver_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = driver_vehicle_long['Driver_ID']
    if _dtype == "datetime64":
        driver_vehicle_long['Driver_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        driver_vehicle_long['Driver_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        driver_vehicle_long['Driver_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        driver_vehicle_long['Driver_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="driver_vehicle_long", column="Vehicle_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = driver_vehicle_long['Vehicle_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = driver_vehicle_long['Vehicle_ID']
    if _dtype == "datetime64":
        driver_vehicle_long['Vehicle_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        driver_vehicle_long['Vehicle_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        driver_vehicle_long['Vehicle_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        driver_vehicle_long['Vehicle_ID'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['driver_vehicle_long'])
    # Terminate
    result = {'driver_vehicle_long': driver_vehicle_long}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_driver_vehicle_pairs = prepared_table_2

# prepared_drivers: columns [Driver_ID (int), First_Name, Last_Name]
# prepared_driver_vehicle_pairs: columns [Driver_ID (int), Vehicle_ID]

# Left-join drivers to driven pairs and find drivers with no matches
merged = prepared_drivers.merge(prepared_driver_vehicle_pairs, on='Driver_ID', how='left')
no_cars = merged[merged['Vehicle_ID'].isna()]
# Count unique drivers with no cars
answer = no_cars['Driver_ID'].nunique()

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
