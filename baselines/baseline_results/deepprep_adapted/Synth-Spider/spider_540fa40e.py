import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['siji_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['siji_id'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="siji_id", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove doubled quotes like ""1"" -> 1, and normal quotes
    #     return re.sub(r'^"+|"+$', '', str(s)).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove doubled quotes like ""1"" -> 1, and normal quotes
        return re.sub(r'^"+|"+$', '', str(s)).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["siji_id"] = table_1["siji_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="driver_attr_long", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame):
    #     df = table_1.copy()
    # 
    #     # Ensure list objects; if they are strings, safely parse basic list-like strings
    #     def to_list(x):
    #         if isinstance(x, list):
    #             return x
    #         if pd.isna(x):
    #             return []
    #         s = str(x).strip()
    #         # very lightweight parser for strings that look like Python lists
    #         if s.startswith('[') and s.endswith(']'):
    #             try:
    #                 import ast
    #                 return ast.literal_eval(s)
    #             except Exception:
    #                 return []
    #         return []
    # 
    #     df['shuxing_list'] = df['shuxing'].apply(to_list)
    #     df['zhi_list'] = df['shuxing_zhi'].apply(to_list)
    # 
    #     # Build long rows
    #     rows = []
    #     for _, r in df.iterrows():
    #         keys = r['shuxing_list']
    #         vals = r['zhi_list']
    #         n = min(len(keys), len(vals))
    #         for i in range(n):
    #             rows.append({
    #                 "siji_id": r["siji_id"],
    #                 "attribute": keys[i],
    #                 "value": vals[i]
    #             })
    # 
    #     out = pd.DataFrame(rows)
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame):
        df = table_1.copy()

        # Ensure list objects; if they are strings, safely parse basic list-like strings
        def to_list(x):
            if isinstance(x, list):
                return x
            if pd.isna(x):
                return []
            s = str(x).strip()
            # very lightweight parser for strings that look like Python lists
            if s.startswith('[') and s.endswith(']'):
                try:
                    import ast
                    return ast.literal_eval(s)
                except Exception:
                    return []
            return []

        df['shuxing_list'] = df['shuxing'].apply(to_list)
        df['zhi_list'] = df['shuxing_zhi'].apply(to_list)

        # Build long rows
        rows = []
        for _, r in df.iterrows():
            keys = r['shuxing_list']
            vals = r['zhi_list']
            n = min(len(keys), len(vals))
            for i in range(n):
                rows.append({
                    "siji_id": r["siji_id"],
                    "attribute": keys[i],
                    "value": vals[i]
                })

        out = pd.DataFrame(rows)
        return out
    driver_attr_long = process_tables(table_1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Pivot(table_name="driver_attr_long", index="siji_id", columns="attribute", values="value", aggfunc="first")
    # Pivot
    driver_attr_long = driver_attr_long.pivot_table(index='siji_id', columns='attribute', values='value', aggfunc='first').reset_index()

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="driver_attr_long", column="Age", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = driver_attr_long['Age'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = driver_attr_long['Age']
    if _dtype == "datetime64":
        driver_attr_long['Age'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        driver_attr_long['Age'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        driver_attr_long['Age'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        driver_attr_long['Age'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="driver_attr_long", columns=['siji_id', 'Age'])
    # SelectCol
    _cols = [c for c in ['siji_id', 'Age'] if c in driver_attr_long.columns]
    driver_attr_long = driver_attr_long[_cols]

    # ---------------- Step 7 ----------------
    # Original operator:
    # Terminate(result=['driver_attr_long'])
    # Terminate
    result = {'driver_attr_long': driver_attr_long}
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
    # CastType(table_name="table_1", column="Road", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Road'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Road']
    if _dtype == "datetime64":
        table_1['Road'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Road'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Road'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Road'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Driver_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Driver_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Driver_ID']
    if _dtype == "datetime64":
        table_1['Driver_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Driver_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Driver_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Driver_ID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Driver_ID', 'Road'])
    # SelectCol
    _cols = [c for c in ['Driver_ID', 'Road'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Driver_ID', 'Road'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Driver_ID', 'Road'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
race_participation = prepared_table_2

# Assume prepared tables already created as per target schemas:
# drivers columns: ['siji_id','Age']
# race_participation columns: ['Driver_ID','Road']

# Normalize key types to string for safe join
race_participation['Driver_ID'] = race_participation['Driver_ID'].astype(str)
drivers['siji_id'] = drivers['siji_id'].astype(str)

# Join participations to driver ages
joined = race_participation.merge(drivers, left_on='Driver_ID', right_on='siji_id', how='left')

# Compute race counts per driver
counts = joined.groupby('Driver_ID', as_index=False).agg(race_count=('Road','nunique'))

# Identify driver(s) with the maximum number of races
max_count = counts['race_count'].max()
top_drivers = counts[counts['race_count'] == max_count]

# Attach ages
result = top_drivers.merge(drivers, left_on='Driver_ID', right_on='siji_id', how='left')

# Final answer: show the age(s)
answer = result[['Age']].drop_duplicates()
answer

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
