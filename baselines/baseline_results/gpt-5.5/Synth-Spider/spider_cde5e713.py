import pandas as pd

sailors = tables["table_1"]
boats_wide = tables["table_2"]
res = tables["table_3"]

# Unpivot boats table to get (bid, boat_name)
boats_long = (
    boats_wide.melt(id_vars=["bid"], var_name="boat_name", value_name="attr")
    .dropna(subset=["attr"])
    .loc[:, ["bid", "boat_name"]]
    .drop_duplicates()
)

# Sailors aged 20-30 (inclusive)
sailors_20_30 = sailors[sailors["age"].between(20, 30)][["sid"]]

# Join reservations -> sailors -> boats, then select boat names
out = (
    res.merge(sailors_20_30, left_on="xh", right_on="sid", how="inner")
      .merge(boats_long, left_on="bh", right_on="bid", how="inner")
      .loc[:, ["boat_name"]]
      .drop_duplicates()
      .sort_values("boat_name")
      .reset_index(drop=True)
)

result = {"boats_booked_by_age_20_30": out}
