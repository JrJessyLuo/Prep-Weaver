import pandas as pd
import numpy as np
import re

t1 = tables["table_1"].copy()
cities = tables["table_2"].copy()

# Get packed segments for city2_code lists and distance lists
city2_packed = t1.loc[t1["city1_code"].eq("city2_code"), "city_data_combined"].iloc[0]
dist_packed = t1.loc[t1["city1_code"].eq("distance"), "city_data_combined"].iloc[0]

city2_segs = str(city2_packed).split("|")
dist_segs = str(dist_packed).split("|")

# Determine the city1 order from the segment that contains the most city codes
def parse_codes(seg):
    seg = str(seg).strip()
    if seg == "" or seg.lower() == "nan":
        return []
    return [c.strip() for c in seg.split(",") if c.strip() != ""]

seg_lengths = [len(parse_codes(s)) for s in city2_segs]
max_idx = int(np.argmax(seg_lengths)) if len(seg_lengths) else 0
city_order = parse_codes(city2_segs[max_idx])

# Fallback if lengths don't match
n = min(len(city_order), len(city2_segs), len(dist_segs))
city_order = city_order[:n]
city2_segs = city2_segs[:n]
dist_segs = dist_segs[:n]

rows = []
for i, city1 in enumerate(city_order):
    dseg = str(dist_segs[i]).strip()
    if dseg == "" or dseg.lower() == "nan":
        dvals = []
    else:
        # Extract numeric values robustly (handles quoted numbers)
        dvals = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", dseg)]

    d = pd.Series(dvals, dtype="float64")
    d = d[(~d.isna()) & (d != 0)]
    avg_dist = float(d.mean()) if len(d) else np.nan
    rows.append({"city_code": city1, "avg_distance": avg_dist})

avg_df = pd.DataFrame(rows)

out = avg_df.merge(cities[["city_code", "city_name"]], on="city_code", how="left")
out["city_name"] = out["city_name"].fillna(out["city_code"])
out = out[["city_name", "avg_distance"]].sort_values("city_name").reset_index(drop=True)

result = {"city_average_distance": out}
