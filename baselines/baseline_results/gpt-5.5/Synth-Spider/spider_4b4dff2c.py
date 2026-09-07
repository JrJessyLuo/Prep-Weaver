import pandas as pd

aff = tables["table_1"].copy()
auth_pap = tables["table_2"].copy()
pap_attr = tables["table_3"].copy()

# Normalize affiliation_id types for joining
aff["affiliation_id_norm"] = (
    aff["affiliation_id"]
    .astype(str)
    .str.replace('"', "", regex=False)
    .str.strip()
)
aff["affiliation_id_norm"] = pd.to_numeric(aff["affiliation_id_norm"], errors="coerce").astype("Int64")

auth_pap["affiliation_id_norm"] = pd.to_numeric(auth_pap["affiliation_id"], errors="coerce").astype("Int64")

# Find Stanford University affiliation ids (case-insensitive contains)
stanford_aff_ids = aff.loc[
    aff["name"].astype(str).str.contains("stanford university", case=False, na=False),
    "affiliation_id_norm"
].dropna().unique()

# Build paper_id and select papers with at least one Stanford-affiliated author
auth_pap["paper_id"] = auth_pap["paper_prefix"].astype(str) + "-" + auth_pap["paper_suffix"].astype(str)
stanford_papers = auth_pap.loc[
    auth_pap["affiliation_id_norm"].isin(stanford_aff_ids),
    ["paper_id"]
].dropna().drop_duplicates()

# Extract year per paper and filter to 2000-2009
years = pap_attr.loc[pap_attr["attribute"].astype(str).str.lower().eq("year"), ["paper_id", "value"]].copy()
years["year"] = pd.to_numeric(years["value"], errors="coerce")
years = years.dropna(subset=["year"])
years = years[(years["year"] >= 2000) & (years["year"] <= 2009)][["paper_id", "year"]].drop_duplicates()

# Count distinct Stanford papers in the year range
count_val = stanford_papers.merge(years, on="paper_id", how="inner")["paper_id"].nunique()

result = {
    "stanford_papers_2000_2009_count": pd.DataFrame({"paper_count": [count_val]})
}
