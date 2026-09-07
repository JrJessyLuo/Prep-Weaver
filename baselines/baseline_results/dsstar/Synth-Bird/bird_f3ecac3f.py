import pandas as pd

# Source tables from the provided `tables` dict
customers = tables["table_1"]      # bird_f3ecac3f_input_0.pkl
products = tables["table_2"]       # bird_f3ecac3f_input_1.pkl
transactions = tables["table_3"]   # bird_f3ecac3f_input_2.pkl

# Join on CustomerID and filter to EUR customers
transactions_eur = (
    transactions.merge(customers[["CustomerID", "huobi"]], on="CustomerID", how="inner")
    .query('huobi == "EUR"')
    .drop(columns=["huobi"])
    .reset_index(drop=True)
)

# Normalize ProductID types in both tables (string + strip whitespace + remove quotes)
transactions_eur = transactions_eur.assign(
    ProductID=transactions_eur["ProductID"].astype(str).str.strip().str.strip('"').str.strip("'")
)
products_clean = products.assign(
    ProductID=products["ProductID"].astype(str).str.strip().str.strip('"').str.strip("'")
)

# Join and output distinct product descriptions for EUR transactions
eur_product_descriptions = (
    transactions_eur.merge(products_clean[["ProductID", "Description"]], on="ProductID", how="left")
    .loc[:, ["Description"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Final answer
result = {"eur_product_descriptions": eur_product_descriptions}