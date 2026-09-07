import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Unpivot invoice status/detail columns into (status_code, status_details)
status_cols = [c for c in t3.columns if c.startswith("invoice_details_")]
inv_status = (
    t3.melt(
        id_vars=["invoice_id", "client_id"],
        value_vars=status_cols,
        var_name="invoice_status_code",
        value_name="invoice_status_details",
    )
    .dropna(subset=["invoice_status_details"])
    .copy()
)
inv_status["invoice_status_code"] = inv_status["invoice_status_code"].str.replace(
    r"^invoice_details_", "", regex=True
)

# Pivot client attributes to wide (client details, etc.)
client_wide = (
    t2.pivot_table(
        index=["client_id", "agency_id"],
        columns="attribute",
        values="value",
        aggfunc="first",
    )
    .reset_index()
)
if "client_details" not in client_wide.columns:
    client_wide["client_details"] = pd.NA

# Agency details
agency = t1.rename(columns={"ag_id": "agency_id", "qymx": "agency_details"})

# Join invoice statuses -> client/agency -> agency details
out = (
    inv_status.merge(client_wide[["client_id", "agency_id", "client_details"]], on="client_id", how="left")
    .merge(agency[["agency_id", "agency_details"]], on="agency_id", how="left")
)

out = out[
    [
        "invoice_id",
        "invoice_status_code",
        "invoice_status_details",
        "client_id",
        "client_details",
        "agency_id",
        "agency_details",
    ]
].sort_values(["invoice_id", "invoice_status_code"], kind="stable").reset_index(drop=True)

result = {"invoice_status_client_agency_details": out}
