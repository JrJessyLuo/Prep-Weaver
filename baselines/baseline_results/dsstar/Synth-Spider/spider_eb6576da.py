import pandas as pd

# The input DataFrames are provided in the `tables` dict:
# tables['table_1'] -> spider_eb6576da_input_0.pkl  (not used here)
# tables['table_2'] -> spider_eb6576da_input_1.pkl  (paper_author mapping)
# tables['table_3'] -> spider_eb6576da_input_2.pkl  (papers with year and pid)
# tables['table_4'] -> aan_1_Affiliation.pkl        (not used here)
# tables['table_5'] -> aan_1_Citation.pkl           (not used here)

# Load DataFrames from provided tables mapping
paper_author_df = tables['table_2'].copy()
papers_df = tables['table_3'].copy()

# Step 1: Filter for year == 2009 and get the set of paper IDs (pid)
paper_ids_2009 = set(papers_df.loc[papers_df["year"] == 2009, "pid"])

# Step 2: Split 'paper_author' into 'paper_id' and 'author_id'
split_cols = paper_author_df["paper_author"].str.split("|", n=1, expand=True)
paper_author_df = paper_author_df.assign(paper_id=split_cols[0], author_id=split_cols[1])

# Step 3: Keep only mappings for 2009 papers
paper_author_2009 = paper_author_df[paper_author_df["paper_id"].isin(paper_ids_2009)].copy()

# Step 4: Count number of papers per author_id (each row is a paper-author mapping)
author_counts = (
    paper_author_2009
    .groupby("author_id", as_index=False)
    .agg(paper_count=("paper_id", "nunique"))
)

# Step 5: Get the author(s) with the maximum paper_count
max_count = author_counts["paper_count"].max() if not author_counts.empty else 0
top_authors = author_counts[author_counts["paper_count"] == max_count].sort_values(["paper_count", "author_id"], ascending=[False, True])

# Prepare final answer DataFrame
final_df = top_authors.reset_index(drop=True)

# Assign to result dict as required
result = {"top_author_2009_by_papers": final_df}