import pandas as pd

# Source table (already loaded in `tables`)
df = tables["table_2"]

# --- Parse set_code and set_name from set_info ---
split = df["set_info"].astype("string").str.split("|", n=1, expand=True)

df_parsed = df.copy()
df_parsed["set_code"] = split[0].astype("string").str.strip()
df_parsed["set_name"] = split[1] if split.shape[1] > 1 else pd.NA
df_parsed["set_name"] = df_parsed["set_name"].astype("string").str.strip()

# Normalize missing/empty set_name to NA
mask_missing = (
    df_parsed["set_name"].isna()
    | (df_parsed["set_name"] == "")
    | (df_parsed["set_name"].str.lower() == "nan")
)
df_parsed.loc[mask_missing, "set_name"] = pd.NA

# Keep only rows relevant to the plan
sub = df_parsed[df_parsed["language"].isin(["Japanese", "Korean"])].copy()

# --- Group by set_code and flag missing/present for Japanese/Korean set_name ---
def _has_non_na_set_name(g: pd.DataFrame) -> bool:
    return bool(g["set_name"].notna().any())

flags = (
    sub.groupby(["set_code", "language"], dropna=False)
       .apply(_has_non_na_set_name)
       .rename("has_set_name")
       .reset_index()
)

flags_wide = (
    flags.pivot(index="set_code", columns="language", values="has_set_name")
         .fillna(False)
)

# Sets where Japanese is missing but Korean is present
target_sets = flags_wide[
    (flags_wide.get("Japanese", False) == False) & (flags_wide.get("Korean", False) == True)
].index

# --- Output corresponding set names from Korean rows for those sets ---
korean_names = (
    sub[(sub["language"] == "Korean") &
        (sub["set_code"].isin(target_sets)) &
        (sub["set_name"].notna())]
    [["set_code", "set_name"]]
    .drop_duplicates()
    .sort_values(["set_code", "set_name"])
    .reset_index(drop=True)
)

# Final answer DataFrame: list the set names (Korean) for sets missing Japanese translation
answer = korean_names[["set_name"]].drop_duplicates().sort_values("set_name").reset_index(drop=True)

result = {"sets_missing_japanese_but_have_korean_translation": answer}