import pandas as pd

# Tables are provided in scope as `tables`
# Mapping:
# tables['table_1'] -> spider_4562fc13_input_0.pkl
# tables['table_2'] -> spider_4562fc13_input_1.pkl
# tables['table_3'] -> spider_4562fc13_input_2.pkl

df0 = tables['table_1']
df1 = tables['table_2']
df2 = tables['table_3']

# Filter df2 to document_id == 0 and get process_outcome_code and process_status_code
row_doc0 = df2[df2["document_id"] == 0][["process_outcome_code", "process_status_code"]].copy()

# Map process_outcome_code "finish!" to the column header "finish" in df0
if not row_doc0.empty and "finish" in df0.columns:
    outcome_description = df0.iloc[0]["finish"]
else:
    outcome_description = None

# Build status map from df1 where attribute == "process_status_description"
status_map = (
    df1[df1["attribute"] == "process_status_description"]
    .set_index("process_status_code")["value"]
    .to_dict()
)

# Assign descriptions
answer_df = row_doc0.assign(
    process_outcome_description=outcome_description,
    process_status_description=row_doc0["process_status_code"].map(status_map)
)[["process_outcome_description", "process_status_description"]]

# Package final result
result = {
    "document_0_outcome_and_status": answer_df
}