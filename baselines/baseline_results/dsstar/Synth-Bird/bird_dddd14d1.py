import pandas as pd

# Input tables (already loaded)
skin_df = tables["table_1"]
heroes_df = tables["table_2"]

# 1) Parse profile_ids in the superheroes table into individual profile_id rows
hero_profiles = heroes_df[["id", "superhero_name", "profile_ids"]].copy()
hero_profiles["profile_ids"] = hero_profiles["profile_ids"].fillna("").astype(str)

hero_profile_map = (
    hero_profiles.assign(profile_id=hero_profiles["profile_ids"].str.split("|"))
    .explode("profile_id")
    .drop(columns=["profile_ids"])
)

hero_profile_map["profile_id"] = pd.to_numeric(hero_profile_map["profile_id"], errors="coerce")
hero_profile_map = hero_profile_map.dropna(subset=["profile_id"]).copy()
hero_profile_map["profile_id"] = hero_profile_map["profile_id"].astype("int64")

# 2) Join profile_id values to the colour table on id, then filter "No Colour" (or null)
joined = hero_profile_map.merge(
    skin_df.rename(columns={"id": "profile_id"}),
    on="profile_id",
    how="inner",
)

no_colour_joined = joined.loc[
    joined["base_colour"].eq("No Colour") | joined["base_colour"].isna(),
    ["id", "superhero_name", "profile_id", "base_colour", "accent_colour"],
].copy()

# 3) Compute mean number of such profiles per distinct superhero
per_hero_counts = (
    no_colour_joined.groupby(["id", "superhero_name"], as_index=False)
    .size()
    .rename(columns={"size": "no_colour_profile_count"})
)

avg_no_colour_profiles_per_hero = (
    float(per_hero_counts["no_colour_profile_count"].mean()) if len(per_hero_counts) else 0.0
)

answer_df = pd.DataFrame(
    {"avg_no_colour_profiles_per_hero": [avg_no_colour_profiles_per_hero]}
)

result = {"average_superheroes_with_no_skin_colour": answer_df}