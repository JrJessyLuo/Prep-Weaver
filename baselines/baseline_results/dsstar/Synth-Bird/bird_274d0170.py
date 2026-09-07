import pandas as pd

# -----------------------------
# Load single-bond molecule list (from tables)
# -----------------------------
bonds_df = tables["table_1"].copy()

# Extract molecule_id from combined_bond like: TR090_13_14_-  -> TR090
bonds_df["molecule_id"] = (
    bonds_df["combined_bond"].astype(str).str.extract(r"^(TR\d+)", expand=False)
)
single_bond_molecules = (
    pd.Series(bonds_df["molecule_id"].dropna().unique(), name="molecule_id").to_frame()
)

# -----------------------------
# Load labels dataset (from tables)
# -----------------------------
labels_full_df = tables["table_2"]

# Normalize columns (case-insensitive safety)
colmap = {c.lower(): c for c in labels_full_df.columns.astype(str)}
labels_df = labels_full_df.rename(
    columns={
        colmap.get("molecule_id", "molecule_id"): "molecule_id",
        colmap.get("label_type", "label_type"): "label_type",
        colmap.get("label_value", "label_value"): "label_value",
    }
).copy()

labels_df["label_type_norm"] = labels_df["label_type"].astype(str).str.strip().str.lower()
labels_df["label_value_norm"] = (
    labels_df["label_value"].astype(str).str.strip().str.lower()
)
labels_df["molecule_id"] = labels_df["molecule_id"].astype(str).str.strip()

# -----------------------------
# Identify carcinogenicity label_type(s)
# -----------------------------
keywords = ["carcin", "cancer", "tumor", "neoplasm"]
pattern = "|".join(keywords)

carc_label_types = (
    labels_df.loc[
        labels_df["label_type_norm"].str.contains(pattern, case=False, na=False),
        "label_type_norm",
    ]
    .dropna()
    .unique()
    .tolist()
)

# If none matched by keywords, fall back to any label_type containing 'carc' substring
if not carc_label_types:
    carc_label_types = (
        labels_df.loc[
            labels_df["label_type_norm"].str.contains("carc", case=False, na=False),
            "label_type_norm",
        ]
        .dropna()
        .unique()
        .tolist()
    )

# -----------------------------
# Join to single-bond molecules and filter to "not carcinogenic"
# -----------------------------
joined = single_bond_molecules.merge(labels_df, on="molecule_id", how="inner")

if carc_label_types:
    joined = joined[joined["label_type_norm"].isin(carc_label_types)]

not_carc_mask = (
    (joined["label_value_norm"] == "not carcinogenic")
    | (joined["label_value_norm"].str.contains(r"\bnot\s+carcinogenic\b", na=False))
    | (joined["label_value_norm"].str.contains(r"\bnon[-\s]?carcinogenic\b", na=False))
)

answer_df = (
    joined.loc[not_carc_mask, ["molecule_id"]]
    .dropna()
    .drop_duplicates()
    .sort_values("molecule_id")
    .reset_index(drop=True)
)

result = {"not_carcinogenic_single_bond_molecules": answer_df}