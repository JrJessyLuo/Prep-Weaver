import pandas as pd
import numpy as np

# Tables are already loaded in scope as `tables`
cards = tables["table_1"]
translations = tables["table_2"]

# Filter Story Spotlight cards
story_spotlight_cards = cards[cards["isStorySpotlight"] == 1].copy()

def normalize_uuid(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
         .str.strip()
         .str.lower()
         .replace({"": pd.NA, "nan": pd.NA, "none": pd.NA})
    )

# --- Normalize join keys (UUID) ---
story_spotlight_cards["_uuid_norm"] = normalize_uuid(story_spotlight_cards["uuid"])
translations["_uuid_norm"] = normalize_uuid(translations["uuid"])

# Attempt join using normalized UUIDs
joined_uuid = story_spotlight_cards.merge(
    translations,
    on="_uuid_norm",
    how="inner",
    suffixes=("_card", "_tr"),
)

matched_story_cards = joined_uuid["_uuid_norm"].nunique()
use_fallback = (len(joined_uuid) == 0) or (matched_story_cards == 0)

joined = joined_uuid
join_method = "uuid_norm"

# Fallback to multiverseId if UUID join doesn't work
if use_fallback:
    story_mv = story_spotlight_cards.get("multiverseId", pd.Series([pd.NA] * len(story_spotlight_cards)))
    tr_mv = translations.get("multiverseid", pd.Series([pd.NA] * len(translations)))

    story_spotlight_cards["_mv_norm"] = pd.to_numeric(story_mv, errors="coerce").astype("Int64")
    translations["_mv_norm"] = pd.to_numeric(tr_mv, errors="coerce").astype("Int64")

    joined_mv = story_spotlight_cards.merge(
        translations,
        on="_mv_norm",
        how="inner",
        suffixes=("_card", "_tr"),
    )
    joined = joined_mv
    join_method = "multiverseId"

# Compute percentage of French rows in the chosen joined dataset
total_joined_rows = len(joined)
french_rows = joined["language_name"].astype("string").str.startswith("French", na=False).sum()
percentage_french = 100.0 * float(french_rows) / float(total_joined_rows) if total_joined_rows else float("nan")

answer_df = pd.DataFrame(
    {
        "join_method_used": [join_method],
        "total_joined_rows": [int(total_joined_rows)],
        "french_rows": [int(french_rows)],
        "percentage_french": [percentage_french],
    }
)

result = {"percentage_french_story_spotlight": answer_df}