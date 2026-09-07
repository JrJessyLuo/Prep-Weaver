import pandas as pd
import html

# Tables
authors = tables["table_1"].copy()
authorship = tables["table_2"].copy()

# Normalize author_id formats
authors["author_id"] = (
    authors["author_id"]
    .astype(str)
    .str.replace('"', "", regex=False)
    .str.strip()
)
authorship["author_id"] = authorship["author_id"].astype(str).str.strip()

# Count distinct papers per author and filter
paper_counts = (
    authorship.groupby("author_id", as_index=False)["paper_id"]
    .nunique()
    .rename(columns={"paper_id": "paper_count"})
)
gt50 = paper_counts.loc[paper_counts["paper_count"] > 50, ["author_id"]]

# Extract author name from combined field and decode HTML entities
authors["author_name"] = (
    authors["name_email_combined"]
    .astype(str)
    .str.split(r"\|\|\|", n=1, expand=True)[0]
    .replace({"nan": pd.NA, "None": pd.NA})
)
authors["author_name"] = authors["author_name"].apply(
    lambda x: html.unescape(x) if pd.notna(x) else x
)

# Join and produce final output
out = (
    gt50.merge(authors[["author_id", "author_name"]], on="author_id", how="left")
    .dropna(subset=["author_name"])
    .drop_duplicates(subset=["author_name"])
    .sort_values("author_name")
    .reset_index(drop=True)[["author_name"]]
)

result = {"authors_more_than_50_papers": out}
