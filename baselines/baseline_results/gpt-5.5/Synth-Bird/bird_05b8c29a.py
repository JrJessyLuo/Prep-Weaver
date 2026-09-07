import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Find the (Ravnica block, 180 cards) set code
set_code = (
    t1.loc[(t1["block"] == "Ravnica") & (t1["baseSetSize"] == 180), "code"]
    .dropna()
    .astype(str)
    .iloc[0]
)

# Parse language_setCode into separate columns
lang_split = t2["language_setCode"].astype(str).str.split("|", n=1, expand=True)
t2_parsed = t2.assign(language=lang_split[0], setCode=lang_split[1])

# Get the language(s) this set is translated into
out = (
    t2_parsed.loc[t2_parsed["setCode"] == set_code, ["language"]]
    .dropna()
    .drop_duplicates()
    .sort_values("language")
    .reset_index(drop=True)
)

result = {"set_translation_languages": out}
