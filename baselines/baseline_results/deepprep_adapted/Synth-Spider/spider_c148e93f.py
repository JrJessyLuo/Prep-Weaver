import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="pairwise_distance_long", func="""
    # import pandas as pd
    # import numpy as np
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    # 
    #     # Expect two special rows identified by the first column (city1_code):
    #     # one row provides city2_code per column, one row provides distance per column.
    #     first_col = df.columns[0]
    #     row_city2 = df[df[first_col].astype(str).str.lower().eq("city2_code")]
    #     row_dist  = df[df[first_col].astype(str).str.lower().eq("distance")]
    # 
    #     # Fallback: if not found, just return empty with target schema
    #     if row_city2.empty or row_dist.empty:
    #         return pd.DataFrame(columns=["city1_code","city2_code","distance"])
    # 
    #     row_city2 = row_city2.iloc[0]
    #     row_dist = row_dist.iloc[0]
    # 
    #     city_cols = [c for c in df.columns if c != first_col]
    # 
    #     out = pd.DataFrame({
    #         "city1_code": city_cols,
    #         "city2_code": [row_city2[c] for c in city_cols],
    #         "distance":  [row_dist[c] for c in city_cols],
    #     })
    # 
    #     out["city1_code"] = out["city1_code"].astype(str)
    #     out["city2_code"] = out["city2_code"].astype(str)
    #     out["distance"] = pd.to_numeric(out["distance"], errors="coerce")
    # 
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()

        # Expect two special rows identified by the first column (city1_code):
        # one row provides city2_code per column, one row provides distance per column.
        first_col = df.columns[0]
        row_city2 = df[df[first_col].astype(str).str.lower().eq("city2_code")]
        row_dist  = df[df[first_col].astype(str).str.lower().eq("distance")]

        # Fallback: if not found, just return empty with target schema
        if row_city2.empty or row_dist.empty:
            return pd.DataFrame(columns=["city1_code","city2_code","distance"])

        row_city2 = row_city2.iloc[0]
        row_dist = row_dist.iloc[0]

        city_cols = [c for c in df.columns if c != first_col]

        out = pd.DataFrame({
            "city1_code": city_cols,
            "city2_code": [row_city2[c] for c in city_cols],
            "distance":  [row_dist[c] for c in city_cols],
        })

        out["city1_code"] = out["city1_code"].astype(str)
        out["city2_code"] = out["city2_code"].astype(str)
        out["distance"] = pd.to_numeric(out["distance"], errors="coerce")

        return out
    pairwise_distance_long = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="pairwise_distance_long", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     df = table_1.copy()
    #     first_col = df.columns[0]
    # 
    #     # identify the special rows
    #     city2_mask = df[first_col].astype(str).str.strip().str.lower().eq("city2_code")
    #     dist_mask  = df[first_col].astype(str).str.strip().str.lower().eq("distance")
    # 
    #     if city2_mask.sum() == 0 or dist_mask.sum() == 0:
    #         return pd.DataFrame(columns=["city1_code","city2_code","distance"])
    # 
    #     row_city2 = df.loc[city2_mask].iloc[0]
    #     row_dist  = df.loc[dist_mask].iloc[0]
    # 
    #     records = []
    #     # iterate by column POSITION to handle duplicate column names safely
    #     for i in range(1, df.shape[1]):
    #         city1 = str(df.columns[i])
    #         city2 = row_city2.iloc[i]
    #         dist  = row_dist.iloc[i]
    #         records.append((city1, city2, dist))
    # 
    #     out = pd.DataFrame(records, columns=["city1_code","city2_code","distance"])
    #     out["city1_code"] = out["city1_code"].astype(str).str.strip()
    #     out["city2_code"] = out["city2_code"].astype(str).str.strip()
    #     out["distance"] = pd.to_numeric(out["distance"], errors="coerce")
    #     return out
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        df = table_1.copy()
        first_col = df.columns[0]

        # identify the special rows
        city2_mask = df[first_col].astype(str).str.strip().str.lower().eq("city2_code")
        dist_mask  = df[first_col].astype(str).str.strip().str.lower().eq("distance")

        if city2_mask.sum() == 0 or dist_mask.sum() == 0:
            return pd.DataFrame(columns=["city1_code","city2_code","distance"])

        row_city2 = df.loc[city2_mask].iloc[0]
        row_dist  = df.loc[dist_mask].iloc[0]

        records = []
        # iterate by column POSITION to handle duplicate column names safely
        for i in range(1, df.shape[1]):
            city1 = str(df.columns[i])
            city2 = row_city2.iloc[i]
            dist  = row_dist.iloc[i]
            records.append((city1, city2, dist))

        out = pd.DataFrame(records, columns=["city1_code","city2_code","distance"])
        out["city1_code"] = out["city1_code"].astype(str).str.strip()
        out["city2_code"] = out["city2_code"].astype(str).str.strip()
        out["distance"] = pd.to_numeric(out["distance"], errors="coerce")
        return out
    pairwise_distance_long = process_tables(table_1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="pairwise_distance_long", subset=['distance'], how="any")
    # DropNulls
    pairwise_distance_long = pairwise_distance_long.dropna(subset=['distance'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="pairwise_distance_long", columns=['city1_code', 'city2_code', 'distance'])
    # SelectCol
    _cols = [c for c in ['city1_code', 'city2_code', 'distance'] if c in pairwise_distance_long.columns]
    pairwise_distance_long = pairwise_distance_long[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Terminate(result=['pairwise_distance_long'])
    # Terminate
    result = {'pairwise_distance_long': pairwise_distance_long}
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
    # OutlierDetection(table_name="table_1", column_name="latitude", action="delete")
    # OutlierDetection (IQR method)
    _q1 = table_1['latitude'].quantile(0.25)
    _q3 = table_1['latitude'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_latitude_is_outlier'] = table_1['latitude'].apply(lambda x: True if x < _low or x > _high else False)
    if 'delete' == 'delete':
        table_1 = table_1[table_1['table_1_latitude_is_outlier'] == False]
        table_1.drop(columns=['table_1_latitude_is_outlier'], inplace=True)
    elif 'delete' == 'add_tag':
        table_1['table_1_latitude_is_outlier'] = table_1['table_1_latitude_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # OutlierDetection(table_name="table_1", column_name="longitude", action="delete")
    # OutlierDetection (IQR method)
    _q1 = table_1['longitude'].quantile(0.25)
    _q3 = table_1['longitude'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_longitude_is_outlier'] = table_1['longitude'].apply(lambda x: True if x < _low or x > _high else False)
    if 'delete' == 'delete':
        table_1 = table_1[table_1['table_1_longitude_is_outlier'] == False]
        table_1.drop(columns=['table_1_longitude_is_outlier'], inplace=True)
    elif 'delete' == 'add_tag':
        table_1['table_1_longitude_is_outlier'] = table_1['table_1_longitude_is_outlier'].astype(bool)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="city_code", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["city_code"] = table_1["city_code"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="state", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["state"] = table_1["state"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="country", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     # normalize common variants for the US
    #     if s in ["USA", "US", "U.S.", "U.S.A", "U.S.A.", "UNITED STATES", "UNITED STATES OF AMERICA"]:
    #         return "USA"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        # normalize common variants for the US
        if s in ["USA", "US", "U.S.", "U.S.A", "U.S.A.", "UNITED STATES", "UNITED STATES OF AMERICA"]:
            return "USA"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["country"] = table_1["country"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="city_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # keep simple title-casing for consistent mapping; preserves spacing nicely
    #     return " ".join([w.capitalize() for w in s.split()])
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # keep simple title-casing for consistent mapping; preserves spacing nicely
        return " ".join([w.capitalize() for w in s.split()])
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["city_name"] = table_1["city_name"].apply(_std_apply)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['city_code', 'city_name', 'state', 'country', 'latitude', 'longitude'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['city_code', 'city_name', 'state', 'country', 'latitude', 'longitude'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['city_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['city_code'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['city_code', 'city_name', 'state', 'country', 'latitude', 'longitude'])
    # SelectCol
    _cols = [c for c in ['city_code', 'city_name', 'state', 'country', 'latitude', 'longitude'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_city_distances = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_cities = prepared_table_2

# prepared_city_distances: columns [city1_code, city2_code, distance]
# prepared_cities: columns [city_code, city_name, state, country, latitude, longitude]

# Normalize city_name for matching user input
cities = prepared_cities.copy()
cities['city_name_norm'] = cities['city_name'].str.strip().str.lower()

# Map user cities to codes
user_city_a = 'Boston'
user_city_b = 'Newark'
code_a = cities.loc[cities['city_name_norm'] == user_city_a.strip().lower(), 'city_code'].iloc[0]
code_b = cities.loc[cities['city_name_norm'] == user_city_b.strip().lower(), 'city_code'].iloc[0]

# Filter the distance for the unordered pair (either direction)
mask = ((prepared_city_distances['city1_code'] == code_a) & (prepared_city_distances['city2_code'] == code_b)) | \
       ((prepared_city_distances['city1_code'] == code_b) & (prepared_city_distances['city2_code'] == code_a))
result = prepared_city_distances.loc[mask, ['city1_code','city2_code','distance']].copy()

# Optionally attach names for readability (not required for computation)
result = result.merge(prepared_cities[['city_code','city_name']], left_on='city1_code', right_on='city_code', how='left') \
               .rename(columns={'city_name':'city1_name'}).drop(columns=['city_code'])
result = result.merge(prepared_cities[['city_code','city_name']], left_on='city2_code', right_on='city_code', how='left') \
               .rename(columns={'city_name':'city2_name'}).drop(columns=['city_code'])

# Final answer frame
answer = result[['city1_name','city2_name','distance']]

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
