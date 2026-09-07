import pandas as pd
import numpy as np

df1 = tables["table_1"].copy()

# Extract the "city2_code" and "distance" rows (stored as a 2-row encoded table)
row_city2 = df1.loc[df1["city1_code"].astype(str).str.lower().eq("city2_code")]
row_dist = df1.loc[df1["city1_code"].astype(str).str.lower().eq("distance")]

# Build an edge list: city1_code (column name) -> city2_code (value in city2_code row), with distance
cols = [c for c in df1.columns if c != "city1_code"]
edges = pd.DataFrame({
    "city1_code": cols,
    "city2_code": [row_city2.iloc[0][c] if not row_city2.empty else np.nan for c in cols],
    "distance": [row_dist.iloc[0][c] if not row_dist.empty else np.nan for c in cols],
})
edges["distance"] = pd.to_numeric(edges["distance"], errors="coerce")

# Find codes for Boston and Newark from table_2 if possible; otherwise fall back to common codes
cities = tables["table_2"].copy()
cities["city_name_l"] = cities["city_name"].astype(str).str.strip().str.lower()

def get_code(city_name, fallback):
    m = cities.loc[cities["city_name_l"].eq(city_name.lower()), "city_code"]
    return m.iloc[0] if len(m) else fallback

bos_code = get_code("Boston", "BOS")
newark_code = get_code("Newark", "EWR")

# Try direct lookup from edges (either direction)
mask = (
    (edges["city1_code"].eq(bos_code) & edges["city2_code"].eq(newark_code)) |
    (edges["city1_code"].eq(newark_code) & edges["city2_code"].eq(bos_code))
)
out = edges.loc[mask, ["city1_code", "city2_code", "distance"]].copy()

# If not present, compute via haversine using table_2 coordinates
if out.empty:
    coord = cities.set_index("city_code")[["latitude", "longitude"]]
    if bos_code in coord.index and newark_code in coord.index:
        lat1, lon1 = coord.loc[bos_code]
        lat2, lon2 = coord.loc[newark_code]

        R = 3958.8  # miles
        phi1, phi2 = np.radians([lat1, lat2])
        dphi = np.radians(lat2 - lat1)
        dlmb = np.radians(lon2 - lon1)
        a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlmb / 2) ** 2
        d = 2 * R * np.arcsin(np.sqrt(a))

        out = pd.DataFrame([{
            "city1_code": bos_code,
            "city2_code": newark_code,
            "distance": float(d)
        }])
    else:
        out = pd.DataFrame([{
            "city1_code": bos_code,
            "city2_code": newark_code,
            "distance": np.nan
        }])

out = out.reset_index(drop=True)

result = {"boston_newark_distance": out}
