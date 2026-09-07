import pandas as pd
import re

# tables are preloaded in scope:
# tables['table_3'] == card_games_foreign_data.pkl
foreign_df = tables["table_3"]

target = "Angel of Mercy"

def norm(s: str) -> str:
    if s is None or (isinstance(s, float) and pd.isna(s)):
        return ""
    s = str(s).lower().strip()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

target_norm = norm(target)

name_norm = foreign_df["name"].map(norm)
mask_exact_norm = name_norm == target_norm
mask_contains = name_norm.str.contains(re.escape(target_norm), na=False)

matched_foreign = foreign_df.loc[mask_exact_norm | mask_contains, ["language", "name"]].copy()

# "How many translations are there" -> count distinct translation languages among matches
translations_count = int(matched_foreign["language"].nunique(dropna=True)) if not matched_foreign.empty else 0

answer_df = pd.DataFrame({"translations_count": [translations_count]})
result = {"answer": answer_df}