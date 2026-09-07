import pandas as pd

circuits = tables["table_1"].copy()
races = tables["table_2"].copy()

# Find the circuitId(s) for Malaysian Grand Prix
malaysia_races = races[races["name"].astype(str).str.strip().str.lower() == "malaysian grand prix"]
circuit_ids = malaysia_races["circuitId"].dropna().unique()

# Join to circuits and return location coordinates
out = (
    circuits[circuits["circuitId"].isin(circuit_ids)]
    .loc[:, ["name", "location", "country", "lat", "lng"]]
    .drop_duplicates()
    .rename(columns={"name": "circuit_name", "lat": "latitude", "lng": "longitude"})
    .reset_index(drop=True)
)

result = {"malaysian_grand_prix_location_coordinates": out}
