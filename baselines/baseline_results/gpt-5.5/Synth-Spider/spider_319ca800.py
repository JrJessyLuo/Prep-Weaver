import pandas as pd

ds = tables["table_1"].copy()
mat = tables["table_2"].copy()

# Unpivot the wide matrix into (doc_row, doc_col, subset_id)
pairs = mat.melt(
    id_vars=["Document_Object_ID"],
    var_name="Other_Document_Object_ID",
    value_name="Document_Subset_ID"
).dropna(subset=["Document_Subset_ID"])

pairs["Other_Document_Object_ID"] = pd.to_numeric(pairs["Other_Document_Object_ID"], errors="coerce")
pairs = pairs.dropna(subset=["Other_Document_Object_ID"])

pairs["Document_Object_ID"] = pairs["Document_Object_ID"].astype("int64")
pairs["Other_Document_Object_ID"] = pairs["Other_Document_Object_ID"].astype("int64")
pairs["Document_Subset_ID"] = pd.to_numeric(pairs["Document_Subset_ID"], errors="coerce").astype("Int64")

# Build membership list: each (subset_id, document_id) from both row and column docs
m1 = pairs[["Document_Subset_ID", "Document_Object_ID"]].rename(columns={"Document_Object_ID": "Document_ID"})
m2 = pairs[["Document_Subset_ID", "Other_Document_Object_ID"]].rename(columns={"Other_Document_Object_ID": "Document_ID"})
membership = pd.concat([m1, m2], ignore_index=True).drop_duplicates()

counts = (
    membership.groupby("Document_Subset_ID", as_index=False)["Document_ID"]
    .nunique()
    .rename(columns={"Document_ID": "number_of_documents"})
)

out = (
    ds.merge(counts, on="Document_Subset_ID", how="left")
      .assign(number_of_documents=lambda d: d["number_of_documents"].fillna(0).astype(int))
      [["Document_Subset_ID", "Document_Subset_Name", "number_of_documents"]]
      .sort_values("Document_Subset_ID")
      .reset_index(drop=True)
)

result = {"document_subsets_document_counts": out}
