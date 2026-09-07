import pandas as pd

# Tables are preloaded in-scope as `tables`
circuits = tables["table_1"]
races = tables["table_2"]

circuit_id = circuits.loc[circuits["name"].eq("Sepang International Circuit"), "circuitId"].iloc[0]
sepang_races = races.loc[races["circuitId"].eq(circuit_id)].copy()

sepang_race_times = (
    sepang_races.loc[:, ["year", "date", "time"]]
    .dropna(subset=["time"])
    .drop_duplicates()
    .assign(date=lambda df: pd.to_datetime(df["date"], errors="coerce"))
    .sort_values(["date", "time"], na_position="last")
    .reset_index(drop=True)
)

result = {"sepang_international_circuit_race_times": sepang_race_times}