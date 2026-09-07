import pandas as pd
import html

# The input tables are provided in a dict named `tables`
# Mapping:
# tables['table_1'] -> authors_df (spider_a6581a17_input_0.pkl)
# tables['table_2'] -> paper_author (spider_a6581a17_input_1.pkl)
# tables['table_3'] -> citations df (spider_a6581a17_input_2.pkl)
# tables['table_4'] -> aan_1_Affiliation.pkl (unused)
# tables['table_5'] -> aan_1_Paper.pkl (unused)

# 1) Load citations DataFrame: columns ['cited_paper_id', 'paper_id']
df = tables['table_3'].copy()

# 2) Clean and explode comma-separated citing paper_ids
edges = (
    df.assign(paper_id=df["paper_id"].astype(str).str.split(","))
      .explode("paper_id")
)

# Strip whitespace, handle NaNs safely
edges["paper_id"] = edges["paper_id"].astype(str).str.strip()
edges = edges[edges["paper_id"].ne("") & edges["paper_id"].ne("nan")]

# 3) Build edge list: citing -> cited
edge_list = edges.rename(columns={"paper_id": "citing_paper_id"})[
    ["citing_paper_id", "cited_paper_id"]
].reset_index(drop=True)

# Optional: drop potential self-citations if any
edge_list = edge_list[edge_list["citing_paper_id"] != edge_list["cited_paper_id"]].reset_index(drop=True)

# 4) Load paper-author mapping: ['paper_id', 'author_id', 'affiliation_id']
paper_author = tables['table_2'].copy()
paper_author["paper_id"] = paper_author["paper_id"].astype(str)

# 5) Join exploded citations with paper-author mapping on cited_paper_id = paper_id
citations_with_authors = edge_list.merge(
    paper_author[["paper_id", "author_id"]],
    left_on="cited_paper_id",
    right_on="paper_id",
    how="left"
).drop(columns=["paper_id"])

# 6) Group by author_id to count total citations per author
author_citation_counts = (
    citations_with_authors.dropna(subset=["author_id"])
    .groupby("author_id", as_index=False)
    .size()
    .rename(columns={"size": "total_citations"})
    .sort_values("total_citations", ascending=False)
    .reset_index(drop=True)
)

# 7) Load authors DataFrame and prepare for join
authors_df = tables['table_1'].copy()

def clean_author_id(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        s = s[1:-1]
    try:
        return int(s)
    except Exception:
        return None

authors_df["author_id_clean"] = authors_df["author_id"].apply(clean_author_id)

def decode_name(x):
    if pd.isna(x):
        return None
    return html.unescape(str(x))

authors_df["name_decoded"] = authors_df["name"].apply(decode_name)

# 8) Join top-cited authors with names
author_citation_counts["author_id"] = author_citation_counts["author_id"].astype("int64")

top_with_names = author_citation_counts.merge(
    authors_df[["author_id_clean", "name_decoded"]],
    left_on="author_id",
    right_on="author_id_clean",
    how="left"
).drop(columns=["author_id_clean"])

# 9) Handle missing names
top_with_names["name_decoded"] = top_with_names["name_decoded"].fillna("(unknown)")

# 10) Get the single author with the most citations
top_author = top_with_names.nlargest(1, "total_citations")[["name_decoded", "total_citations"]]
top_author = top_author.rename(columns={"name_decoded": "author_name", "total_citations": "citations"}).reset_index(drop=True)

# Final result as required
result = {"top_author_by_citations": top_author}