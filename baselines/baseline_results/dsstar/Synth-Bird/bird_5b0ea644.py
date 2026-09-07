import pandas as pd

# Tables are preloaded in a dict named `tables`
cards = tables["table_1"]
set_translations = tables["table_5"]

# Filter cards by artist
cards_f = cards[cards["artist"] == "Volkan BaÇµa"].copy()

# Join to set translations on setCode, then filter to French
joined = cards_f.merge(
    set_translations,
    on="setCode",
    how="inner",
)

joined_french = joined[joined["language"] == "French"].copy()

# Count distinct cards.uuid
distinct_uuid_count = joined_french["uuid"].nunique(dropna=True)

# Final answer as a DataFrame
answer_df = pd.DataFrame({"count": [distinct_uuid_count]})

# Assign to required result dict
result = {"volkan_baga_french_cards_count": answer_df}

print(distinct_uuid_count)