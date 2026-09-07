import pandas as pd

# Tables already loaded in scope as `tables`
circuits = tables["table_1"]
races = tables["table_2"]

# Filter to year 2005 and dates in September 2005
races_2005_sept = races[(races["year"] == 2005) & (races["date"].astype(str).str.startswith("2005-09"))]

# Join on cid (races) == circuitId (circuits) and select required columns
answer_df = (
    races_2005_sept.merge(
        circuits[["circuitId", "name", "location_country"]],
        left_on="cid",
        right_on="circuitId",
        how="inner",
    )
    .loc[:, ["gp", "name", "location_country"]]
)

# Final result dict (only final table)
result = {"september_2005_f1_races_with_circuit_and_location": answer_df}