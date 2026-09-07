import pandas as pd
import numpy as np

# Use the provided tables dict; cities data corresponds to tables['table_2']
cities_df = tables['table_2'].copy()

# Normalize city_name and state for robust matching (strip spaces, case-insensitive)
cities_df['city_name_norm'] = cities_df['city_name'].astype(str).str.strip().str.lower()
cities_df['state_norm'] = cities_df['state'].astype(str).str.strip().str.upper()

# Disambiguate Newark: select Newark in New Jersey (NJ) and closest to the given coordinates if multiple
target_city = 'newark'
target_state = 'NJ'
target_lat, target_lon = 40.737, -74.167

newark_candidates = cities_df[
    (cities_df['city_name_norm'] == target_city) &
    (cities_df['state_norm'] == target_state)
].copy()

# If multiple, pick the one nearest to the provided coordinates
newark_candidates['dist_ref'] = np.sqrt(
    (newark_candidates['latitude'] - target_lat)**2 +
    (newark_candidates['longitude'] - target_lon)**2
)
newark_nj = newark_candidates.sort_values('dist_ref').iloc[0]

# Boston fixed coordinates (per reference)
boston_lat, boston_lon = 42.362, -71.050

# Haversine distance function
def haversine(lat1, lon1, lat2, lon2, radius_km=6371.0088):
    lat1_rad, lon1_rad = np.radians([lat1, lon1])
    lat2_rad, lon2_rad = np.radians([lat2, lon2])
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat/2.0)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return radius_km * c

distance_km = haversine(boston_lat, boston_lon, float(newark_nj['latitude']), float(newark_nj['longitude']))

# Prepare final result DataFrame
answer_df = pd.DataFrame([{
    'from_city': 'Boston, MA (fixed coords)',
    'from_latitude': boston_lat,
    'from_longitude': boston_lon,
    'to_city': f"{newark_nj['city_name']}, {newark_nj['state']}",
    'to_latitude': float(newark_nj['latitude']),
    'to_longitude': float(newark_nj['longitude']),
    'haversine_distance_km': distance_km
}])

# Assign to result dict as required
result = {
    'boston_to_newark_distance': answer_df
}