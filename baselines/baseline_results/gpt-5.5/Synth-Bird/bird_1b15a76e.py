import pandas as pd

cards = tables["table_1"].copy()
rulings = tables["table_2"].copy()

# Parse ruling dates
rulings["rq_dt"] = pd.to_datetime(rulings["rq"], errors="coerce")

# Target date is ambiguous (01/02/2007); match both interpretations
target_dates = {
    pd.to_datetime("2007-02-01", errors="coerce"),  # mm/dd/yyyy
    pd.to_datetime("2007-01-02", errors="coerce"),  # dd/mm/yyyy
}

# Filter rulings with non-null ruling text on the target date
rulings_f = rulings[
    rulings["rq_dt"].isin(target_dates) & rulings["nr"].notna() & rulings["uuid"].notna()
]

# Join to cards and require print rarity present
m = rulings_f.merge(cards[["uuid", "rarity"]], on="uuid", how="inner")
m = m[m["rarity"].notna()]

count_cards = m["uuid"].nunique()

result = {
    "cards_with_rarity_and_ruling_text_on_2007_01_02_or_2007_02_01": pd.DataFrame(
        {"count": [count_cards]}
    )
}
