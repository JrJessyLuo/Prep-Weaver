import pandas as pd

# Tables are already loaded in scope as `tables`
alignment_df = tables["table_1"]
heroes_df = tables["table_2"]

# Normalize the alignment table into a mapping: id -> alignment label
alignment_map = (
    alignment_df.assign(
        alignment=alignment_df["qz"].fillna("").astype(str) + alignment_df["hz"].fillna("").astype(str)
    )
    .loc[:, ["id", "alignment"]]
    .dropna(subset=["id"])
)

# Detect which column in heroes_df contains alignment ids and join
alignment_id_col = None
for c in heroes_df.columns:
    if c.lower() in {"alignment_id", "alignment", "alignmentid", "alignment_id_fk"}:
        alignment_id_col = c
        break

if alignment_id_col is None:
    int_cols = [c for c in heroes_df.columns if pd.api.types.is_integer_dtype(heroes_df[c]) and c != "id"]
    candidates = []
    for c in int_cols:
        nunique = heroes_df[c].nunique(dropna=True)
        if 2 <= nunique <= 10:
            candidates.append((c, nunique))
    candidates.sort(key=lambda x: x[1])
    alignment_id_col = candidates[0][0] if candidates else None

if alignment_id_col is None:
    raise ValueError(
        "Could not find an alignment id column in the superhero table. "
        "Available columns: " + ", ".join(map(str, heroes_df.columns))
    )

# Join and extract Neutral superheroes
merged = heroes_df.merge(
    alignment_map.rename(columns={"id": alignment_id_col}),
    on=alignment_id_col,
    how="left",
)

neutral_superheroes = (
    merged.loc[merged["alignment"].astype(str).str.strip().str.lower() == "neutral", "superhero_name"]
    .astype("string")
    .str.strip()
    .replace("", pd.NA)
    .dropna()
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
)

answer_df = neutral_superheroes.to_frame(name="superhero_name")

# Final answer (as required)
result = {"neutral_alignment_superheroes": answer_df}