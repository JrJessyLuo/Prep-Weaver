import pandas as pd

# Input tables are already loaded in `tables`
df_atoms = tables["table_1"]   # atom_id, fz_id, ys
df_bonds = tables["table_2"]   # molecule_id, bond_id_type

# --- Reproduce reference logic to get ONLY-single-bond molecule set ---
df_bonds = df_bonds.copy()
df_bonds["bond_type_marker"] = df_bonds["bond_id_type"].astype(str).str.extract(r"\|(.+)$", expand=False)
single_bond_mask = df_bonds["bond_type_marker"].eq("-")

mol_has_any = df_bonds.groupby("molecule_id").size()
mol_has_non_single = df_bonds.loc[~single_bond_mask].groupby("molecule_id").size()
molecules_only_single = mol_has_any.index.difference(mol_has_non_single.index)

# --- Elements = unique atom types (ys) among atoms in ONLY-single-bond molecules ---
atoms_only_single = df_atoms[df_atoms["fz_id"].isin(molecules_only_single)].copy()
n_elements = atoms_only_single["ys"].nunique(dropna=True)

answer_df = pd.DataFrame({"elements_count": [int(n_elements)]})
result = {"single_bond_molecules_elements_count": answer_df}