import pandas as pd

# --- Single-bond molecule ids from table_1 ---
t1 = tables["table_1"].copy()
single_bond_mols = (
    t1["combined_bond"]
    .astype(str)
    .str.split("_", n=1, expand=True)[0]
    .dropna()
    .unique()
)
single_bond_mols = pd.Index(single_bond_mols)

# --- Parse carcinogenic labels from denormalized table_2 ---
t2 = tables["table_2"].copy()
t2 = t2[t2["label_type"].astype(str).str.lower().eq("label")]

parts = []
for _, r in t2.iterrows():
    mols = [x.strip() for x in str(r["molecule_id"]).split(",") if x.strip() != ""]
    labs = [x.strip() for x in str(r["label_value"]).split(",") if x.strip() != ""]
    n = min(len(mols), len(labs))
    parts.append(pd.DataFrame({"molecule_id": mols[:n], "label": labs[:n]}))

labels_long = pd.concat(parts, ignore_index=True).drop_duplicates()

# Not carcinogenic assumed to be label "-"
not_carcinogenic = (
    labels_long[
        labels_long["molecule_id"].isin(single_bond_mols) &
        labels_long["label"].eq("-")
    ][["molecule_id"]]
    .drop_duplicates()
    .sort_values("molecule_id")
    .reset_index(drop=True)
)

result = {"not_carcinogenic_single_bond_molecules": not_carcinogenic}
