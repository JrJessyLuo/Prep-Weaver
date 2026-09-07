import pandas as pd

# Inputs are provided in the dict `tables`
authors = tables['table_1'].copy()
author_paper = tables['table_2'].copy()

# Ensure author_id is string for consistent joining
if "author_id" in authors.columns:
    authors["author_id"] = authors["author_id"].astype(str)
if "author_id" in author_paper.columns:
    author_paper["author_id"] = author_paper["author_id"].astype(str)

# Basic de-duplication
authors_clean = authors.drop_duplicates().copy()
author_paper_clean = author_paper.drop_duplicates().copy()

# Aggregation: number of unique papers per author_id
papers_per_author = (
    author_paper_clean
    .dropna(subset=["author_id"])
    .groupby("author_id", dropna=False)
    .agg(num_papers=("paper_id", "nunique"))
    .reset_index()
)

# Extract author name from name_email_combined (before '|||')
def extract_name(x):
    if pd.isna(x):
        return pd.NA
    s = str(x)
    parts = s.split("|||")
    name = parts[0].strip().strip('"').strip()
    return name if name != "" and name.lower() != "nan" else pd.NA

authors_enriched = authors_clean.copy()
if "name_email_combined" in authors_enriched.columns:
    authors_enriched["author_name"] = authors_enriched["name_email_combined"].apply(extract_name)
else:
    authors_enriched["author_name"] = pd.NA

# Filter authors with > 50 papers
prolific_authors = papers_per_author.loc[papers_per_author["num_papers"] > 50].copy()

# Join to get author names
prolific_with_names = (
    prolific_authors
    .merge(authors_enriched[["author_id", "author_name"]], on="author_id", how="left")
    .sort_values(["num_papers", "author_id"], ascending=[False, True])
    .reset_index(drop=True)
)

# Final answer: names of all authors who have more than 50 papers
# Keep unique names; include author_id to disambiguate where names are missing
final_df = prolific_with_names[["author_id", "author_name", "num_papers"]]

result = {
    "authors_with_more_than_50_papers": final_df
}