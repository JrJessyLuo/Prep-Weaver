import pandas as pd

# Access pre-loaded tables
df_docs = tables['table_1']        # spider_3fbfe563_input_0.pkl
df_process = tables['table_2']     # spider_3fbfe563_input_1.pkl
df_proc_map = tables['table_3']    # spider_3fbfe563_input_2.pkl

# Reproduce title construction and locate the target document
df_docs_local = df_docs.copy()
df_docs_local["title"] = df_docs_local["category_prefix"].fillna("") + " " + df_docs_local["connector"].fillna("") + " " + df_docs_local["topic"].fillna("")
df_docs_local["title"] = df_docs_local["title"].str.strip()

target_title = "Travel to Brazil"
doc_match = df_docs_local.loc[df_docs_local["title"] == target_title, ["document_id", "title"]]

# Join through the process mapping to get process_id(s)
# Assumed keys based on typical schema: df_proc_map links documents to processes
# Try common key names; align on 'document_id' and 'process_id' if present
left = doc_match
right = df_proc_map

# Identify likely key columns
doc_id_col_left = "document_id"
doc_id_col_right = "document_id" if "document_id" in right.columns else None
proc_id_col = "process_id" if "process_id" in right.columns else None

# Proceed only if keys are present
if doc_id_col_right is not None and proc_id_col is not None:
    mapped = left.merge(right[[doc_id_col_right, proc_id_col]], left_on=doc_id_col_left, right_on=doc_id_col_right, how="left")
else:
    mapped = left.copy()
    mapped[proc_id_col or "process_id"] = pd.NA

# Join to process table to fetch process name
# Assume common column names like 'process_id' and 'process_name' or 'name'
proc_name_col = "process_name" if "process_name" in df_process.columns else ("name" if "name" in df_process.columns else None)
if proc_name_col is not None and (proc_id_col or "process_id") in mapped.columns and "process_id" in df_process.columns:
    final = mapped.merge(df_process[["process_id", proc_name_col]], on="process_id", how="left")
else:
    final = mapped.copy()
    final["process_name"] = pd.NA
    proc_name_col = "process_name"

# Prepare final answer DataFrame with minimal columns
answer = final[[doc_id_col_left, "title", proc_name_col]].drop_duplicates().rename(columns={proc_name_col: "process_name"})

# Package result
result = {"process_name_for_travel_to_brazil": answer}