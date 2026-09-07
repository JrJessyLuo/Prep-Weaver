import pandas as pd

cards = tables["table_1"]
leg = tables["table_2"]

# Future frame cards (by printing uuid)
future_mask = cards["frameVersion"].astype(str).str.lower().eq("future")
future_cards = cards.loc[future_mask, ["uuid"]].dropna().drop_duplicates()

total_future_cards = future_cards["uuid"].nunique()

# Join to legality and summarize legality status
future_leg = future_cards.merge(leg[["uuid", "format", "status"]], on="uuid", how="left")
future_leg["format"] = future_leg["format"].fillna("Unknown")
future_leg["status"] = future_leg["status"].fillna("Unknown")

out = (
    future_leg.groupby(["format", "status"], as_index=False)
    .agg(card_count=("uuid", "nunique"))
    .sort_values(["format", "status"])
)

out.insert(0, "total_future_frame_cards", total_future_cards)

result = {"future_frame_cards_legality_status": out.reset_index(drop=True)}
