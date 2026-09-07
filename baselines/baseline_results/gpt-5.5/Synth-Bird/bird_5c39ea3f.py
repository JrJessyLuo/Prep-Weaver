import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Build TransactionID -> Currency mapping from table_1's column headers (excluding the descriptor column)
currency_cols = [c for c in t1.columns if c != "Currency"]
tx_currency = pd.DataFrame({
    "TransactionID": range(1, len(currency_cols) + 1),
    "Currency": currency_cols
})

# Filter transactions on date and morning time (hour < 12)
t2_f = t2.copy()
t2_f["Date"] = pd.to_datetime(t2_f["Date"], errors="coerce")
t2_f["Time_dt"] = pd.to_datetime(t2_f["Time"], format="%H:%M:%S", errors="coerce")

mask = (t2_f["Date"] == pd.Timestamp("2012-08-26")) & (t2_f["Time_dt"].dt.hour < 12)
t2_morning = t2_f.loc[mask, ["TransactionID"]]

# Join to currency and count CZK
cnt = (
    t2_morning.merge(tx_currency, on="TransactionID", how="left")
    .loc[lambda d: d["Currency"].eq("CZK")]
    .shape[0]
)

result = {
    "transactions_paid_CZK_morning_2012_08_26": pd.DataFrame({"count": [cnt]})
}
