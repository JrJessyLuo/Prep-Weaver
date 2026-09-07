import re
import numpy as np
import pandas as pd

# Tables already loaded in scope as `tables`
currency_wide = tables["table_1"]
transactions = tables["table_2"]

cw = currency_wide.copy()

if len(cw) != 1:
    raise ValueError(f"Expected currency_wide to have 1 row, got {len(cw)}")

# Wide -> long by position (since duplicate column names exist)
headers = [str(c) for c in cw.columns[1:]]
values = cw.iloc[0, 1:].tolist()

cw_long = pd.DataFrame(
    {
        "pos": np.arange(1, len(headers) + 1, dtype=int),
        "Currency": headers,
        "raw_value": values,
    }
)

def extract_customer_id(x):
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    left = s.split("-", 1)[0].strip()
    m = re.search(r"\d+", left)
    return float(m.group(0)) if m else np.nan

cw_long["CustomerID"] = cw_long["raw_value"].apply(extract_customer_id)

currency_map = (
    cw_long.dropna(subset=["CustomerID"])
    .assign(CustomerID=lambda d: d["CustomerID"].astype(int))
    .loc[:, ["CustomerID", "Currency"]]
    .drop_duplicates(subset=["CustomerID"], keep="first")
    .reset_index(drop=True)
)

tx = transactions.merge(currency_map, on="CustomerID", how="left")

filtered = tx[
    (tx["Date"] == "2012-08-26")
    & (tx["Time"] < "12:00:00")
    & (tx["Currency"] == "CZK")
]

answer_df = pd.DataFrame({"count": [int(len(filtered))]})
result = {"czk_morning_transactions_2012_08_26": answer_df}