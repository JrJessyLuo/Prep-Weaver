import pandas as pd

# Tables are already loaded in-scope as a dict named `tables`
league_df = tables["table_1"]   # european_football_2_League.pkl
country_df = tables["table_2"]  # bird_27883e3e_input_1.pkl (sid -> mc)

# Filter for "Italy Serie A" and get its country_id
italy_serie_a = league_df.loc[league_df["name"].eq("Italy Serie A"), ["country_id"]].head(1)

# Map country_id to country name
answer_df = (
    italy_serie_a.merge(country_df, left_on="country_id", right_on="sid", how="left")
    .loc[:, ["country_id", "mc"]]
    .rename(columns={"mc": "country_name"})
)

result = {"italy_serie_a_country": answer_df}
print(result["italy_serie_a_country"]["country_name"].iloc[0])