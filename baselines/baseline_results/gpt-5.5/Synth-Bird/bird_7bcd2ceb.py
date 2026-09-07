import pandas as pd

df_atoms = tables["table_1"]
df_labels = tables["table_2"]

# Carcinogenic molecules
carcinogenic = set(
    df_labels.loc[df_labels["lb"].astype(str).str.strip() == "+", "mid"]
    .dropna()
    .astype(str)
    .str.strip()
    .unique()
)

# Molecules that contain at least one Nitrogen atom
nitrogen_mols = set(
    df_atoms.loc[df_atoms["n"].notna(), "n"]
    .astype(str)
    .str.strip()
    .unique()
)

count_val = len(carcinogenic & nitrogen_mols)

result = {
    "carcinogenic_molecules_with_nitrogen_count": pd.DataFrame(
        {"count": [count_val]}
    )
}
