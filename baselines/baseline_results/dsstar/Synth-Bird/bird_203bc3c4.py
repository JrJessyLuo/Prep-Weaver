import pandas as pd

# Transactions table (reference code loads bird_203bc3c4_input_1.pkl)
tx = tables["table_2"]

# Normalize Date to YYYY-MM-DD (handle mixed formats like '2012-08-24' and '2012 / 08 / 24')
date_norm = pd.to_datetime(
    tx["Date"].astype(str).str.replace("/", "-", regex=False).str.replace(" ", "", regex=False),
    errors="coerce"
).dt.date

# Normalize Time to HH:MM:SS
time_norm = pd.to_datetime(tx["Time"].astype(str), format="%H:%M:%S", errors="coerce").dt.time

# Filter for Date = 2012-08-24 and Time = 12:42:00
target_date = pd.to_datetime("2012-08-24").date()
target_time = pd.to_datetime("12:42:00").time()

filtered_tx = tx.loc[(date_norm == target_date) & (time_norm == target_time)].copy()

# Get GasStationID(s) for the deal(s)
gas_station_ids = sorted(filtered_tx["GasStationID"].dropna().unique().tolist())

# Gas stations table (bird_203bc3c4_input_0.pkl)
gas = tables["table_1"]

# Find the country for the matching GasStationID(s)
answer_df = (
    gas.loc[gas["GasStationID"].isin(gas_station_ids), ["Country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"answer": answer_df}