import pandas as pd

aff_kv = tables["table_1"].copy()
pa = tables["table_2"].copy()

# Pivot affiliation key-value table to wide (e.g., name, address)
aff_wide = (
    aff_kv.pivot_table(index="affiliation_id", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)

# Prepare affiliation id in paper-author-affiliation mapping
pa["aff_id"] = pd.to_numeric(pa["aff_id"], errors="coerce")
pa_nonnull = pa.dropna(subset=["aff_id"]).copy()
pa_nonnull["affiliation_id"] = pa_nonnull["aff_id"].round().astype("Int64")

# Count distinct papers per affiliation
counts = (
    pa_nonnull.groupby("affiliation_id", as_index=False)["paper_id"]
    .nunique()
    .rename(columns={"paper_id": "total_papers"})
)

# Include all affiliations (even those with 0 papers)
out = (
    aff_wide.merge(counts, on="affiliation_id", how="left")
    .assign(total_papers=lambda d: d["total_papers"].fillna(0).astype(int))
)

# Optional: standardize affiliation name column label
if "name" in out.columns:
    out = out.rename(columns={"name": "affiliation_name"})

# Select key output columns first, keep any other affiliation attributes after
front_cols = ["affiliation_id"] + (["affiliation_name"] if "affiliation_name" in out.columns else []) + ["total_papers"]
other_cols = [c for c in out.columns if c not in front_cols]
out = out[front_cols + other_cols].sort_values(["total_papers", "affiliation_id"], ascending=[False, True]).reset_index(drop=True)

result = {"papers_per_affiliation": out}
