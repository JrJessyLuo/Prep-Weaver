import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Build alignment name (e.g., "G"+"ood" -> "Good")
t1["alignment"] = t1["qz"].fillna("").astype(str) + t1["hz"].fillna("").astype(str)

# Extract alignment_id from combined_ids (last token)
t2["alignment_id"] = (
    t2["combined_ids"].astype(str).str.split("|").str[-1].pipe(pd.to_numeric, errors="coerce").astype("Int64")
)

# Join to get alignment label and filter neutral
neutral_names = (
    t2.merge(t1[["id", "alignment"]], left_on="alignment_id", right_on="id", how="left")
      .loc[lambda df: df["alignment"].str.strip().str.lower().eq("neutral"), ["superhero_name"]]
      .dropna()
      .drop_duplicates()
      .sort_values("superhero_name")
      .reset_index(drop=True)
)

result = {"neutral_alignment_superheroes": neutral_names}
