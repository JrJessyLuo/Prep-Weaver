import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Client names from key-value table
clients = (
    t1[t1["attribute"].eq("Name")]
    .assign(IdClient=lambda d: pd.to_numeric(d["IdClient"], errors="coerce"))
    .dropna(subset=["IdClient"])
    .assign(IdClient=lambda d: d["IdClient"].astype(int))
    .rename(columns={"details": "client_name"})[["IdClient", "client_name"]]
    .drop_duplicates(subset=["IdClient"])
)

# Normalize order IDs and client IDs
orders = t2.assign(
    IdOrder=t2["IdOrder"].astype(str).str.strip(),
    IdClient=pd.to_numeric(t2["IdClient"].astype(str).str.replace('"', "", regex=False).str.strip(), errors="coerce"),
).dropna(subset=["IdClient"])
orders["IdClient"] = orders["IdClient"].astype(int)

# Build order id in order lines to match table_2 IdOrder
lines = t3.assign(
    IdOrder=(t3["IdOrder_num"].astype(str).str.strip() + t3["IdOrder_suffix"].astype(str).str.strip()),
    amount=pd.to_numeric(t3["amount"], errors="coerce").fillna(0),
)

# Sum amounts by client
totals = (
    lines.merge(orders[["IdOrder", "IdClient"]], on="IdOrder", how="inner")
    .groupby("IdClient", as_index=False)["amount"]
    .sum()
    .rename(columns={"amount": "total_books_ordered"})
)

out = (
    clients.merge(totals, on="IdClient", how="inner")[["client_name", "total_books_ordered"]]
    .sort_values(["total_books_ordered", "client_name"], ascending=[False, True])
    .reset_index(drop=True)
)

result = {"client_total_books_ordered": out}
