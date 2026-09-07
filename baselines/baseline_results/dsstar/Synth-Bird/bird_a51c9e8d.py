import pandas as pd

# Tables already provided in-scope as `tables`
atom_df = tables["table_1"]
labels_df = tables["table_2"]

# Find molecules that contain chlorine atoms (element ends with "_cl")
chlorine_atoms = atom_df[atom_df["molecule_element"].str.endswith("_cl", na=False)].copy()
chlorine_atoms["molecule_id"] = chlorine_atoms["atom_id"].str.split("_", n=1).str[0]
molecules_with_chlorine = sorted(chlorine_atoms["molecule_id"].unique().tolist())

# From the "label" row, select those chlorine-containing molecules labeled carcinogenic ("+")
chlorine_label_series = labels_df.loc[labels_df["molecule_id"].eq("label"), molecules_with_chlorine].iloc[0]
carcinogenic_chlorine_molecules = sorted(chlorine_label_series[chlorine_label_series.eq("+")].index.tolist())

# Final answer table
answer_df = pd.DataFrame({"molecule_id": carcinogenic_chlorine_molecules})

result = {"carcinogenic_molecules_with_cl": answer_df}