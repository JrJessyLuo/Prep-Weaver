import pandas as pd

# Tables already loaded in scope as `tables`
gas_df = tables["table_1"]          # bird_52f00eb1_input_0.pkl
df = tables["table_2"]              # bird_52f00eb1_input_1.pkl

# Filter by Date and Time window: [08:00:00, 09:00:00)
time_parsed = pd.to_datetime(df["Time"], format="%H:%M:%S", errors="coerce").dt.time
mask = (
    (df["Date"] == "2012-08-26")
    & (time_parsed >= pd.to_datetime("08:00:00").time())
    & (time_parsed < pd.to_datetime("09:00:00").time())
)
filtered_df = df.loc[mask].copy()

# Join on GasStationID
joined = filtered_df.merge(gas_df, on="GasStationID", how="inner")

# Filter to rows with non-null CZE (and SVK null) and count them
filtered_joined = joined.loc[joined["CZE"].notna() & joined["SVK"].isna()].copy()
count_filtered = len(filtered_joined)

# Final answer as a DataFrame and pack into `result`
answer_df = pd.DataFrame({"count_transactions_in_CZE": [count_filtered]})
result = {"answer": answer_df}