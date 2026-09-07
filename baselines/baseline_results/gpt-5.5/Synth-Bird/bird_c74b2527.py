import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Find the league row
league_row = t1[t1["ls"].str.contains(r"Belgium Jupiler League", na=False)].head(1).copy()

# Extract league_id (prefer explicit id column; fall back to parsing ls)
if not league_row.empty:
    league_id = (
        league_row["id"].astype(str).str.strip().str.strip('"').astype(int).iloc[0]
        if "id" in league_row.columns
        else league_row["ls"].astype(str).str.extract(r"^(\d+)-", expand=False).astype(int).iloc[0]
    )
else:
    league_id = pd.NA

# Map league_id -> country_id via matches (table_3)
country_id = (
    t3.loc[t3["league_id"].eq(league_id), "country_id"].dropna().astype(int).mode().iloc[0]
    if pd.notna(league_id) and (t3["league_id"].eq(league_id).any())
    else pd.NA
)

# country_id -> country name via key-value table (table_2)
country_name = (
    t2.loc[(t2["id"].eq(country_id)) & (t2["attribute"].eq("name")), "value"]
      .astype(str).str.strip().str.strip('"')
      .iloc[0]
    if pd.notna(country_id) and ((t2["id"].eq(country_id)) & (t2["attribute"].eq("name"))).any()
    else pd.NA
)

result = {
    "belgium_jupiler_league_country": pd.DataFrame({"country": [country_name]})
}
