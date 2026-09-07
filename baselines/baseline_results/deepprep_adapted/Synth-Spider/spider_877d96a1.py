import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1'], target_table="table_1_transposed", func="""
    # import pandas as pd
    # 
    # def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
    #     # Convert two-row key-value layout into single-row with columns city2_code and distance
    #     pivot = table_1.set_index("city1_code")["city_data_combined"].to_dict()
    #     return pd.DataFrame([pivot])
    # """)
    # CodeGeneration

    def process_tables(table_1: pd.DataFrame) -> pd.DataFrame:
        # Convert two-row key-value layout into single-row with columns city2_code and distance
        pivot = table_1.set_index("city1_code")["city_data_combined"].to_dict()
        return pd.DataFrame([pivot])
    table_1_transposed = process_tables(table_1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CodeGeneration(table_names=['table_1_transposed'], target_table="prepared_city_distances", func="""
    # import pandas as pd
    # import re
    # 
    # def process_tables(table_1_transposed: pd.DataFrame) -> pd.DataFrame:
    #     row = table_1_transposed.iloc[0]
    #     city_blob = row["city2_code"]
    #     dist_blob = row["distance"]
    # 
    #     # Split into aligned blocks
    #     city_blocks = str(city_blob).strip().split("|")
    #     dist_blocks = str(dist_blob).strip().split("|")
    # 
    #     def parse_city_list(seg: str):
    #         seg = seg.strip().strip('"')
    #         if not seg:
    #             return []
    #         return [c.strip().upper() for c in seg.split(",") if c.strip()]
    # 
    #     def parse_dist_list(seg: str):
    #         seg = seg.strip()
    #         if not seg:
    #             return []
    #         # Extract numbers even if wrapped in quotes like ""576","665""
    #         nums = re.findall(r"-?\d+", seg)
    #         return nums
    # 
    #     parsed_city_blocks = [parse_city_list(s) for s in city_blocks]
    #     parsed_dist_blocks = [parse_dist_list(s) for s in dist_blocks]
    # 
    #     out = []
    # 
    #     for i, (cities, dists) in enumerate(zip(parsed_city_blocks, parsed_dist_blocks)):
    #         if not cities or not dists:
    #             continue
    # 
    #         # Infer base city for this block
    #         base = None
    #         if "0" in dists and dists.index("0") < len(cities):
    #             base = cities[dists.index("0")]
    #         else:
    #             # For blocks without an explicit 0 (notably the first one), infer from next block's first city
    #             if i + 1 < len(parsed_city_blocks) and parsed_city_blocks[i + 1]:
    #                 base = parsed_city_blocks[i + 1][0]
    # 
    #         if base is None:
    #             continue
    # 
    #         # Emit long-form rows; align by position up to min length
    #         m = min(len(cities), len(dists))
    #         for j in range(m):
    #             other = cities[j]
    #             dist_val = dists[j]
    #             if other == base and dist_val == "0":
    #                 continue
    #             out.append({
    #                 "city_code": base,
    #                 "other_city_code": other,
    #                 "distance": int(dist_val)
    #             })
    # 
    #     return pd.DataFrame(out, columns=["city_code", "other_city_code", "distance"])
    # """)
    # CodeGeneration

    def process_tables(table_1_transposed: pd.DataFrame) -> pd.DataFrame:
        row = table_1_transposed.iloc[0]
        city_blob = row["city2_code"]
        dist_blob = row["distance"]

        # Split into aligned blocks
        city_blocks = str(city_blob).strip().split("|")
        dist_blocks = str(dist_blob).strip().split("|")

        def parse_city_list(seg: str):
            seg = seg.strip().strip('"')
            if not seg:
                return []
            return [c.strip().upper() for c in seg.split(",") if c.strip()]

        def parse_dist_list(seg: str):
            seg = seg.strip()
            if not seg:
                return []
            # Extract numbers even if wrapped in quotes like ""576","665""
            nums = re.findall(r"-?\d+", seg)
            return nums

        parsed_city_blocks = [parse_city_list(s) for s in city_blocks]
        parsed_dist_blocks = [parse_dist_list(s) for s in dist_blocks]

        out = []

        for i, (cities, dists) in enumerate(zip(parsed_city_blocks, parsed_dist_blocks)):
            if not cities or not dists:
                continue

            # Infer base city for this block
            base = None
            if "0" in dists and dists.index("0") < len(cities):
                base = cities[dists.index("0")]
            else:
                # For blocks without an explicit 0 (notably the first one), infer from next block's first city
                if i + 1 < len(parsed_city_blocks) and parsed_city_blocks[i + 1]:
                    base = parsed_city_blocks[i + 1][0]

            if base is None:
                continue

            # Emit long-form rows; align by position up to min length
            m = min(len(cities), len(dists))
            for j in range(m):
                other = cities[j]
                dist_val = dists[j]
                if other == base and dist_val == "0":
                    continue
                out.append({
                    "city_code": base,
                    "other_city_code": other,
                    "distance": int(dist_val)
                })

        return pd.DataFrame(out, columns=["city_code", "other_city_code", "distance"])
    prepared_city_distances = process_tables(table_1_transposed)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['prepared_city_distances'])
    # Terminate
    result = {'prepared_city_distances': prepared_city_distances}
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
    # DropNulls(table_name="table_1", subset=['city_code', 'city_name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['city_code', 'city_name'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="city_code", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding single/double quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["city_code"] = table_1["city_code"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="city_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     # normalize internal whitespace
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        # normalize internal whitespace
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["city_name"] = table_1["city_name"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['city_code', 'city_name'])
    # SelectCol
    _cols = [c for c in ['city_code', 'city_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['city_code'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['city_code'], keep='first').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_city_distances = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_city_directory = prepared_table_2

# prepared_city_distances columns: city_code, other_city_code, distance (numeric)
# prepared_city_directory columns: city_code, city_name

# 1) Join distances with city names for the base city
base_named = prepared_city_distances.merge(prepared_city_directory, how='left', on='city_code')
# 2) Optionally drop self-distances if present (distance to self should be excluded from average to 'all other cities')
base_named = base_named[base_named['city_code'] != base_named['other_city_code']]
# 3) Compute average distance to all other cities per base city
avg_dist = (base_named
            .groupby(['city_code', 'city_name'], as_index=False)['distance']
            .mean()
            .rename(columns={'distance': 'avg_distance_to_others'}))
# 4) Select required output columns: city name and the computed average
target = avg_dist[['city_name', 'avg_distance_to_others']]

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
