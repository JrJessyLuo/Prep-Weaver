import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

tx = t2.copy()

# Parse date/time
tx["Date"] = pd.to_datetime(tx["Date"], errors="coerce")
tx["Time"] = pd.to_datetime(tx["Time"], format="%H:%M:%S", errors="coerce").dt.time

# Filter: 2012-08-26, 08:00-09:00
start_t = pd.to_datetime("08:00:00").time()
end_t = pd.to_datetime("09:00:00").time()

tx_filt = tx[
    (tx["Date"] == pd.Timestamp("2012-08-26")) &
    (tx["Time"] >= start_t) &
    (tx["Time"] < end_t)
]

# Join to gas stations and keep those in CZE (non-null CZE)
tx_joined = tx_filt.merge(t1[["GasStationID", "CZE"]], on="GasStationID", how="left")
count_cze = tx_joined["CZE"].notna().sum()

result = {
    "transactions_2012_08_26_08_00_09_00_in_CZE": pd.DataFrame(
        {"transactions_in_CZE": [count_cze]}
    )
}
