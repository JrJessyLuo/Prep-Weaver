import pandas as pd

# The input tables are provided in the `tables` dict.
# Map to variables for clarity based on the given names.
clients = tables['table_3']
packages = tables['table_5']

# Reproduce the SAME logic as the reference code, but sourcing from `tables`.

# DataFrame overview (computed but not printed per guidelines)
summary = {
    "shape": packages.shape,
    "columns": list(packages.columns),
    "dtypes": packages.dtypes.astype(str).to_dict(),
    "head": packages.head(10).to_dict(orient="records"),
}
id_analysis = {
    "Shipment_unique_count": packages["Shipment"].nunique(),
    "PackageNumber_per_Shipment_counts": packages.groupby("Shipment")["PackageNumber"].nunique().to_dict(),
    "Sender_unique_ids": sorted(packages["Sender"].unique().tolist()),
    "Recipient_unique_ids": sorted(packages["Recipient"].unique().tolist()),
}
ownership_column = "Sender"
id_namespace = "AccountNumber"

# Client lookup for "Phillip J. Fry"
clients = clients.copy()
clients["_Name_norm"] = clients["Name"].astype(str).str.strip()
target_name = "Phillip J. Fry"

exact_match = clients.loc[clients["_Name_norm"] == target_name, ["AccountNumber", "Name"]]

account_number_for_fry = None
if not exact_match.empty and exact_match.shape[0] == 1:
    account_number_for_fry = int(exact_match.iloc[0]["AccountNumber"])

# Determine shipments under Phillip J. Fry's management:
# Following the conclusion from reference code, ownership_column = "Sender" and id_namespace = "AccountNumber".
# If account number is not found (None), the result should be an empty set.
if account_number_for_fry is not None:
    shipment_ids = (
        packages.loc[packages[ownership_column] == account_number_for_fry, ["Shipment"]]
        .drop_duplicates()
        .sort_values(by="Shipment")
        .reset_index(drop=True)
    )
else:
    shipment_ids = packages.loc[[] , ["Shipment"]].copy()  # empty DataFrame with correct column

# Package the final answer as required
result = {
    "shipments_under_phillip_j_fry": shipment_ids
}