import pandas as pd

# The input tables are provided in `tables`
# tables['table_1'] -> customers
# tables['table_2'] -> receipts

df_customers = tables['table_1'].copy()
df_receipts = tables['table_2'].copy()

# Parse receipts’ Date column into datetime for accurate sorting
df_receipts["Date"] = pd.to_datetime(df_receipts["Date"], format="%d-%b-%Y", errors="coerce")

# Find the minimum date and the receipts on that date
min_date = df_receipts["Date"].min()
receipts_min_date = df_receipts[df_receipts["Date"] == min_date].copy()

# Get unique CustomerId(s) for that min date
customer_ids_min_date = receipts_min_date["CustomerId"].dropna().unique()

# Prepare customers for matching (coerce Id to numeric)
df_customers_coerced = df_customers.copy()
df_customers_coerced["Id_num"] = pd.to_numeric(df_customers_coerced["Id"], errors="coerce")

# Match customers by ID
matched_customers = df_customers_coerced[df_customers_coerced["Id_num"].isin(customer_ids_min_date)]

# Select only required columns and rename for clarity
answer_df = matched_customers[["ming", "xing"]].rename(columns={"ming": "FirstName", "xing": "LastName"}).reset_index(drop=True)

# Final result mapping
result = {"earliest_customer_name": answer_df}