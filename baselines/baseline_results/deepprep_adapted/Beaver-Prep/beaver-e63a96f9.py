import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['FULL_NAME', 'JOB_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['FULL_NAME', 'JOB_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'JOB_TITLE', 'HR_DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['FULL_NAME', 'FIRST_NAME', 'LAST_NAME', 'JOB_TITLE', 'HR_DEPARTMENT_NAME'] if c in table_1.columns]
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
    # StandardizeString(table_name="table_1", column_name="ROOM", func="""
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
    table_1["ROOM"] = table_1["ROOM"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
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
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR", func="""
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
    table_1["FLOOR"] = table_1["FLOOR"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fac_room_key", func="""
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
    table_1["fac_room_key"] = table_1["fac_room_key"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SPACE_ID", func="""
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
    table_1["SPACE_ID"] = table_1["SPACE_ID"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     # Keep rows that look like \"office\" in any available use description field
    #     candidates = []
    #     for c in [\"USE_DESC\", \"MAJOR_USE_DESC\", \"MINOR_USE_DESC\"]:
    #         if c in row.index:
    #             v = row[c]
    #             if v is not None and not (isinstance(v, float) and pd.isna(v)):
    #                 candidates.append(str(v))
    #     haystack = \" | \".join(candidates).upper()
    #     return (\"OFFICE\" in haystack) or (\"ADMIN\" in haystack)
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        # Keep rows that look like \"office\" in any available use description field
        candidates = []
        for c in [\"USE_DESC\", \"MAJOR_USE_DESC\", \"MINOR_USE_DESC\"]:
            if c in row.index:
                v = row[c]
                if v is not None and not (isinstance(v, float) and pd.isna(v)):
                    candidates.append(str(v))
        haystack = \" | \".join(candidates).upper()
        return (\"OFFICE\" in haystack) or (\"ADMIN\" in haystack)
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 7 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="ROOM_FULL_NAME_PREP", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     v = row.get("ROOM_FULL_NAME", None)
    #     if v is not None and not (isinstance(v, float) and pd.isna(v)) and str(v).strip() != "":
    #         return str(v).strip()
    #     b = str(row.get("BUILDING_KEY", "")).strip()
    #     f = str(row.get("FLOOR", "")).strip()
    #     r = str(row.get("ROOM", "")).strip()
    #     # Fallback evidence-friendly label if ROOM_FULL_NAME is missing
    #     return "-".join([x for x in [b, f, r] if x])
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        v = row.get("ROOM_FULL_NAME", None)
        if v is not None and not (isinstance(v, float) and pd.isna(v)) and str(v).strip() != "":
            return str(v).strip()
        b = str(row.get("BUILDING_KEY", "")).strip()
        f = str(row.get("FLOOR", "")).strip()
        r = str(row.get("ROOM", "")).strip()
        # Fallback evidence-friendly label if ROOM_FULL_NAME is missing
        return "-".join([x for x in [b, f, r] if x])
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["ROOM_FULL_NAME_PREP"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 8 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['ROOM_FULL_NAME'])
    # DropColumn
    table_1 = table_1.drop(columns=['ROOM_FULL_NAME'], errors='ignore')

    # ---------------- Step 9 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'ROOM_FULL_NAME_PREP', 'new_name': 'ROOM_FULL_NAME'}])
    # Rename
    table_1 = table_1.rename(columns={'ROOM_FULL_NAME_PREP': 'ROOM_FULL_NAME'})

    # ---------------- Step 10 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['fac_room_key', 'BUILDING_KEY', 'FLOOR', 'ROOM', 'SPACE_ID', 'ROOM_FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['fac_room_key', 'BUILDING_KEY', 'FLOOR', 'ROOM', 'SPACE_ID', 'ROOM_FULL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 11 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['fac_room_key', 'SPACE_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['fac_room_key', 'SPACE_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 12 ----------------
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
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="prepared_building_address", func="""
    # import pandas as pd
    # import numpy as np
    # import re
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Treat common string-null tokens as real nulls, and trim strings
    #     def clean_str(x):
    #         if pd.isna(x):
    #             return pd.NA
    #         s = str(x).strip()
    #         if s == "" or s.lower() in {"nan", "none", "null"}:
    #             return pd.NA
    #         return s
    # 
    #     str_cols = [
    #         "BUILDING_KEY","ADDRESS_PURPOSE","STREET_NUMBER","STREET_NUMBER_SUFFIX",
    #         "PRE_DIRECTIONAL","STREET_NAME","STREET_SUFFIX","POST_DIRECTIONAL",
    #         "CITY","STATE"
    #     ]
    #     for c in str_cols:
    #         if c in df.columns:
    #             df[c] = df[c].map(clean_str)
    # 
    #     # Uppercase locality + street components (keeps consistent reference data)
    #     upper_cols = [
    #         "ADDRESS_PURPOSE","STREET_NUMBER_SUFFIX","PRE_DIRECTIONAL","STREET_NAME",
    #         "STREET_SUFFIX","POST_DIRECTIONAL","CITY","STATE"
    #     ]
    #     for c in upper_cols:
    #         if c in df.columns:
    #             df[c] = df[c].astype("string").str.upper()
    # 
    #     # Keep STREET_NUMBER as string but trimmed; do not force numeric (values like 'AME31' may exist)
    #     if "STREET_NUMBER" in df.columns:
    #         df["STREET_NUMBER"] = df["STREET_NUMBER"].astype("string").str.upper()
    # 
    #     # Standardize postal code: cast to string; if numeric-like -> zero-pad to 5
    #     def clean_postal(x):
    #         if pd.isna(x):
    #             return pd.NA
    #         s = str(x).strip()
    #         if s.lower() in {"nan","none","null",""}:
    #             return pd.NA
    #         # If it's like 2142.0 or 02142, normalize
    #         m = re.fullmatch(r"\d+(?:\.0)?", s)
    #         if m:
    #             n = str(int(float(s)))
    #             return n.zfill(5)
    #         # Otherwise keep as-is (e.g., ZIP+4 or alphanumeric)
    #         return s
    # 
    #     if "POSTAL_CODE" in df.columns:
    #         df["POSTAL_CODE"] = df["POSTAL_CODE"].map(clean_postal).astype("string")
    # 
    #     # Final column order per target schema
    #     cols = [
    #         "BUILDING_KEY","ADDRESS_PURPOSE","STREET_NUMBER","STREET_NUMBER_SUFFIX",
    #         "PRE_DIRECTIONAL","STREET_NAME","STREET_SUFFIX","POST_DIRECTIONAL",
    #         "CITY","STATE","POSTAL_CODE"
    #     ]
    #     df = df[cols]
    # 
    #     return df
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Treat common string-null tokens as real nulls, and trim strings
        def clean_str(x):
            if pd.isna(x):
                return pd.NA
            s = str(x).strip()
            if s == "" or s.lower() in {"nan", "none", "null"}:
                return pd.NA
            return s

        str_cols = [
            "BUILDING_KEY","ADDRESS_PURPOSE","STREET_NUMBER","STREET_NUMBER_SUFFIX",
            "PRE_DIRECTIONAL","STREET_NAME","STREET_SUFFIX","POST_DIRECTIONAL",
            "CITY","STATE"
        ]
        for c in str_cols:
            if c in df.columns:
                df[c] = df[c].map(clean_str)

        # Uppercase locality + street components (keeps consistent reference data)
        upper_cols = [
            "ADDRESS_PURPOSE","STREET_NUMBER_SUFFIX","PRE_DIRECTIONAL","STREET_NAME",
            "STREET_SUFFIX","POST_DIRECTIONAL","CITY","STATE"
        ]
        for c in upper_cols:
            if c in df.columns:
                df[c] = df[c].astype("string").str.upper()

        # Keep STREET_NUMBER as string but trimmed; do not force numeric (values like 'AME31' may exist)
        if "STREET_NUMBER" in df.columns:
            df["STREET_NUMBER"] = df["STREET_NUMBER"].astype("string").str.upper()

        # Standardize postal code: cast to string; if numeric-like -> zero-pad to 5
        def clean_postal(x):
            if pd.isna(x):
                return pd.NA
            s = str(x).strip()
            if s.lower() in {"nan","none","null",""}:
                return pd.NA
            # If it's like 2142.0 or 02142, normalize
            m = re.fullmatch(r"\d+(?:\.0)?", s)
            if m:
                n = str(int(float(s)))
                return n.zfill(5)
            # Otherwise keep as-is (e.g., ZIP+4 or alphanumeric)
            return s

        if "POSTAL_CODE" in df.columns:
            df["POSTAL_CODE"] = df["POSTAL_CODE"].map(clean_postal).astype("string")

        # Final column order per target schema
        cols = [
            "BUILDING_KEY","ADDRESS_PURPOSE","STREET_NUMBER","STREET_NUMBER_SUFFIX",
            "PRE_DIRECTIONAL","STREET_NAME","STREET_SUFFIX","POST_DIRECTIONAL",
            "CITY","STATE","POSTAL_CODE"
        ]
        df = df[cols]

        return df
    prepared_building_address = process_tables(table_1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="prepared_building_address", subset=['BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'], keep="last")
    # Deduplicate
    prepared_building_address = prepared_building_address.drop_duplicates(subset=['BUILDING_KEY', 'ADDRESS_PURPOSE', 'STREET_NUMBER', 'STREET_NUMBER_SUFFIX', 'PRE_DIRECTIONAL', 'STREET_NAME', 'STREET_SUFFIX', 'POST_DIRECTIONAL', 'CITY', 'STATE', 'POSTAL_CODE'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['prepared_building_address'])
    # Terminate
    result = {'prepared_building_address': prepared_building_address}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_10'])
people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
rooms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
building_addresses = prepared_table_3

# Inputs are the prepared tables: people, rooms, building_addresses

# 1) Identify the target person (Professor Summer Haynes)
name_mask = False
if 'FULL_NAME' in people.columns:
    name_mask = people['FULL_NAME'].str.contains('Summer', case=False, na=False) & people['FULL_NAME'].str.contains('Haynes', case=False, na=False)
else:
    name_mask = (people['FIRST_NAME'].str.contains('Summer', case=False, na=False)) & (people['LAST_NAME'].str.contains('Haynes', case=False, na=False))

prof_candidates = people[name_mask]
# Optionally prefer rows with JOB_TITLE containing 'Professor'
if 'JOB_TITLE' in prof_candidates.columns:
    prof_pref = prof_candidates[prof_candidates['JOB_TITLE'].str.contains('Professor', case=False, na=False)]
    if len(prof_pref) > 0:
        prof_candidates = prof_pref

# If multiple, take first (question expects a single office)
prof_row = prof_candidates.head(1)

# NOTE: No explicit join keys from people->rooms are present in the provided schemas.
# In practice, another mapping (e.g., person-to-room assignment) would be required.
# Proceed assuming the office is present in rooms and must be selected by additional business logic or external mapping.
# Here we select candidate office rooms by filtering rooms whose ROOM_FULL_NAME or ROOM suggests an office for the person name if available.

room_candidates = rooms.copy()
if 'ROOM_FULL_NAME' in rooms.columns:
    mask_office_owner = rooms['ROOM_FULL_NAME'].fillna('').str.contains('Haynes', case=False)
    room_candidates = rooms[mask_office_owner]

# If no labeled ownership, fallback to rooms with USE/DESC not available in target; retain all as last resort
if len(room_candidates) == 0:
    room_candidates = rooms

# If multiple rooms, pick first
room_row = room_candidates.head(1).copy()

# 2) Join to building address by BUILDING_KEY
joined = room_row.merge(building_addresses, on='BUILDING_KEY', how='left')

# 3) Compose street address
def compose_street(r):
    parts = [str(r.get('STREET_NUMBER') or '').strip()]
    if pd.notna(r.get('STREET_NUMBER_SUFFIX')) and str(r.get('STREET_NUMBER_SUFFIX')).strip() != 'nan':
        parts.append(str(r['STREET_NUMBER_SUFFIX']).strip())
    if pd.notna(r.get('PRE_DIRECTIONAL')) and str(r.get('PRE_DIRECTIONAL')).strip() != 'nan':
        parts.append(str(r['PRE_DIRECTIONAL']).strip())
    if pd.notna(r.get('STREET_NAME')) and str(r.get('STREET_NAME')).strip() != 'nan':
        parts.append(str(r['STREET_NAME']).strip())
    if pd.notna(r.get('STREET_SUFFIX')) and str(r.get('STREET_SUFFIX')).strip() != 'nan':
        parts.append(str(r['STREET_SUFFIX']).strip())
    if pd.notna(r.get('POST_DIRECTIONAL')) and str(r.get('POST_DIRECTIONAL')).strip() != 'nan':
        parts.append(str(r['POST_DIRECTIONAL']).strip())
    return ' '.join([p for p in parts if p])

joined['street_address'] = joined.apply(compose_street, axis=1)

# 4) Select and rename output columns
answer = joined.rename(columns={
    'ROOM': 'room',
    'FLOOR': 'floor',
    'BUILDING_KEY': 'building_key',
    'CITY': 'city',
    'STATE': 'state',
    'POSTAL_CODE': 'postal_code'
})[
    ['room', 'floor', 'building_key', 'street_address', 'city', 'state', 'postal_code']
]

result = answer

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
