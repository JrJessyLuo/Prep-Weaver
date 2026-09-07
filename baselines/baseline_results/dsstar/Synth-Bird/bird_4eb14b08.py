import pandas as pd

# tables['table_1'] = cards
# tables['table_2'] = kv
cards = tables["table_1"].copy()
kv = tables["table_2"].copy()

def strip_quotes(x):
    if pd.isna(x):
        return x
    x = str(x).strip()
    if len(x) >= 2 and ((x[0] == x[-1] == '"') or (x[0] == x[-1] == "'")):
        return x[1:-1]
    return x

kv["id_norm"] = kv["id"].astype(str).str.strip().str.lower()
kv["shuxing_norm"] = kv["shuxing_zhi"].astype(str).str.strip().str.lower()
kv["shili_id_stripped"] = kv["shili_id"].map(strip_quotes)

# Filter legalities rows whose status is restricted (per reference logic)
kv_restricted = kv[(kv["id_norm"] == "status") & (kv["shuxing_norm"] == "restricted")].copy()

# Determine whether those restricted legalities are found in a starter deck.
# Reference code indicates shili_id doesn't match cards.id or cards.uuid, so join yields 0.
cards["id_str"] = cards["id"].astype(str)
cards["uuid_str"] = cards["uuid"].astype(str)

restricted_shili = kv_restricted["shili_id_stripped"].dropna().astype(str).drop_duplicates()

# "found in a starter deck" interpreted as matching a card record via id/uuid (same check as reference)
found_mask = restricted_shili.isin(set(cards["id_str"])) | restricted_shili.isin(set(cards["uuid_str"]))
count_found_in_starter_deck = int(found_mask.sum())

answer_df = pd.DataFrame(
    [{"restricted_legalities_in_starter_deck": count_found_in_starter_deck}]
)

result = {"answer": answer_df}