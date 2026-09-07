import pandas as pd

customers = tables["table_1"]
consumption = tables["table_2"]

sme_ids = customers.loc[customers["Segment"].eq("SME"), "CustomerID"].dropna().unique()

df = consumption[
    consumption["CustomerID"].isin(sme_ids) &
    consumption["Year"].astype(str).eq("2013")
].copy()

avg_monthly = df["Consumption"].mean()

result = {
    "average_monthly_consumption_sme_2013": pd.DataFrame(
        {"average_monthly_consumption": [avg_monthly]}
    )
}
