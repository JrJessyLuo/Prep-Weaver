import pandas as pd
import numpy as np

# Input DataFrames from provided `tables` dict
df_city_combined = tables['table_1']  # corresponds to spider_877d96a1_input_0.pkl
df_city_info = tables['table_2']      # corresponds to spider_877d96a1_input_1.pkl

# Parse 'coordinates' into numeric latitude and longitude
def split_coords(val):
    if pd.isna(val):
        return pd.Series([pd.NA, pd.NA], index=["lat", "lon"])
    lat_str, lon_str = str(val).split(",", 1)
    return pd.Series([float(lat_str), float(lon_str)], index=["lat", "lon"])

coords_df = df_city_info["coordinates"].apply(split_coords)
df_city_info = pd.concat([df_city_info.drop(columns=["coordinates"]), coords_df], axis=1)

# Keep only rows with valid lat/lon
df_valid = df_city_info.dropna(subset=["lat", "lon"]).copy()

# Convert degrees to radians for vectorized computation
lat_rad = np.radians(df_valid["lat"].to_numpy())
lon_rad = np.radians(df_valid["lon"].to_numpy())

# Prepare for broadcasting
lat1 = lat_rad[:, None]  # shape (n,1)
lat2 = lat_rad[None, :]  # shape (1,n)
lon1 = lon_rad[:, None]
lon2 = lon_rad[None, :]

# Haversine formula
dlat = lat2 - lat1
dlon = lon2 - lon1
a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
c = 2 * np.arcsin(np.sqrt(a))

# Earth's radius in kilometers
R = 6371.0088
dist_matrix_km = R * c  # shape (n, n)

# Build distance matrix DataFrame keyed by city_code
city_codes = df_valid["city_code"].to_list()
df_distance = pd.DataFrame(dist_matrix_km, index=city_codes, columns=city_codes)

# Compute average distance to all other cities (exclude self-distance)
n = df_distance.shape[0]
avg_dist = (df_distance.sum(axis=1) - 0.0) / (n - 1) if n > 1 else pd.Series(0.0, index=df_distance.index)

# Map city_code to city_name (assume df_city_info has 'city_code' and 'city_name')
code_to_name = df_valid.set_index("city_code")["city_name"]

result_df = pd.DataFrame({
    "city_name": code_to_name.loc[avg_dist.index].values,
    "avg_distance_km": avg_dist.values
})
# Optional: sort by city_name for readability
result_df = result_df.sort_values(by="city_name").reset_index(drop=True)

# Package final result
result = {"city_average_distance": result_df}