import pandas as pd

# Tables are already loaded in scope as: tables['table_1'], tables['table_2']
df_customers = tables["table_1"]     # columns: CustomerID, Segment, Currency
df_consumption = tables["table_2"]   # columns: CustomerID, Consumption, Year, Month

# Join on CustomerID
df_joined = df_consumption.merge(
    df_customers[["CustomerID", "Segment"]],
    on="CustomerID",
    how="left"
)

# Filter to Segment == "SME" for Year == "2013"
df_sme_2013 = df_joined[
    (df_joined["Segment"] == "SME") & (df_joined["Year"].astype(str) == "2013")
].copy()

# Group by Month and compute mean Consumption for each month
monthly_mean_consumption = (
    df_sme_2013.assign(Month=df_sme_2013["Month"].astype(str).str.zfill(2))
    .groupby("Month", as_index=False)["Consumption"]
    .mean()
    .rename(columns={"Consumption": "MeanConsumption"})
    .sort_values("Month")
)

# Compute overall average monthly consumption for SME in 2013
overall_avg_monthly_consumption_sme_2013 = monthly_mean_consumption["MeanConsumption"].mean()

# Final answer as a DataFrame
answer_df = pd.DataFrame(
    {"AverageMonthlyConsumption_SME_2013": [overall_avg_monthly_consumption_sme_2013]}
)

# Required output variable
result = {"average_monthly_consumption_sme_2013": answer_df}