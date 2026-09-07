import pandas as pd

bonds = tables["table_1"].copy()
atoms = tables["table_3"].copy()

# single bonds indicated by non-null "-" column
single = bonds[bonds["-"].notna()].copy()

# parse bond_id like "TR001_1_8" -> molecule_id, atom_num_1, atom_num_2
parts = single["bond_id"].astype(str).str.split("_", n=2, expand=True)
single["molecule_id"] = parts[0]
single["atom_id_1"] = parts[0] + "_" + parts[1]
single["atom_id_2"] = parts[0] + "_" + parts[2]

# attach element info for each atom
a1 = atoms[["atom_id", "element"]].rename(columns={"atom_id": "atom_id_1", "element": "element_1"})
a2 = atoms[["atom_id", "element"]].rename(columns={"atom_id": "atom_id_2", "element": "element_2"})

out = (
    single[["bond_id", "molecule_id", "atom_id_1", "atom_id_2"]]
    .merge(a1, on="atom_id_1", how="left")
    .merge(a2, on="atom_id_2", how="left")
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"single_bond_connected_atoms": out}
