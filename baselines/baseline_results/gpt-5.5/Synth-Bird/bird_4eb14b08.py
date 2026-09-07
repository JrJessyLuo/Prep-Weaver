import pandas as pd

cards = tables["table_1"].copy()
leg = tables["table_2"].copy()

# Clean up potential quoting/whitespace
for c in ["id", "shili_id", "shuxing_zhi"]:
    if c in leg.columns:
        leg[c] = (
            leg[c]
            .astype(str)
            .str.strip()
            .str.replace('"', "", regex=False)
            .str.replace("'", "", regex=False)
        )

# Find rows indicating "restricted" status (could appear in either column)
mask_restricted = (
    leg["shuxing_zhi"].str.contains(r"\brestricted\b", case=False, na=False)
    | leg["id"].str.contains(r"\brestricted\b", case=False, na=False)
)

restricted_ids = pd.to_numeric(leg.loc[mask_restricted, "shili_id"], errors="coerce")
restricted_ids = restricted_ids.dropna().astype("int64").unique()

# Pick the card identifier column that best matches these ids
candidate_keys = [
    "multiverseId",
    "mtgoId",
    "mtgArenaId",
    "cardKingdomId",
    "cardKingdomFoilId",
    "tcgplayerProductId",
    "mcmId",
    "mcmMetaId",
    "id",
]

best_key = None
best_hits = -1
for k in candidate_keys:
    if k in cards.columns:
        s = pd.to_numeric(cards[k], errors="coerce")
        hits = int(s.isin(restricted_ids).sum())
        if hits > best_hits:
            best_hits = hits
            best_key = k

if best_key is None or len(restricted_ids) == 0:
    count_val = 0
else:
    starter_mask = cards["isStarter"].fillna(0).astype(int).eq(1)
    key_vals = pd.to_numeric(cards[best_key], errors="coerce")
    restricted_starter = cards.loc[starter_mask & key_vals.isin(restricted_ids)]
    # Count distinct cards (prefer uuid if available)
    count_val = (
        restricted_starter["uuid"].nunique()
        if "uuid" in restricted_starter.columns
        else len(restricted_starter)
    )

result = {
    "restricted_starter_card_count": pd.DataFrame(
        {"restricted_starter_card_count": [int(count_val)]}
    )
}
