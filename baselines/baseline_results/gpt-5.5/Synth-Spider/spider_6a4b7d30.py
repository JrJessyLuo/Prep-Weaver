import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# --- Clean affiliation ids ---
t1["affiliation_id_clean"] = t1["affiliation_id"].astype(str).str.strip().str.strip('"')

t2 = t2.dropna(subset=["affiliation_id", "paper_author_combined"]).copy()
t2["affiliation_id_clean"] = t2["affiliation_id"].astype("Int64").astype(str)
t2["paper_id"] = t2["paper_author_combined"].astype(str).str.split(r"\|\|", n=1, expand=True)[0]

# --- Parse paper_info into paper_id and year ---
pi = t3["paper_info"].astype(str).str.split("|", n=2, expand=True)
papers = pd.DataFrame({
    "paper_id": pi[0],
    "year": pd.to_numeric(pi[2], errors="coerce")
})
papers_2009 = papers[papers["year"].eq(2009)][["paper_id"]].dropna().drop_duplicates()

# --- Count distinct papers per affiliation in 2009 ---
t2_2009 = t2.merge(papers_2009, on="paper_id", how="inner")
counts = (
    t2_2009[["affiliation_id_clean", "paper_id"]]
    .drop_duplicates()
    .groupby("affiliation_id_clean", as_index=False)
    .agg(number_of_papers=("paper_id", "nunique"))
)

top3 = counts.sort_values(["number_of_papers", "affiliation_id_clean"], ascending=[False, True]).head(3)

out = (
    top3.merge(t1[["affiliation_id_clean", "name"]], on="affiliation_id_clean", how="left")
    .rename(columns={"affiliation_id_clean": "affiliation_id"})
    [["affiliation_id", "name", "number_of_papers"]]
)

result = {"top_3_affiliations_2009": out.reset_index(drop=True)}
