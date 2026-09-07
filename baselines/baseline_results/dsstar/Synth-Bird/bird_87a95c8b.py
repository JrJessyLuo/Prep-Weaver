import pandas as pd

# Input tables are already loaded in `tables`
stations = tables["table_1"]      # bird_87a95c8b_input_0.pkl
tx = tables["table_2"]            # bird_87a95c8b_input_1.pkl

target_date = pd.Timestamp("2012-08-25")

# 1) Get earliest transaction on 2012-08-25 and its GasStationID
tx_day = tx.loc[tx["Date"] == target_date].copy()
tx_day["Time"] = pd.to_datetime(
    tx_day["Time"].astype(str),
    format="%H:%M:%S",
    errors="coerce"
).dt.time

first_tx = tx_day.sort_values(["Time", "TransactionID"], ascending=[True, True]).head(1)
first_transaction_gasstationid = first_tx["GasStationID"].iloc[0] if len(first_tx) else None

# 2) Look up that station's country in station metadata
country = None
if first_transaction_gasstationid is not None:
    station_id_str = str(first_transaction_gasstationid)
    meta_rows = stations.loc[
        (stations["StationID"].astype(str) == station_id_str)
        & (stations["GasStationID"].astype(str) == "Country")
    ]
    if len(meta_rows):
        country = meta_rows["Value"].iloc[0]

answer_df = pd.DataFrame({"Country": [country]})

result = {"first_paid_customer_country_2012_08_25": answer_df}