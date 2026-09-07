import pandas as pd

# Tables already loaded in-scope as `tables`
results = tables["table_1"]   # likely formula_1_results
races = tables["table_2"]     # races
drivers = tables["table_3"]   # drivers

# Reproduce reference logic to get raceId for 2008 Australian Grand Prix
race_2008_aus = races[(races["year"] == 2008) & (races["name"] == "Australian Grand Prix")]
raceId_2008_aus = int(str(race_2008_aus["raceId"].iloc[0]).strip('"')) if not race_2008_aus.empty else None

# Count distinct drivers from nationality == "UN" who participated in that race
race_results = results[results["raceId"] == raceId_2008_aus]
race_driver_ids = race_results["driverId"].dropna().unique()

drivers_un = drivers[drivers["nationality"] == "UN"]
num_un_drivers = drivers_un[drivers_un["driverId"].isin(race_driver_ids)]["driverId"].nunique()

answer_df = pd.DataFrame({"num_drivers_from_UN": [int(num_un_drivers)]})

result = {"answer": answer_df}