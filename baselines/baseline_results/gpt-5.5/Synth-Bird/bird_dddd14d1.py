import pandas as pd

colors = tables["table_1"].copy()
heroes = tables["table_2"].copy()

# Extract skin colour id from packed profile_ids (assume last token is skin_colour_id)
skin_id = heroes["profile_ids"].astype("string").str.split("|").str[-1]
heroes["skin_colour_id"] = pd.to_numeric(skin_id, errors="coerce").astype("Int64")

# Join to colour lookup and filter "No Colour" skin
merged = heroes.merge(
    colors.rename(columns={"id": "skin_colour_id"}),
    on="skin_colour_id",
    how="left"
)

no_skin = merged[
    merged["base_colour"].astype("string").str.strip().str.casefold().eq("no colour")
]

out = pd.DataFrame({
    "average_height_cm": [no_skin["height_cm"].mean()],
    "average_weight_kg": [no_skin["weight_kg"].mean()],
    "num_superheroes": [no_skin["id"].nunique()]
})

result = {"average_superheroes_no_skin_colour": out}
