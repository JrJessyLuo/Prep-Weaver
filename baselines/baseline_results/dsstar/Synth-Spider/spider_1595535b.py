import pandas as pd

# Access pre-loaded tables
df0 = tables['table_1']  # spider_1595535b_input_0.pkl
df1 = tables['table_2']  # spider_1595535b_input_1.pkl
df2 = tables['table_3']  # spider_1595535b_input_2.pkl

# Helper to parse heat_result 'H-M:SS.mmm' -> total seconds
def parse_heat_result(s):
    if pd.isna(s):
        return None
    _, time_part = s.split('-', 1)
    m_str, s_str = time_part.split(':', 1)
    minutes = int(m_str)
    seconds = float(s_str)
    return minutes * 60 + seconds

# Enrich cyclists with parsed heat_seconds
df1_parsed = df1.copy()
df1_parsed["heat_seconds"] = df1_parsed["heat_result"].apply(parse_heat_result)

# Threshold: 4:21.558 -> 261.558 seconds
threshold_seconds = 4 * 60 + 21.558  # 261.558

# Filter cyclists faster than threshold
fast_cyclists = df1_parsed[df1_parsed["heat_seconds"].notna() & (df1_parsed["heat_seconds"] < threshold_seconds)]

# Join: cyclists -> bridge(year) on id=cid, then to bikes on bike_id=id
merged = df2.merge(
    fast_cyclists[["id", "name", "nation", "heat_result", "heat_seconds"]],
    left_on="cid",
    right_on="id",
    how="inner"
)
merged = merged.merge(df0, left_on="bike_id", right_on="id", how="left", suffixes=("", "_bike"))

# Extract bike names by splitting product_material at '###' and taking the left part
def extract_bike_name(s):
    if pd.isna(s):
        return None
    parts = str(s).split("###", 1)
    return parts[0].strip()

merged["bike_name"] = merged["product_material"].apply(extract_bike_name)

# Get distinct bike names
distinct_bike_names = sorted([bn for bn in merged["bike_name"].dropna().unique().tolist()])

# Prepare final answer DataFrame
answer_df = pd.DataFrame({"bike_name": distinct_bike_names})

# Assign to result dict as required
result = {"distinct_bike_names": answer_df}