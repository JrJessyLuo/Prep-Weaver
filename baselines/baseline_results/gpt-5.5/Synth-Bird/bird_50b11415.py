import pandas as pd

cards = tables["table_1"]
formats = tables["table_2"]

duel_legal_uuids = formats.loc[
    formats["fs"].astype(str).str.lower().eq("duel|legal"), "uuid"
].dropna().unique()

duel_cards = cards.loc[cards["uuid"].isin(duel_legal_uuids)].copy()
duel_cards["convertedManaCost"] = pd.to_numeric(duel_cards["convertedManaCost"], errors="coerce")

top10 = (
    duel_cards.dropna(subset=["name", "convertedManaCost"])
    .groupby("name", as_index=False)["convertedManaCost"].max()
    .sort_values(["convertedManaCost", "name"], ascending=[False, True])
    .head(10)
    .reset_index(drop=True)
)

result = {"top_10_duel_cards_by_converted_mana_cost": top10}
