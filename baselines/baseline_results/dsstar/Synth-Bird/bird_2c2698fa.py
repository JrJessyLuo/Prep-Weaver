import pandas as pd

# Tables already loaded in scope as `tables`
lap_times = tables["table_2"]   # bird_2c2698fa_input_1.pkl
races = tables["table_10"]      # formula_1_races.pkl
circuits = tables["table_3"]    # formula_1_circuits.pkl

# Filter to Lewis Hamilton (driverId == 1)
ham_laps = lap_times[lap_times["driverId"] == 1].copy()
if ham_laps.empty:
    raise ValueError("No lap-times rows available for Lewis Hamilton (driverId=1).")

# Find his minimum milliseconds row (fastest lap)
best_lap_row = ham_laps.loc[ham_laps["milliseconds"].idxmin()]

# Join to races -> circuits to get circuit details
best_race = races.loc[races["raceId"] == int(best_lap_row["raceId"])].iloc[0]
best_circuit = circuits.loc[circuits["circuitId"] == int(best_race["circuitId"])].iloc[0]

# Final answer table (position during fastest lap; include circuit name for clarity)
answer = pd.DataFrame([{
    "circuit_name": best_circuit["name"],
    "position": int(best_lap_row["position"]),
}])

result = {"lewis_hamilton_fastest_lap_circuit_position": answer}