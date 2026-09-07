import pandas as pd

# Source tables (already loaded in scope)
cards = tables["table_1"]
fmt = tables["table_2"]

# 2) Filter fmt to duel|Legal, then join to cards on uuid
fmt_duel_legal = fmt.loc[fmt["fs"].eq("duel|Legal")].copy()
fmt_duel_legal["uuid"] = fmt_duel_legal["uuid"].astype(str)

cards_join = cards.copy()
if "uuid" not in cards_join.columns:
    raise KeyError("Expected 'uuid' column in cards DataFrame for joining, but it was not found.")
cards_join["uuid"] = cards_join["uuid"].astype(str)

duel_legal_cards = cards_join.merge(
    fmt_duel_legal[["uuid", "fs", "id"]].rename(columns={"id": "fmt_id"}),
    on="uuid",
    how="inner",
    validate="m:m",
)

# 3) Group by name keeping max convertedManaCost, then top 10 by that max (desc), tie-break by name
top10 = (
    duel_legal_cards.loc[:, ["name", "convertedManaCost"]]
    .dropna(subset=["convertedManaCost"])
    .groupby("name", as_index=False, dropna=False)["convertedManaCost"]
    .max()
    .rename(columns={"convertedManaCost": "maxConvertedManaCost"})
    .sort_values(["maxConvertedManaCost", "name"], ascending=[False, True], kind="mergesort")
    .head(10)
    .reset_index(drop=True)
)

# Final answer as required
result = {"top10_duel_legal_by_max_convertedManaCost": top10}