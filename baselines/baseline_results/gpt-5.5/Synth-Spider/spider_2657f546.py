import pandas as pd

customers = tables["table_1"].copy()
receipts = tables["table_2"].copy()

# Normalize customer Id to int for joining
customers["CustomerId"] = (
    customers["Id"].astype(str).str.strip().str.replace('"', '', regex=False).astype(int)
)

# Parse dates and find earliest visit
receipts["Date_dt"] = pd.to_datetime(receipts["Date"], format="%d-%b-%Y", errors="coerce")
earliest = receipts.sort_values(["Date_dt", "ReceiptNumber"], ascending=[True, True]).head(1)

# Join to get customer name (ming = first name, xing = last name)
out = (
    earliest.merge(customers, on="CustomerId", how="left")
    .rename(columns={"ming": "first_name", "xing": "last_name"})
    [["first_name", "last_name"]]
    .reset_index(drop=True)
)

result = {"earliest_visit_customer": out}
