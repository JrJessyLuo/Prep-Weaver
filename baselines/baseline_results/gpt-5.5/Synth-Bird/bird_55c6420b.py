import pandas as pd

df_cards = tables["table_1"]
df_lang = tables["table_2"]

# Story Spotlight cards (distinct printings by uuid)
spotlight_uuids = (
    df_cards.loc[df_cards["isStorySpotlight"].eq(1), "uuid"]
    .dropna()
    .drop_duplicates()
)
total_spotlight = int(spotlight_uuids.shape[0])

# Extract language from "language_name" (e.g., "French|<card name>")
lang = df_lang[["uuid", "language_name"]].dropna(subset=["uuid", "language_name"]).copy()
lang["language"] = lang["language_name"].astype(str).str.split("|", n=1).str[0].str.strip()

french_spotlight = lang.loc[
    lang["uuid"].isin(set(spotlight_uuids)) & lang["language"].eq("French"),
    "uuid",
].nunique()

percentage_french = (french_spotlight / total_spotlight * 100) if total_spotlight else 0.0

result = {
    "french_percentage_among_story_spotlight": pd.DataFrame(
        {"percentage_french": [percentage_french]}
    )
}
