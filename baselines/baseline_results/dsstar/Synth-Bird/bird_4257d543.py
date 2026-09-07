import pandas as pd
import re

# Source tables from the provided `tables` dict (already loaded in scope)
bonds = tables["table_1"]
atoms = tables["table_3"]

# 1) Filter to single bonds where '-' is not null
single_bonds = bonds[bonds["-"].notna()].copy()

# 2) Parse bond_id like "TR001_1_8" -> molecule_id="TR001", atom_idx_1=1, atom_idx_2=8
pat = re.compile(r"^(TR\d+)_([0-9]+)_([0-9]+)$")
parsed = single_bonds["bond_id"].astype(str).str.extract(pat)
parsed.columns = ["molecule_id", "atom_idx_1", "atom_idx_2"]

bad = parsed["molecule_id"].isna()
if bad.any():
    raise ValueError(
        f"Failed to parse {bad.sum()} bond_id values. Examples: "
        f"{single_bonds.loc[bad, 'bond_id'].head(10).tolist()}"
    )

parsed["atom_idx_1"] = parsed["atom_idx_1"].astype(int)
parsed["atom_idx_2"] = parsed["atom_idx_2"].astype(int)

single_bonds_parsed = pd.concat([single_bonds.reset_index(drop=True), parsed], axis=1)

# Create endpoint atom_id strings (e.g., TR001_1 and TR001_8)
single_bonds_parsed["atom_id_1"] = (
    single_bonds_parsed["molecule_id"] + "_" + single_bonds_parsed["atom_idx_1"].astype(str)
)
single_bonds_parsed["atom_id_2"] = (
    single_bonds_parsed["molecule_id"] + "_" + single_bonds_parsed["atom_idx_2"].astype(str)
)

# Atom lookup for joining
atoms_lookup = atoms[["atom_id", "molecule_id", "element"]].copy()

# Join for endpoint 1
out = single_bonds_parsed.merge(
    atoms_lookup.rename(columns={"atom_id": "atom_id_1", "element": "element_1"}),
    on=["molecule_id", "atom_id_1"],
    how="left",
    validate="many_to_one",
)

# Join for endpoint 2
out = out.merge(
    atoms_lookup.rename(columns={"atom_id": "atom_id_2", "element": "element_2"}),
    on=["molecule_id", "atom_id_2"],
    how="left",
    validate="many_to_one",
)

# Validate mapping success
missing_1 = out["element_1"].isna()
missing_2 = out["element_2"].isna()
if missing_1.any() or missing_2.any():
    examples = out.loc[missing_1 | missing_2, ["bond_id", "molecule_id", "atom_id_1", "atom_id_2"]].head(10)
    raise ValueError(
        f"Unmapped endpoints: endpoint1_missing={missing_1.sum()}, endpoint2_missing={missing_2.sum()}. "
        f"Examples:\n{examples.to_string(index=False)}"
    )

# Final answer: atoms connected in single type bonds (with elements)
connected_atom_pairs = out[
    ["bond_id", "molecule_id", "atom_id_1", "element_1", "atom_id_2", "element_2"]
].copy()

result = {"connected_atoms_in_single_bonds": connected_atom_pairs}