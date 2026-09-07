import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Find race_id for "Vampire"
t1["value_norm"] = t1["value"].astype(str).str.strip().str.lower()
vampire_ids = pd.to_numeric(t1.loc[t1["value_norm"] == "vampire", "id"], errors="coerce").dropna().astype(int)
vampire_id_set = set(vampire_ids.tolist())

# Pivot hero key-value attributes to wide
t2["superhero_id"] = pd.to_numeric(t2["superhero_id"], errors="coerce")
wide = (
    t2.pivot_table(index="superhero_id", columns="id", values="value", aggfunc="first")
      .reset_index()
)

# Filter to vampire heroes and return full names
wide["race_id_num"] = pd.to_numeric(wide.get("race_id"), errors="coerce").astype("Int64")
out = wide.loc[wide["race_id_num"].isin(vampire_id_set), ["full_name"]].dropna().drop_duplicates().reset_index(drop=True)

result = {"vampire_hero_full_names": out}
