import pandas as pd

# Load tables
authors = tables["table_1"].copy()
paper_authors = tables["table_2"].copy()
cit = tables["table_3"].copy()

# --- Clean/standardize author_id for joining ---
authors["author_id"] = (
    authors["author_id"]
    .astype(str)
    .str.strip()
    .str.replace('"', "", regex=False)
)
authors["author_id"] = pd.to_numeric(authors["author_id"], errors="coerce").astype("Int64")

paper_authors["author_id"] = pd.to_numeric(paper_authors["author_id"], errors="coerce").astype("Int64")

# --- Compute citations per cited paper ---
# table_3.paper_id contains comma-separated citing paper ids
cit["paper_id"] = cit["paper_id"].astype(str)
citations_per_paper = cit.assign(
    citations=cit["paper_id"].where(cit["paper_id"].str.strip().ne(""), "").apply(
        lambda s: 0 if s.strip() in ("", "nan", "None") else len([x for x in s.split(",") if x.strip()])
    )
)[["cited_paper_id", "citations"]]

# Aggregate in case cited_paper_id appears multiple times
citations_per_paper = citations_per_paper.groupby("cited_paper_id", as_index=False)["citations"].sum()

# --- Sum citations over each author's papers ---
author_citations = (
    paper_authors.merge(
        citations_per_paper,
        left_on="paper_id",
        right_on="cited_paper_id",
        how="left",
    )
    .assign(citations=lambda d: d["citations"].fillna(0))
    .groupby("author_id", as_index=False)["citations"]
    .sum()
)

# --- Get top author and their name ---
top = author_citations.sort_values(["citations", "author_id"], ascending=[False, True]).head(1)

out = top.merge(authors[["author_id", "name"]], on="author_id", how="left")
out = out.rename(columns={"citations": "number_of_citations"})[["name", "number_of_citations"]]

result = {"most_cited_author": out.reset_index(drop=True)}
