import pandas as pd

cards = tables["table_1"]
set_trans = tables["table_2"]
sets = tables["table_6"]

target_set_name = "Hauptset Zehnte Edition"

# Try to find set code(s) via localization table (German set name -> set code)
set_codes = set_trans.loc[
    (set_trans["language"].astype(str).str.strip().str.casefold() == "german")
    & (set_trans["fy"].astype(str).str.strip() == target_set_name),
    "jhm",
].dropna().astype(str).str.strip().unique().tolist()

# Fallback: use known English set name "Tenth Edition" from sets table
if len(set_codes) == 0:
    set_codes = sets.loc[
        sets["name"].astype(str).str.strip().str.casefold() == "tenth edition",
        "code",
    ].dropna().astype(str).str.strip().unique().tolist()

mask = (
    cards["setCode"].astype(str).str.strip().isin(set_codes)
    & (cards["artist"].astype(str).str.strip().str.casefold() == "adam rex")
)

count_adam_rex = int(mask.sum())

result = {
    "adam_rex_cards_in_hauptset_zehnte_edition": pd.DataFrame(
        {"count": [count_adam_rex]}
    )
}
