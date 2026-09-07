import pandas as pd

cards = tables["table_1"]
legal = tables["table_2"]
rulings_wide = tables["table_3"]

# --- Rulings: wide (date rows) -> long (card_id, ruling_text) ---
rulings_long = rulings_wide.melt(id_vars=["id"], var_name="card_id", value_name="ruling_text")
rulings_long = rulings_long.dropna(subset=["ruling_text"])
rulings_long["card_id"] = pd.to_numeric(rulings_long["card_id"], errors="coerce")
rulings_long = rulings_long.dropna(subset=["card_id"])
rulings_long["card_id"] = rulings_long["card_id"].astype("int64")

target_ruling_ids = rulings_long.loc[
    rulings_long["ruling_text"].eq("This is a triggered mana ability."),
    "card_id"
].drop_duplicates()

# --- Premodern legal ids ---
premodern_legal_ids = legal.loc[legal["sts_premodern"].eq("Legal"), "id"].drop_duplicates()

# --- Single-faced: no otherFaceIds (treat NaN / empty / [] / ['...'] strings) ---
other_face = cards["otherFaceIds"]
single_faced_mask = other_face.isna() | other_face.astype(str).str.strip().isin(["", "[]", "nan", "None"])

# --- Combine filters ---
filtered = cards.loc[
    cards["id"].isin(premodern_legal_ids)
    & cards["id"].isin(target_ruling_ids)
    & single_faced_mask
]

result = {
    "premodern_triggered_mana_ability_single_faced_count": pd.DataFrame(
        {"number_of_cards": [filtered["id"].nunique()]}
    )
}
