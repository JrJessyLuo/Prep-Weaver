import pandas as pd

# Tables are already loaded in scope as `tables`
cards_df = tables["table_1"]
rulings_df = tables["table_2"]

# Filter to uncommon rarity, keeping at least id and name for joining later
uncommon_cards_df = cards_df.loc[cards_df["rarity"].eq("uncommon"), ["id", "name"]].copy()

# Convert date to datetime
rulings_df = rulings_df.copy()
rulings_df["date"] = pd.to_datetime(rulings_df["date"], errors="coerce")

# Inner-join rulings with uncommon cards on id
uncommon_rulings_df = rulings_df.merge(uncommon_cards_df, on="id", how="inner")

# Group by id/name, take min date as first_ruling_date, then sort and select top 3
top3_earliest_uncommon_rulings = (
    uncommon_rulings_df.groupby(["id", "name"], as_index=False)["date"]
    .min()
    .rename(columns={"date": "first_ruling_date"})
    .sort_values(["first_ruling_date", "name"], ascending=[True, True])
    .head(3)[["name", "first_ruling_date"]]
)

result = {"top3_earliest_uncommon_rulings": top3_earliest_uncommon_rulings}