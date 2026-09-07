import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="name", mode="mode")
    # MissingValueImputation
    table_1["name"] = table_1["name"].fillna(table_1["name"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="age", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['age'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['age']
    if _dtype == "datetime64":
        table_1['age'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['age'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['age'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['age'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return row['age'] >= 20 and row['age'] <= 30
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return row['age'] >= 20 and row['age'] <= 30
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['sid', 'name', 'age'])
    # SelectCol
    _cols = [c for c in ['sid', 'name', 'age'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['xh', 'bh', 'day'])
    # SelectCol
    _cols = [c for c in ['xh', 'bh', 'day'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="day", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip().strip('"').strip("'")
    #     # Expect patterns like 9/12 or 09/12; normalize to MM/DD
    #     m = re.fullmatch(r'(\d{1,2})/(\d{1,2})', s)
    #     if m:
    #         mm, dd = m.groups()
    #         return f"{int(mm):02d}/{int(dd):02d}"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip().strip('"').strip("'")
        # Expect patterns like 9/12 or 09/12; normalize to MM/DD
        m = re.fullmatch(r'(\d{1,2})/(\d{1,2})', s)
        if m:
            mm, dd = m.groups()
            return f"{int(mm):02d}/{int(dd):02d}"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["day"] = table_1["day"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['xh', 'bh', 'day'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['xh', 'bh', 'day'], keep='first').reset_index(drop=True)

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Mars", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Mars"] = table_1["Mars"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Legacy", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or pd.isna(s):
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or pd.isna(s):
            return None
        s = str(s).strip().strip('"').strip("'")
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Legacy"] = table_1["Legacy"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Mars", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or pd.isna(s):
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or pd.isna(s):
            return None
        s = str(s).strip().strip('"').strip("'")
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Mars"] = table_1["Mars"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Melon", func="""
    # import pandas as pd
    # def transform_func(s):
    #     if s is None or (isinstance(s, float) and pd.isna(s)) or pd.isna(s):
    #         return None
    #     s = str(s).strip().strip('"').strip("'")
    #     if s.lower() in ["nan", "none", "null", ""]:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None or (isinstance(s, float) and pd.isna(s)) or pd.isna(s):
            return None
        s = str(s).strip().strip('"').strip("'")
        if s.lower() in ["nan", "none", "null", ""]:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Melon"] = table_1["Melon"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Stack(table_name="table_1", id_vars=['bid'], value_vars=['Legacy', 'Mars', 'Melon'], var_name="source_col", value_name="boat_name")
    # Stack
    table_1 = table_1.melt(id_vars=['bid'], value_vars=['Legacy', 'Mars', 'Melon'], var_name='source_col', value_name='boat_name')
    table_1 = table_1.dropna(subset=['boat_name'])

    # ---------------- Step 6 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     return row['boat_name'] is not None and not pd.isna(row['boat_name']) and str(row['boat_name']).strip() != ''
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return row['boat_name'] is not None and not pd.isna(row['boat_name']) and str(row['boat_name']).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['bid', 'boat_name'])
    # SelectCol
    _cols = [c for c in ['bid', 'boat_name'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_bookings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_boats = prepared_table_3

# prepared_people: select needed columns
prepared_people = table_1[['sid','name','age']].copy()

# prepared_bookings: select needed columns
prepared_bookings = table_2[['xh','bh','day']].copy()

# prepared_boats: unpivot wide boat-name columns into a single 'boat_name'
boat_name_cols = [c for c in table_3.columns if c != 'bid']
long = table_3.melt(id_vars=['bid'], value_vars=boat_name_cols, var_name='name_col', value_name='boat_name')
prepared_boats = long.dropna(subset=['boat_name'])[['bid','boat_name']].drop_duplicates()

# Integration
people_bookings = prepared_people.merge(prepared_bookings, left_on='sid', right_on='xh', how='inner')
people_bookings_boats = people_bookings.merge(prepared_boats, left_on='bh', right_on='bid', how='inner')

# Apply question-specific filtering: age between 20 and 30 inclusive
people_bookings_boats['age'] = pd.to_numeric(people_bookings_boats['age'], errors='coerce')
filtered = people_bookings_boats[(people_bookings_boats['age'] >= 20) & (people_bookings_boats['age'] <= 30)]

# Get the names of the boats booked
answer = filtered['boat_name'].dropna().drop_duplicates().tolist()
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
