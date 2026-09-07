import pandas as pd

# Load DataFrames from provided 'tables' dict
df_services = tables['table_1']      # Service_ID, Service_Type, Details
df_customers = tables['table_2']     # kehu_id, kehu_xinxi
df_cust_services = tables['table_3'] # Customer_ID, Service_ID, Attribute, Value
df_interactions = tables['table_4']  # Customer_Interaction_ID, Channel_ID, Customer_ID, Service_ID, zhuangtai, xiangxi

# Prepare customers DataFrame with consistent column names
df_customers_renamed = df_customers.rename(columns={"kehu_id": "Customer_ID", "kehu_xinxi": "Customer_Name"})

# Find Customer_ID for "Hardy Kutch"
hardy_row = df_customers_renamed[df_customers_renamed["Customer_Name"] == "Hardy Kutch"]

if hardy_row.empty:
    # If customer not found, result is an empty DataFrame with expected columns
    final_df = df_services.head(0)[["Service_ID", "Service_Type", "Details"]].copy()
else:
    hardy_id = int(hardy_row.iloc[0]["Customer_ID"])

    # From interactions: Service_IDs where xiangxi == "good" OR Customer_ID == Hardy's ID
    services_from_interactions = df_interactions.loc[
        (df_interactions["xiangxi"] == "good") | (df_interactions["Customer_ID"] == hardy_id),
        ["Service_ID"]
    ].dropna().drop_duplicates()

    # From customer-service attributes: Service_IDs where Customer_ID == Hardy's ID
    services_from_attrs = df_cust_services.loc[
        df_cust_services["Customer_ID"] == hardy_id, ["Service_ID"]
    ].dropna().drop_duplicates()

    # Union and deduplicate Service_IDs
    all_service_ids = pd.concat([services_from_interactions, services_from_attrs], ignore_index=True).drop_duplicates()

    if all_service_ids.empty:
        final_df = df_services.head(0)[["Service_ID", "Service_Type", "Details"]].copy()
    else:
        # Join to services to return Service_Type and Details
        final_df = (
            all_service_ids.merge(df_services, on="Service_ID", how="left")
            .drop_duplicates()
            .sort_values(by="Service_ID")
            .reset_index(drop=True)
        )[["Service_ID", "Service_Type", "Details"]]

# Assign to result as required
result = {"services_for_hardy_or_good": final_df}