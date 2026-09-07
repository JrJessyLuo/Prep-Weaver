import pandas as pd
import re

# Tables are already loaded in a dict named `tables`
hero_df = tables["table_1"]
hero_power_df = tables["table_2"]

# 1) Transpose so each hero becomes one row
t = hero_df.set_index("id").T.reset_index().rename(columns={"index": "hero_key"})

# 2) Locate the row for hero named "Amazo"
name_col_candidates = [
    c for c in t.columns
    if re.search(r"(superhero.*name|hero.*name|character.*name|name)$", str(c).lower())
]

amazo_rows = pd.DataFrame()
for c in name_col_candidates:
    m = t[c].astype(str).str.contains(r"\bAmazo\b", case=False, na=False)
    if m.any():
        amazo_rows = t[m].copy()
        break

# Fallback: scan all columns if name-like columns didn't work
if amazo_rows.empty:
    mask = t.astype(str).apply(lambda col: col.str.contains(r"\bAmazo\b", case=False, na=False))
    amazo_rows = t[mask.any(axis=1)].copy()

if amazo_rows.empty:
    raise ValueError("Could not find 'Amazo' after transposing the hero table.")

# 3) Re-extract Amazo's TRUE hero_id from hero_key/index
amazo_row = amazo_rows.iloc[0].copy()
raw_hero_key = amazo_row["hero_key"]

amazo_hero_id = int(float(str(raw_hero_key).strip()))

# 4) Count hero_power entries where left side (before '-') equals Amazo hero_id
if "hero_power" not in hero_power_df.columns:
    raise ValueError("Expected column 'hero_power' not found in hero_power_df.")

hp = hero_power_df["hero_power"].astype(str)
left_id = pd.to_numeric(hp.str.split("-", n=1, expand=True)[0], errors="coerce").astype("Int64")
amazo_power_count = int((left_id == amazo_hero_id).sum())

answer_df = pd.DataFrame({"powers_count": [amazo_power_count]})
result = {"amazo_powers_count": answer_df}