import pandas as pd

# Use the already-loaded table mapping
df_expense = tables["table_4"]

# Filter to approved == true (handle potential casing/whitespace and missing values)
approved_mask = (
    df_expense["approved"]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq("true")
)
df_approved = df_expense.loc[approved_mask].copy()

# Parse expense_date and extract year
df_approved["expense_date"] = pd.to_datetime(df_approved["expense_date"], errors="coerce")
df_approved["year"] = df_approved["expense_date"].dt.year

# Compute year-wise sums of cost for approved expenses in 2019 and 2020
yearly_sums = (
    df_approved[df_approved["year"].isin([2019, 2020])]
    .groupby("year", as_index=False)["cost"]
    .sum()
    .rename(columns={"cost": "total_cost"})
    .sort_values("year")
)

# Subtract (2020 total − 2019 total) to get the difference
totals = yearly_sums.set_index("year")["total_cost"]
difference_2020_minus_2019 = totals.get(2020, 0.0) - totals.get(2019, 0.0)

# Final answer table
answer_df = pd.DataFrame(
    {"difference_2020_minus_2019_total_spent": [difference_2020_minus_2019]}
)

# Assign to result per guidelines
result = {"difference_total_spent_2019_vs_2020": answer_df}