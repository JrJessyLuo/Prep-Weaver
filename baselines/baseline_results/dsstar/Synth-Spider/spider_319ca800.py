import pandas as pd

# Load tables from the provided 'tables' dict
subset_details = tables['table_1']          # not used per reference logic
doc_object_metrics = tables['table_2']
subset_members = tables['table_3']
subsets = tables['table_4']
collections = tables['table_5']
doc_objects = tables['table_6']
docs_in_collections = tables['table_7']

# Reproduce the same logic as the reference code

# Subsets with their collections
subsets_with_collections = subset_members.merge(
    subsets, on="Collection_Subset_ID", how="left"
).merge(
    collections, on="Collection_ID", how="left", suffixes=("_subset", "_collection")
)

# Collections with documents
collections_with_docs = docs_in_collections.merge(
    collections, on="Collection_ID", how="left"
)

# Documents with object details and metrics
docs_full = collections_with_docs.merge(
    doc_objects, on="Document_Object_ID", how="left", suffixes=("_coll", "_doc")
).merge(
    doc_object_metrics, on="Document_Object_ID", how="left", suffixes=("", "_metric")
)

# Link subsets to documents
subsets_to_docs = subsets_with_collections.merge(
    docs_full, on="Collection_ID", how="left", suffixes=("_subset_chain", "_doc_chain")
)

# Group by subset and count distinct Document_Object_ID
answer_df = (
    subsets_to_docs.groupby(
        ["Collection_Subset_ID", "Collection_Subset_Name"], dropna=False
    )["Document_Object_ID"]
    .nunique(dropna=True)
    .reset_index(name="doc_count")
    .sort_values(["doc_count", "Collection_Subset_ID"], ascending=[False, True])
    .reset_index(drop=True)
)

# Package final result as required
result = {
    "subset_document_counts": answer_df
}