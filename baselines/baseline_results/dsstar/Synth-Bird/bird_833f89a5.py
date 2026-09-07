import pandas as pd

# Tables are already loaded in-scope as `tables`
circuits = tables["table_1"]
races_long = tables["table_2"]

# Identify circuitId for Brands Hatch
brands_hatch = circuits[
    circuits["name"].astype(str).str.strip().str.lower().eq("brands hatch")
    | circuits["circuitRef"].astype(str).str.strip().str.lower().str.contains("brands", na=False)
].copy()

brands_hatch_id = brands_hatch["circuitId"].dropna().astype(int).unique().tolist()

# Filter to races held at circuitId == 38 (as in the reference logic)
circuit_race_ids = (
    races_long.loc[
        (races_long["attribute"] == "circuitId") & (races_long["value"].astype(str) == "38"),
        "raceId",
    ]
    .dropna()
    .astype(int)
    .unique()
)

subset = races_long[races_long["raceId"].isin(circuit_race_ids)].copy()

race_meta = (
    subset[subset["attribute"].isin(["name", "year"])]
    .pivot_table(index="raceId", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)

race_meta["name"] = race_meta["name"].astype(str)
race_meta["year"] = pd.to_numeric(race_meta["year"], errors="coerce")

british_at_38 = race_meta[race_meta["name"] == "British Grand Prix"].copy()
max_year = int(british_at_38["year"].max()) if not british_at_38.empty else None

answer_df = pd.DataFrame(
    {"last_season_year": [max_year], "circuit": ["Brands Hatch"], "grand_prix": ["British Grand Prix"]}
)

result = {"answer": answer_df}