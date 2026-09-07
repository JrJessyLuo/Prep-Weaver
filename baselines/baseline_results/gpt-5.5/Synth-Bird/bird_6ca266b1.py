import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Carcinogenic molecules (assume label_value "+" means carcinogenic)
carc = t2[(t2["label_type"] == "label") & (t2["label_value"] == "+")][["molecule_id"]].drop_duplicates()

# Extract bond type symbol from jd_lx (e.g., "...-" / "...=" / "...#")
t1["bond_type"] = t1["jd_lx"].astype(str).str.extract(r'([=\-#])\s*$', expand=False)

# Count double bonds per molecule (drop duplicates in case bonds are repeated)
double_counts = (
    t1.drop_duplicates(subset=["fz_id", "jd_lx"])
      .loc[t1["bond_type"] == "=", ["fz_id"]]
      .rename(columns={"fz_id": "molecule_id"})
      .merge(carc, on="molecule_id", how="inner")
      .groupby("molecule_id", as_index=False)
      .size()
      .rename(columns={"size": "double_bond_count"})
)

# If no double bonds found, still return the carcinogenic molecule(s) with 0
if double_counts.empty:
    out = carc.copy()
    out["double_bond_count"] = 0
    out = out.sort_values(["double_bond_count", "molecule_id"], ascending=[False, True]).head(1).reset_index(drop=True)
else:
    out = double_counts.sort_values(["double_bond_count", "molecule_id"], ascending=[False, True]).head(1).reset_index(drop=True)

result = {"carcinogenic_molecule_with_most_double_bonds": out}
