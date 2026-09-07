import pandas as pd

cards = tables["table_1"].copy()
leg = tables["table_2"].copy()

# Filter to Commander + Legal
leg["fmt_norm"] = leg["fmt"].astype(str).str.strip().str.lower()
leg["sts_norm"] = leg["sts"].astype(str).str.strip().str.lower()
comm_legal = leg[(leg["fmt_norm"] == "commander") & (leg["sts_norm"] == "legal")][["uuid"]].dropna().drop_duplicates()

# Join to cards to get content warning flag
merged = comm_legal.merge(cards[["uuid", "hasContentWarning"]], on="uuid", how="inner")
merged["hasContentWarning"] = merged["hasContentWarning"].fillna(0).astype(int)

den = merged["uuid"].nunique()
num = merged.loc[merged["hasContentWarning"] == 0, "uuid"].nunique()
pct = (num / den * 100) if den else 0.0

result = {
    "commander_legal_no_content_warning_percentage": pd.DataFrame(
        {"percentage": [pct]}
    )
}
