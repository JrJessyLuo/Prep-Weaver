import pandas as pd

cs = tables["table_1"].copy()
rel = tables["table_2"].copy()

# Keep only collection subset relations (if other subset types exist)
rel = rel[rel["subset_type"].eq("Collection_Subset_ID")].copy()

# Count distinct collections per subset
counts = (
    rel.groupby("subset_id", as_index=False)
       .agg(number_of_collections=("Collection_ID", "nunique"))
       .rename(columns={"subset_id": "Collection_Subset_ID"})
)

# Merge with subset master list; include subsets with zero collections
out = (
    cs.merge(counts, on="Collection_Subset_ID", how="left")
      .assign(number_of_collections=lambda d: d["number_of_collections"].fillna(0).astype(int))
      .loc[:, ["Collection_Subset_ID", "Collection_Subset_Name", "number_of_collections"]]
      .sort_values("Collection_Subset_ID")
      .reset_index(drop=True)
)

result = {"collection_subsets_collection_counts": out}
