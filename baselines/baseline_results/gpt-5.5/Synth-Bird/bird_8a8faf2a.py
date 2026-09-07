import pandas as pd

circuits = tables["table_1"]
races = tables["table_2"]

sepang_ids = circuits.loc[circuits["name"].eq("Sepang International Circuit"), "circuitId"].unique()

out = (
    races.loc[races["circuitId"].isin(sepang_ids), ["year", "round", "name", "date", "time"]]
    .sort_values(["year", "round"], kind="mergesort")
    .reset_index(drop=True)
)

result = {"sepang_race_times": out}
