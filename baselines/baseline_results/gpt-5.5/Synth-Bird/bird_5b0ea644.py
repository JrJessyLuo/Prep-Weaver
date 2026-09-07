import pandas as pd

cards = tables["table_1"]
set_lang = tables["table_5"]

# Set codes that have French as an available language
french_setcodes = set_lang.loc[set_lang["language"].eq("French"), "setCode"].dropna().unique()

# Filter cards illustrated by Volkan BaÇµa (robust to minor encoding issues)
mask_artist = (
    cards["artist"].fillna("").str.contains("Volkan", case=False, regex=False)
    & cards["artist"].fillna("").str.contains("Ba", case=False, regex=False)
)

filtered = cards.loc[mask_artist & cards["setCode"].isin(french_setcodes)]

num_cards = filtered["uuid"].nunique()

result = {
    "volkan_baça_french_cards_count": pd.DataFrame({"num_cards": [num_cards]})
}
