import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# --- process outcome code -> description (table_1 is wide, single-row mapping) ---
row = t1[t1["process_outcome_code"].eq("process_outcome_description")]
if row.empty:
    row = t1.head(1)
row = row.iloc[0].drop(labels=["process_outcome_code"], errors="ignore")
outcome_map = row.to_dict()

# --- process status code -> description (table_2 is key-value) ---
status_map = (
    t2[t2["attribute"].eq("process_status_description")]
    .drop_duplicates(subset=["process_status_code"])
    .set_index("process_status_code")["value"]
    .to_dict()
)

# --- document 0 ---
doc0 = t3[t3["document_id"].eq(0)].head(1).copy()
doc0["process_outcome_code_norm"] = (
    doc0["process_outcome_code"].astype(str).str.strip().str.replace(r"[!]+$", "", regex=True)
)

out = pd.DataFrame(
    {
        "process_outcome_description": doc0["process_outcome_code_norm"].map(outcome_map).values,
        "process_status_description": doc0["process_status_code"].map(status_map).values,
    }
)

result = {"document_0_process_descriptions": out}
