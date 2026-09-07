import pandas as pd

# Load tables
pub_raw = tables["table_1"].copy()
heroes = tables["table_2"].copy()

# Normalize publisher table (table_1 appears stored as lists in a single row)
if len(pub_raw) == 1 and isinstance(pub_raw.iloc[0]["bh"], (list, tuple)) and isinstance(pub_raw.iloc[0]["mc"], (list, tuple)):
    publishers = pd.DataFrame({
        "publisher_id": pub_raw.iloc[0]["bh"],
        "publisher_name": pub_raw.iloc[0]["mc"]
    })
else:
    publishers = pub_raw.rename(columns={"bh": "publisher_id", "mc": "publisher_name"})

publishers["publisher_id"] = pd.to_numeric(publishers["publisher_id"], errors="coerce")
dark_horse_ids = publishers.loc[publishers["publisher_name"].eq("Dark Horse Comics"), "publisher_id"].dropna().unique()

heroes_pub = pd.to_numeric(heroes["publisher_id"], errors="coerce")
count_dark_horse = int(heroes.loc[heroes_pub.isin(dark_horse_ids)].shape[0])

result = {
    "dark_horse_comics_superheroes_count": pd.DataFrame(
        {"number_of_superheroes": [count_dark_horse]}
    )
}
