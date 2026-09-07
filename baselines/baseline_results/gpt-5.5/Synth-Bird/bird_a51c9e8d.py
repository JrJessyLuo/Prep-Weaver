import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# --- molecules that contain "cl" element ---
me_parts = t1["molecule_element"].astype(str).str.rsplit("_", n=1, expand=True)
t1["molecule_id"] = me_parts[0]
t1["element"] = me_parts[1].str.lower()

cl_molecules = (
    t1.loc[t1["element"].eq("cl"), "molecule_id"]
      .dropna()
      .unique()
      .tolist()
)

# --- carcinogenic labels from table_2 (stored as a wide single 'label' row) ---
label_row = t2.loc[t2["molecule_id"].astype(str).str.lower().eq("label")].head(1)
labels_long = label_row.melt(
    id_vars=["molecule_id"],
    var_name="molecule_id",
    value_name="carcinogenic"
).drop(columns=["molecule_id"])

out = (
    labels_long[
        labels_long["molecule_id"].isin(cl_molecules)
        & labels_long["carcinogenic"].astype(str).str.strip().eq("+")
    ][["molecule_id", "carcinogenic"]]
    .drop_duplicates()
    .sort_values("molecule_id")
    .reset_index(drop=True)
)

result = {"carcinogenic_cl_molecules": out}
