import pandas as pd

# --- Sets table (table_1) is stored as attributes in rows, set entries in columns ---
t1 = tables["table_1"].copy()

sets_wide = (
    t1.set_index("id")
      .T
      .rename_axis(None)
      .reset_index(drop=True)
)

# Keep just what we need
sets = sets_wide.rename(columns={"code": "setCode", "name": "setName"})[["setCode", "setName"]].copy()
sets["setCode"] = sets["setCode"].astype(str)

# --- Translations table (table_2): set_info is like "ALA|阿拉若斷片" ---
t2 = tables["table_2"].copy()
t2[["setCode", "translatedName"]] = t2["set_info"].astype(str).str.split("|", n=1, expand=True)
t2["setCode"] = t2["setCode"].astype(str)

langs_by_set = t2.groupby("setCode")["language"].apply(lambda s: set(s.dropna())).reset_index(name="languages")

target_codes = langs_by_set.loc[
    langs_by_set["languages"].apply(lambda x: ("Korean" in x) and ("Japanese" not in x)),
    "setCode"
]

out = (
    sets[sets["setCode"].isin(target_codes)]
    .dropna(subset=["setName"])
    .drop_duplicates(subset=["setName"])
    .sort_values("setName")
    .reset_index(drop=True)[["setName"]]
)

result = {"sets_without_japanese_with_korean": out}
