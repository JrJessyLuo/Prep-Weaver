import pandas as pd

# tables['table_1'] -> bird_7bcd2ceb_input_0.pkl (atoms_df)
# tables['table_2'] -> bird_7bcd2ceb_input_1.pkl (labels_df)
atoms_df = tables["table_1"]
labels_df = tables["table_2"]

# Filter carcinogenic molecules
carc_df = labels_df.loc[labels_df["lb"] == "+", ["mid"]].dropna().drop_duplicates()

# Extract molecule id from atom_id prefix and keep only rows with Nitrogen present
atoms_n_df = atoms_df.loc[atoms_df["n"].notna(), ["atom_id"]].copy()
atoms_n_df["mid"] = atoms_n_df["atom_id"].astype(str).str.split("_").str[0]
atoms_n_df = atoms_n_df[["mid"]].dropna().drop_duplicates()

# Join and count distinct mids
merged = carc_df.merge(atoms_n_df, on="mid", how="inner")
count_carcinogenic_with_n = merged["mid"].nunique()

answer_df = pd.DataFrame({"count_carcinogenic_molecules_with_nitrogen": [count_carcinogenic_with_n]})

result = {"answer": answer_df}