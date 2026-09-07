import pandas as pd

races = tables["table_2"].copy()
circuits = tables["table_1"].copy()

races["date"] = pd.to_datetime(races["date"], errors="coerce")

sept_2005 = races.loc[
    (races["year"] == 2005) & (races["date"].dt.month == 9),
    ["raceId", "gp", "cid", "date"]
]

out = (
    sept_2005.merge(circuits[["circuitId", "name", "location_country"]],
                    left_on="cid", right_on="circuitId", how="left")
    .sort_values("date")
    .rename(columns={
        "gp": "race",
        "name": "circuit_name",
        "location_country": "location"
    })[["race", "circuit_name", "location"]]
    .reset_index(drop=True)
)

result = {"september_2005_f1_races": out}
