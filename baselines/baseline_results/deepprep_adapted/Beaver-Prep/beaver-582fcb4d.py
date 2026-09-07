import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_TYPE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_TYPE"] = table_1["BUILDING_TYPE"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="PARENT_BUILDING_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # normalize common null-like values
    #     if s.lower() in {"nan", "none", "(null)", ""}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # normalize common null-like values
        if s.lower() in {"nan", "none", "(null)", ""}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["PARENT_BUILDING_NUMBER"] = table_1["PARENT_BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="OWNERSHIP_TYPE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["OWNERSHIP_TYPE"] = table_1["OWNERSHIP_TYPE"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SITE", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SITE"] = table_1["SITE"].apply(_std_apply)

    # ---------------- Step 8 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DATE_OCCUPIED", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['DATE_OCCUPIED'] = table_1['DATE_OCCUPIED'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_OCCUPIED'] = table_1['DATE_OCCUPIED'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILDING_NAME', 'BUILDING_TYPE', 'DATE_OCCUPIED', 'OWNERSHIP_TYPE', 'SITE', 'PARENT_BUILDING_NUMBER'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_NAME_LONG', 'BUILDING_NAME', 'BUILDING_TYPE', 'DATE_OCCUPIED', 'OWNERSHIP_TYPE', 'SITE', 'PARENT_BUILDING_NUMBER'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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
    # ErrorDetection(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return s != '' and s.lower() != 'nan'
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        s = str(val).strip()
        return s != '' and s.lower() != 'nan'
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['BUILDING_NUMBER'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_NUMBER'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_NUMBER'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_STREET_ADDRESS", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # trim and collapse multiple spaces
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # trim and collapse multiple spaces
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_STREET_ADDRESS"] = table_1["BUILDING_STREET_ADDRESS"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_NUMBER', 'BUILDING_STREET_ADDRESS', 'BUILDING_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_NUMBER', 'BUILDING_STREET_ADDRESS', 'BUILDING_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_buildings_core = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_buildings_address = prepared_table_2

core = prepared_buildings_core.copy()
addr = prepared_buildings_address.copy()

# Merge on BUILDING_NUMBER
merged = core.merge(addr, on='BUILDING_NUMBER', how='left')

# Exclude subdivisions: rows with null PARENT_BUILDING_NUMBER are top-level buildings
not_subdiv = merged[merged['PARENT_BUILDING_NUMBER'].isna()].copy()

# Choose full name preference: use BUILDING_NAME_LONG if present else BUILDING_NAME from core else name from address
def choose_full_name(row):
    for col in ['BUILDING_NAME_LONG', 'BUILDING_NAME_x', 'BUILDING_NAME_y']:
        if col in row and pd.notna(row[col]) and str(row[col]).strip() != '':
            return row[col]
    return None

not_subdiv['FULL_NAME'] = not_subdiv.apply(choose_full_name, axis=1)

# Select and rename columns per request
result_cols = [
    'BUILDING_NUMBER',                    # building number
    'FULL_NAME',                          # full name
    'BUILDING_STREET_ADDRESS',            # street address
    'BUILDING_TYPE',                      # building type
    'DATE_OCCUPIED',                      # occupancy date
    'OWNERSHIP_TYPE',                     # ownership type
    'SITE'                                # site location
]
result = not_subdiv[result_cols].copy()

# Build the three summary rows for owned, leased, all (among not subdivisions and SITE == 'MIT' per question wording)
# If "at MIT" should filter by SITE == 'MIT'. Apply that to both detail rows and counts.
result_at_mit = result[result['SITE'] == 'MIT'].copy()

owned_count = (not_subdiv['SITE'].eq('MIT') & not_subdiv['OWNERSHIP_TYPE'].str.upper().eq('OWNED')).sum()
leased_count = (not_subdiv['SITE'].eq('MIT') & not_subdiv['OWNERSHIP_TYPE'].str.upper().eq('LEASED')).sum()
all_count = result_at_mit.shape[0]

summary_rows = pd.DataFrame([
    {
        'BUILDING_NUMBER': None,
        'FULL_NAME': f"{owned_count} Buildings",
        'BUILDING_STREET_ADDRESS': None,
        'BUILDING_TYPE': None,
        'DATE_OCCUPIED': None,
        'OWNERSHIP_TYPE': None,
        'SITE': None
    },
    {
        'BUILDING_NUMBER': None,
        'FULL_NAME': f"{leased_count} Buildings",
        'BUILDING_STREET_ADDRESS': None,
        'BUILDING_TYPE': None,
        'DATE_OCCUPIED': None,
        'OWNERSHIP_TYPE': None,
        'SITE': None
    },
    {
        'BUILDING_NUMBER': None,
        'FULL_NAME': f"{all_count} Buildings",
        'BUILDING_STREET_ADDRESS': None,
        'BUILDING_TYPE': None,
        'DATE_OCCUPIED': None,
        'OWNERSHIP_TYPE': None,
        'SITE': None
    }
], columns=result_cols)

# Concatenate detailed MIT rows first, then the three summary rows
final_answer = pd.concat([result_at_mit, summary_rows], ignore_index=True)

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
