import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Extract bond type (part after '|')
t2["bond_type"] = t2["bond_id_type"].astype(str).str.split("|").str[-1]

# Molecules whose all recorded bonds are single ('-')
single_bond_molecules = (
    t2.groupby("molecule_id")["bond_type"]
      .apply(lambda s: (s.dropna().nunique() == 1) and (s.dropna().iloc[0] == "-") if len(s.dropna()) > 0 else False)
)
single_bond_molecules = single_bond_molecules[single_bond_molecules].index

# Count atoms/elements (rows in table_1) for those molecules
num_elements = t1[t1["fz_id"].isin(single_bond_molecules)].shape[0]

result = {
    "single_bond_molecules_element_count": pd.DataFrame({"num_elements": [num_elements]})
}
