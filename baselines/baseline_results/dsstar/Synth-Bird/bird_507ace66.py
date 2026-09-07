import pandas as pd

# Tables (already loaded in scope)
races_eav = tables["table_2"]   # bird_507ace66_input_1.pkl
results = tables["table_3"]     # bird_507ace66_input_2.pkl
status = tables["table_13"]     # formula_1_status.pkl

# Get raceIds where year == 2007
race_ids_year_2007 = set(
    races_eav.loc[
        (races_eav["attribute"] == "year")
        & (races_eav["value"].astype(str) == "2007"),
        "raceId",
    ]
)

# Get raceIds where name == "Bahrain Grand Prix"
race_ids_bahrain_gp = set(
    races_eav.loc[
        (races_eav["attribute"] == "name")
        & (races_eav["value"] == "Bahrain Grand Prix"),
        "raceId",
    ]
)

# Intersection gives the raceId(s) for the 2007 Bahrain Grand Prix
race_ids_2007_bahrain_gp = sorted(race_ids_year_2007 & race_ids_bahrain_gp)
if not race_ids_2007_bahrain_gp:
    raise ValueError("No raceId found for the 2007 Bahrain Grand Prix.")
race_id = race_ids_2007_bahrain_gp[0]

# Count drivers whose status != "Finished"
results_2007_bahrain = results.loc[results["raceId"] == race_id].copy()
results_with_status = results_2007_bahrain.merge(status, on="statusId", how="left")

not_finished_count = int((results_with_status["status"] != "Finished").sum())

# Final answer table
answer_df = pd.DataFrame({"not_finished_drivers": [not_finished_count]})

result = {"answer": answer_df}