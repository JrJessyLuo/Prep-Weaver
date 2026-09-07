import pandas as pd

# Use preloaded tables (no file I/O)
jd_lx_df = tables["table_1"]
labels_df = tables["table_2"]

# Filter carcinogenic molecules (label_value == '+') and collect molecule_ids
carcinogenic_labels_df = labels_df.loc[labels_df["label_value"] == "+"].copy()
carcinogenic_molecule_ids = carcinogenic_labels_df["molecule_id"].dropna().unique().tolist()

# -------------------------------
# 1) Deduplicate bonds by bond_id
# -------------------------------
# Parse jd_lx into components to canonicalize bond direction (a_b same as b_a)
bond_parts = jd_lx_df["jd_lx"].fillna("").astype(str).str.extract(
    r"^(?P<mol>[^_]+)_(?P<a>\d+)_(?P<b>\d+)(?P<bt>.*)$"
)
jd_lx_df["_mol"] = bond_parts["mol"]
jd_lx_df["_a"] = pd.to_numeric(bond_parts["a"], errors="coerce")
jd_lx_df["_b"] = pd.to_numeric(bond_parts["b"], errors="coerce")

a_min = jd_lx_df[["_a", "_b"]].min(axis=1)
b_max = jd_lx_df[["_a", "_b"]].max(axis=1)

# Canonical bond_id (same for 1_2 and 2_1). If parsing fails, fall back to original jd_lx string.
jd_lx_df["_bond_id"] = (
    jd_lx_df["_mol"].fillna("") + "_"
    + a_min.fillna(-1).astype("Int64").astype(str) + "_"
    + b_max.fillna(-1).astype("Int64").astype(str)
)
jd_lx_df["_bond_id"] = jd_lx_df["_bond_id"].where(
    jd_lx_df["_mol"].notna(),
    jd_lx_df["jd_lx"].fillna("").astype(str),
)

# Deduplicate by bond_id (keep first)
jd_lx_dedup_df = jd_lx_df.drop_duplicates(subset=["_bond_id"], keep="first").copy()

# -------------------------------
# 2) Count double bonds per carcinogenic molecule
# -------------------------------
carcinogenic_jd_lx_dedup_df = jd_lx_dedup_df.loc[
    jd_lx_dedup_df["fz_id"].isin(carcinogenic_molecule_ids)
].copy()

carcinogenic_jd_lx_dedup_df["is_double_bond"] = (
    carcinogenic_jd_lx_dedup_df["jd_lx"].fillna("").astype(str).str.contains("=", regex=False)
)

double_bonds_by_molecule = (
    carcinogenic_jd_lx_dedup_df.groupby("fz_id", as_index=False)["is_double_bond"]
    .sum()
    .rename(columns={"fz_id": "molecule_id", "is_double_bond": "double_bond_rows"})
)

# -------------------------------
# 3) Pick the molecule with the most double bonds (ties: molecule_id ascending)
# -------------------------------
max_double_bond_molecule_df = (
    double_bonds_by_molecule.sort_values(["double_bond_rows", "molecule_id"], ascending=[False, True])
    .head(1)
    .reset_index(drop=True)
)

# Final answer (per guidelines)
result = {"most_double_bonds_carcinogenic_molecule": max_double_bond_molecule_df}