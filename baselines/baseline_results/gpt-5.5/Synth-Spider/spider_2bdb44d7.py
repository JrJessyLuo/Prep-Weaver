import pandas as pd

docs = tables["table_1"][["document_id"]].drop_duplicates()

proc_docs_2 = tables["table_2"][["document_id"]].dropna().drop_duplicates()
proc_docs_9 = tables["table_9"][["document_id"]].dropna().drop_duplicates()

proc_docs = pd.concat([proc_docs_2, proc_docs_9], ignore_index=True).drop_duplicates()

out = (
    docs.merge(proc_docs, on="document_id", how="left", indicator=True)
        .query("_merge == 'left_only'")[["document_id"]]
        .sort_values("document_id")
        .reset_index(drop=True)
)

result = {"document_ids_without_process": out}
