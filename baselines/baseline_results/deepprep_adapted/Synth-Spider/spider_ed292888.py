import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="first_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip().title()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip().title()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["first_name"] = table_1["first_name"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="middle_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.title() if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.title() if s != "" and s.lower() != "nan" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["middle_name"] = table_1["middle_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="last_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.title() if s != "" and s.lower() != "nan" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.title() if s != "" and s.lower() != "nan" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["last_name"] = table_1["last_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="user_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['user_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['user_id']
    if _dtype == "datetime64":
        table_1['user_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['user_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['user_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['user_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="user_address_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['user_address_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['user_address_id']
    if _dtype == "datetime64":
        table_1['user_address_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['user_address_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['user_address_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['user_address_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['user_id', 'user_address_id', 'first_name', 'middle_name', 'last_name'])
    # SelectCol
    _cols = [c for c in ['user_id', 'user_address_id', 'first_name', 'middle_name', 'last_name'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="property_address_id", mode="mode")
    # MissingValueImputation
    table_1["property_address_id"] = table_1["property_address_id"].fillna(table_1["property_address_id"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="property_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['property_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['property_id']
    if _dtype == "datetime64":
        table_1['property_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['property_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['property_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['property_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="property_address_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['property_address_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['property_address_id']
    if _dtype == "datetime64":
        table_1['property_address_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['property_address_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['property_address_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['property_address_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="owner_user_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['owner_user_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['owner_user_id']
    if _dtype == "datetime64":
        table_1['owner_user_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['owner_user_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['owner_user_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['owner_user_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['property_id', 'property_address_id', 'owner_user_id', 'property_name'])
    # SelectCol
    _cols = [c for c in ['property_id', 'property_address_id', 'owner_user_id', 'property_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
    # StandardizeString(table_name="table_1", column_name="country", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = ' '.join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = ' '.join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["country"] = table_1["country"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="address_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['address_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['address_id']
    if _dtype == "datetime64":
        table_1['address_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['address_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['address_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['address_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['address_id', 'line_1_number_building', 'line_2_number_street', 'line_3_area_locality', 'town_city', 'zip_postcode', 'county_state_province', 'country'])
    # SelectCol
    _cols = [c for c in ['address_id', 'line_1_number_building', 'line_2_number_street', 'line_3_area_locality', 'town_city', 'zip_postcode', 'county_state_province', 'country'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_users = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_properties = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_addresses = prepared_table_3

owned = prepared_users.merge(prepared_properties, left_on='user_id', right_on='owner_user_id', how='inner')
residents = owned[owned['user_address_id'] == owned['property_address_id']]
# Optional: enrich with address details (not required to form names)
residents = residents.merge(prepared_addresses, left_on='user_address_id', right_on='address_id', how='left')
residents['full_name'] = residents[['first_name','middle_name','last_name']].fillna('').agg(' '.join, axis=1).str.replace('  +',' ', regex=True).str.strip()
answer = residents[['full_name']].drop_duplicates().sort_values('full_name')

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
