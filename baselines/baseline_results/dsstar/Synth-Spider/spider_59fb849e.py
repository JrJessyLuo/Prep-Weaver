import pandas as pd

# Load input DataFrames from provided `tables` dict
aff_meta = tables['table_1']  # spider_59fb849e_input_0.pkl
paper_aff = tables['table_2']  # spider_59fb849e_input_1.pkl

# Reproduce the logic from the reference:
# - Filter rows with non-null aff_id
# - Cast aff_id to int
# - Count distinct papers per affiliation
df = paper_aff[paper_aff["aff_id"].notna()].assign(aff_id=lambda d: d["aff_id"].astype(int))
counts = df.groupby("aff_id")["paper_id"].nunique().reset_index(name="paper_count")

# Optionally enrich with affiliation metadata similar to reference (pivot attributes wide)
if "affiliation_id" in aff_meta.columns and "attribute" in aff_meta.columns and "value" in aff_meta.columns:
    aff_attrs = aff_meta.pivot_table(
        index="affiliation_id",
        columns="attribute",
        values="value",
        aggfunc="first"
    ).reset_index()
    final_counts = counts.merge(aff_attrs, left_on="aff_id", right_on="affiliation_id", how="left")
    # Keep a concise set of columns: aff_id, paper_count, name, address when available
    cols = [c for c in ["aff_id", "paper_count", "name", "address"] if c in final_counts.columns]
    answer_df = final_counts[cols].sort_values(["paper_count", "aff_id"], ascending=[False, True]).reset_index(drop=True)
else:
    answer_df = counts.sort_values(["paper_count", "aff_id"], ascending=[False, True]).reset_index(drop=True)

# Package final answer
result = {"papers_per_affiliation": answer_df}