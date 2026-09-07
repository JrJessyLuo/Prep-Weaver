import pandas as pd

cards = tables["table_1"].copy()
rulings = tables["table_2"].copy()

# Build full UUID in rulings table
rulings["uuid"] = (
    rulings["uuid_part1"].astype(str) + "-" +
    rulings["uuid_part2"].astype(str) + "-" +
    rulings["uuid_part3"].astype(str) + "-" +
    rulings["uuid_part4"].astype(str) + "-" +
    rulings["uuid_part5"].astype(str)
)

# Earliest ruling date per card (uuid)
rulings["date"] = pd.to_datetime(rulings["date"], errors="coerce")
min_rulings = (
    rulings.dropna(subset=["uuid", "date"])
           .groupby("uuid", as_index=False)["date"]
           .min()
           .rename(columns={"date": "ruling_date"})
)

# Filter uncommon cards and join to rulings
uncommon = cards[cards["rarity"].astype(str).str.lower().eq("uncommon")].copy()
out = (
    uncommon.merge(min_rulings, on="uuid", how="inner")
            .sort_values(["ruling_date", "name"], ascending=[True, True])
            .drop_duplicates(subset=["uuid"])
            .head(3)[["name", "ruling_date"]]
            .reset_index(drop=True)
)

result = {"uncommon_cards_by_ruling_date": out}
