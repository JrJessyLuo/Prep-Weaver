import pandas as pd

circuits = tables["table_1"]
races = tables["table_2"]
results_df = tables["table_3"]
drivers = tables["table_8"]

# Identify the circuit used for the Austrian Grand Prix
austrian_gp_races = races[races["mingcheng"].str.contains("Austrian Grand Prix", case=False, na=False)].copy()
austrian_circuit_id = austrian_gp_races["luquId"].mode().iloc[0] if not austrian_gp_races.empty else None

# All races held at that circuit
races_at_circuit = races[races["luquId"] == austrian_circuit_id][["raceId", "year", "mingcheng", "date", "luquId"]].copy()

# Fastest laps at that circuit
fl = results_df.merge(races_at_circuit, on="raceId", how="inner")
fl = fl[fl["fastestLapTime"].notna()].copy()

# Parse fastestLapTime to timedelta for min calculation
t = fl["fastestLapTime"].astype(str).str.strip()
t_norm = t.where(t.str.count(":") >= 2, "0:" + t)  # convert m:ss.xxx -> 0:m:ss.xxx
fl["fastestLapTd"] = pd.to_timedelta(t_norm, errors="coerce")
fl = fl[fl["fastestLapTd"].notna()].copy()

# Get lap record row (minimum fastest lap)
lap_record_row = fl.sort_values("fastestLapTd", ascending=True).head(1)

# Add driver and circuit info
lap_record_row = lap_record_row.merge(
    drivers[["driverId", "forename", "surname"]],
    on="driverId",
    how="left"
)
lap_record_row["driver_name"] = (lap_record_row["forename"].fillna("") + " " + lap_record_row["surname"].fillna("")).str.strip()

circuit_name = circuits.loc[circuits["circuitId"] == austrian_circuit_id, "name"]
circuit_name = circuit_name.iloc[0] if len(circuit_name) else None

out = pd.DataFrame([{
    "circuit_name": circuit_name,
    "lap_record_time": lap_record_row["fastestLapTime"].iloc[0] if len(lap_record_row) else None,
    "driver_name": lap_record_row["driver_name"].iloc[0] if len(lap_record_row) else None,
    "year": int(lap_record_row["year"].iloc[0]) if len(lap_record_row) else None,
    "race_name": lap_record_row["mingcheng"].iloc[0] if len(lap_record_row) else None,
}])

result = {"austrian_grand_prix_circuit_lap_record": out}
