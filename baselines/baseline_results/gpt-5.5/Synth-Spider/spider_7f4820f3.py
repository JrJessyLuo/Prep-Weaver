import pandas as pd

boats = tables["table_1"].copy()
res = tables["table_2"].copy()

# Normalize boat colors and filter to red/blue
boats["clr_norm"] = boats["clr"].astype(str).str.lower().str.replace(r"[^a-z]", "", regex=True)
boats_rb = boats[boats["clr_norm"].isin(["red", "blue"])][["b"]].drop_duplicates()

# Extract reserved boat ids from packed "date_value_pairs"
res_long = (
    res.assign(
        b=res["date_value_pairs"]
        .astype(str)
        .str.findall(r":\s*([0-9]+(?:\.[0-9]+)?)")
    )
    .explode("b", ignore_index=True)
)
res_long["b"] = pd.to_numeric(res_long["b"], errors="coerce").dropna().astype(int)

# SIDs who reserved red or blue boats
out = (
    res_long.merge(boats_rb, on="b", how="inner")[["sid"]]
    .drop_duplicates()
    .sort_values("sid")
    .reset_index(drop=True)
)

result = {"sids": out}
