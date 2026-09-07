import pandas as pd

# Tables are preloaded in the provided environment
leagues = tables["table_1"]
country = tables["table_2"]

mask = leagues["ls"].astype(str).str.contains("Belgium Jupiler League", case=False, na=False)
belgium_row = leagues.loc[mask, ["id", "ls"]]
belgium_league_id = belgium_row["id"].iloc[0] if not belgium_row.empty else None

belgium_country_name = None
if belgium_league_id is not None:
    belgium_id_int = int(str(belgium_league_id).strip().strip('"'))
    name_mask = (country["id"] == belgium_id_int) & (country["attribute"] == "name")
    belgium_country_name = country.loc[name_mask, "value"].iloc[0] if name_mask.any() else None

answer_df = pd.DataFrame({"country": [belgium_country_name]})
result = {"belgium_jupiler_league_country": answer_df}