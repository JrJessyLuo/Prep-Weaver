import pandas as pd

# Tables are already loaded in scope as `tables`
circuits = tables["table_1"]
races = tables["table_2"]

# Find circuits used for the Malaysian Grand Prix
malaysian_gp = races.loc[races["name"] == "Malaysian Grand Prix"].copy()
circuit_ids = sorted(malaysian_gp["circuitId"].unique().tolist())

# Get location and coordinates for those circuits
answer_df = circuits.loc[
    circuits["circuitId"].isin(circuit_ids),
    ["name", "location", "country", "lat", "lng"],
].copy().reset_index(drop=True)

# Final output per guidelines
result = {"malaysian_grand_prix_location_coordinates": answer_df}