import pandas as pd

t1 = tables["table_1"].copy()

# Build collection name from prefix+suffix
t1["Collection_Name"] = t1["Name_Prefix"].fillna("").astype(str) + t1["Name_Suffix"].fillna("").astype(str)

# Get Collection_ID(s) for the collection named 'Best'
best_ids = t1.loc[t1["Collection_Name"].str.strip().eq("Best"), "Collection_ID"].unique()

# Count distinct collections related via Parent_Collection_ID
related_count = t1.loc[t1["Parent_Collection_ID"].isin(best_ids), "Collection_ID"].nunique()

result = {
    "related_collections_count": pd.DataFrame(
        {"number_of_related_collections": [related_count]}
    )
}
