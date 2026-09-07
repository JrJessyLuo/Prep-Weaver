import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Pivot league key-value table to wide format
t1["league_id"] = t1["id"].astype(str).str.replace('"', "", regex=False).astype(int)
league_wide = (
    t1.pivot_table(index="league_id", columns="attribute", values="value", aggfunc="first")
      .reset_index()
)

# Find country for "Italy Serie A"
league_row = league_wide[league_wide["name"].astype(str) == "Italy Serie A"].copy()
league_row["country_id"] = pd.to_numeric(league_row["country_id"], errors="coerce")

out = (
    league_row.merge(t2, left_on="country_id", right_on="sid", how="left")[["mc"]]
    .rename(columns={"mc": "country"})
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"league_country": out}
