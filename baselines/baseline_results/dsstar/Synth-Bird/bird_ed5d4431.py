import pandas as pd

# Source tables from the provided `tables` dict (already loaded, in-scope)
bond_attr = tables["table_1"]      # bird_ed5d4431_input_0.pkl
carc = tables["table_2"]           # bird_ed5d4431_input_1.pkl
connected = tables["table_4"]      # toxicology_connected.pkl

# --- Parse bond type labels from bond_attr ---
bond_type = bond_attr.loc[bond_attr["bond_id"].eq("lx"), ["part1", "attribute_value"]].rename(
    columns={"part1": "bond_id", "attribute_value": "bond_type"}
)

# Keep only plausible bond_id patterns (avoid any stray rows)
bond_type = bond_type.loc[bond_type["bond_id"].str.match(r"^TR\d+_\d+_\d+$", na=False)].copy()

# If any duplicates exist for the same bond_id, keep the first
bond_type = bond_type.drop_duplicates(subset=["bond_id"], keep="first")

# --- Join connected bonds with bond type labels ---
bonds_labeled = connected.merge(bond_type, on="bond_id", how="inner")

# Extract molecule_id from bond_id like TRxxx_i_j
bonds_labeled["molecule_id"] = bonds_labeled["bond_id"].str.extract(r"^(TR\d+)_\d+_\d+$", expand=False)
bonds_labeled = bonds_labeled.dropna(subset=["molecule_id"])

# --- Molecules whose ALL labeled bonds are single ('-') ---
mol_has_nonsingle = (
    bonds_labeled.assign(is_nonsingle=bonds_labeled["bond_type"].ne("-"))
    .groupby("molecule_id", as_index=False)["is_nonsingle"]
    .any()
    .rename(columns={"is_nonsingle": "has_nonsingle"})
)

all_single_mols = mol_has_nonsingle.loc[~mol_has_nonsingle["has_nonsingle"], ["molecule_id"]]

# Join to carcinogenicity table and filter to non-carcinogenic sign == '-'
all_single_with_sign = all_single_mols.merge(
    carc.rename(columns={"code": "molecule_id"}),
    on="molecule_id",
    how="inner"
)

non_carc_all_single_count = all_single_with_sign.loc[
    all_single_with_sign["sign"].eq("-"), "molecule_id"
].nunique()

# Final answer table
answer_df = pd.DataFrame(
    {"non_carcinogenic_single_bond_molecules_count": [int(non_carc_all_single_count)]}
)

result = {"answer": answer_df}