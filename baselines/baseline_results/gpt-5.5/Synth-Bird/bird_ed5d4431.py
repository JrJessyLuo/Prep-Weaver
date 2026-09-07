import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t4 = tables["table_4"].copy()

# Build bond instance id from parts (handles cases where id is split across multiple columns)
part_cols = [c for c in ["part1", "sep1", "part2", "sep2", "part3"] if c in t1.columns]
t1[part_cols] = t1[part_cols].fillna("")
t1["bond_instance_id"] = t1[part_cols].astype(str).agg("".join, axis=1).str.strip()

bond_types = (
    t1.loc[t1["bond_instance_id"].ne(""), ["bond_instance_id", "attribute_value"]]
    .drop_duplicates(subset=["bond_instance_id"], keep="first")
    .rename(columns={"attribute_value": "bond_type"})
)

# Unique bonds per molecule from adjacency list (table_4 has both directions)
bonds = (
    t4[["bond_id"]].dropna()
    .drop_duplicates()
    .assign(molecule_id=lambda d: d["bond_id"].astype(str).str.split("_", n=1).str[0])
    .rename(columns={"bond_id": "bond_instance_id"})
)

bonds = bonds.merge(bond_types, on="bond_instance_id", how="left")

mol_bond_counts = bonds.groupby("molecule_id", as_index=False).agg(
    total_bonds=("bond_instance_id", "nunique"),
    single_bonds=("bond_type", lambda s: (s == "-").sum())
)

single_bond_molecules = mol_bond_counts.loc[
    (mol_bond_counts["total_bonds"] > 0) & (mol_bond_counts["single_bonds"] == mol_bond_counts["total_bonds"]),
    ["molecule_id"]
]

# Non-carcinogenic molecules from table_2 (normalize sign)
t2["sign_norm"] = t2["sign"].astype(str).str.strip()
non_carc = t2.loc[t2["sign_norm"].eq("-"), ["code"]].rename(columns={"code": "molecule_id"}).drop_duplicates()

count_val = (
    single_bond_molecules.merge(non_carc, on="molecule_id", how="inner")["molecule_id"]
    .nunique()
)

result = {
    "non_carcinogenic_single_bond_molecules_count": pd.DataFrame(
        {"count": [count_val]}
    )
}
