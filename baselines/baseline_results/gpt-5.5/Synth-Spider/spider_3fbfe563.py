import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Build document name
t1["document_name"] = (
    t1["category_prefix"].astype(str).str.strip() + " " +
    t1["connector"].astype(str).str.strip() + " " +
    t1["topic"].astype(str).str.strip()
)

# Standardize process_id in table_2 to int for joining
t2["process_id_int"] = (
    t2["process_id"].astype(str)
      .str.strip()
      .str.replace('"', '', regex=False)
      .str.replace("'", "", regex=False)
)
t2["process_id_int"] = pd.to_numeric(t2["process_id_int"], errors="coerce").fillna(t2["next_process_id"]).astype("Int64")

doc_ids = t1.loc[t1["document_name"].eq("Travel to Brazil"), ["document_id"]].drop_duplicates()

out = (
    doc_ids.merge(t3[["document_id", "process_id"]], on="document_id", how="inner")
           .merge(t2[["process_id_int", "process_name"]], left_on="process_id", right_on="process_id_int", how="left")
           [["process_name"]]
           .drop_duplicates()
           .reset_index(drop=True)
)

result = {"process_name_for_document": out}
