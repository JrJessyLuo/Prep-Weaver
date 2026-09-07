import pandas as pd

authors = tables["table_1"].copy()
pa = tables["table_2"].copy()
papers = tables["table_3"].copy()

# Normalize author_id in authors
authors["author_id_norm"] = (
    authors["author_id"].astype(str).str.strip().str.strip('"').str.strip("'")
)

# Split paper_author_combined into paper_id and author_id, normalize author_id
pa_split = pa["paper_author_combined"].astype(str).str.split("|", n=1, expand=True)
pa["paper_id"] = pa_split[0]
pa["author_id_norm"] = pa_split[1].astype(str).str.strip().str.strip('"').str.strip("'")

# Normalize year and filter to 2009
papers["year_norm"] = papers["year"].astype(str).str.strip().str.strip('"').str.strip("'")
papers_2009 = papers.loc[papers["year_norm"] == "2009", ["paper_id"]].dropna()

# Count papers per author in 2009
pa_2009 = pa.merge(papers_2009, on="paper_id", how="inner")
counts = (
    pa_2009.drop_duplicates(subset=["paper_id", "author_id_norm"])
    .groupby("author_id_norm", as_index=False)["paper_id"]
    .nunique()
    .rename(columns={"paper_id": "paper_count"})
)

top_author = counts.sort_values(["paper_count", "author_id_norm"], ascending=[False, True]).head(1)

# Join to get author name
out = top_author.merge(authors[["author_id_norm", "name"]], on="author_id_norm", how="left")
out["author_name"] = out["name"].fillna(out["author_id_norm"])
out = out[["author_name"]].reset_index(drop=True)

result = {"author_with_most_papers_2009": out}
