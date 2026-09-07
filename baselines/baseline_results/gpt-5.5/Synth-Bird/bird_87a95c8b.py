import pandas as pd

# Tables
t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Pivot station key-value table to wide (one row per station)
stations = (
    t1.pivot_table(index="StationID", columns="GasStationID", values="Value", aggfunc="first")
      .reset_index()
)

# Find a likely "Country" column in the station attributes
country_col = next((c for c in stations.columns if c != "StationID" and "country" in str(c).lower()), None)

# Filter to date 2012-08-25 and get earliest transaction time
target_date = pd.Timestamp("2012-08-25")
tx = t2.loc[t2["Date"].dt.normalize() == target_date].copy()

# Build sortable datetime
tx["DateTime"] = pd.to_datetime(tx["Date"].dt.strftime("%Y-%m-%d") + " " + tx["Time"].astype(str), errors="coerce")

first_tx = (
    tx.sort_values(["DateTime", "TransactionID"], ascending=[True, True])
      .head(1)
)

# Join to station attributes to get country
first_with_station = first_tx.merge(
    stations,
    left_on="GasStationID",
    right_on="StationID",
    how="left"
)

if country_col is None:
    out = pd.DataFrame({"Country": [pd.NA]})
else:
    out = first_with_station[[country_col]].rename(columns={country_col: "Country"}).reset_index(drop=True)

result = {"first_paid_customer_country": out}
