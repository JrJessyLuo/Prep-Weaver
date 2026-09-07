import pandas as pd

sailors = tables["table_1"]
reservations = tables["table_2"]

# Extract sid from packed "sid_bid" (e.g., "1_102")
res_sids = (
    reservations["sid_bid"]
    .astype(str)
    .str.split("_", n=1, expand=True)[0]
)
res_sids = pd.to_numeric(res_sids, errors="coerce").dropna().astype("int64").unique()

out = (
    sailors.loc[~sailors["sid"].isin(res_sids), ["sid"]]
    .drop_duplicates()
    .sort_values("sid")
    .reset_index(drop=True)
)

result = {"sailors_without_reservations": out}
