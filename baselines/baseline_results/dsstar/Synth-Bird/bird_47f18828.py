import pandas as pd

# Tables already loaded in-scope as `tables`
formula_1_results = tables["table_3"]         # bird_47f18828_input_2.pkl
formula_1_races_eav = tables["table_2"]       # bird_47f18828_input_1.pkl

# Filter for driverId == 1 (Lewis Hamilton) and extract unique raceIds
race_ids_for_driver_1 = formula_1_results.loc[
    formula_1_results["driverId"] == 1, "raceId"
].unique()

# Filter to attr=='year' for Hamilton raceIds, convert val to int, and return sorted distinct years
hamilton_years = (
    formula_1_races_eav.loc[
        (formula_1_races_eav["raceId"].isin(race_ids_for_driver_1))
        & (formula_1_races_eav["attr"].eq("year")),
        "val",
    ]
    .dropna()
    .astype(int)
    .drop_duplicates()
    .sort_values()
)

answer_df = pd.DataFrame({"year": hamilton_years.to_numpy()})

result = {"lewis_hamilton_participation_years": answer_df}