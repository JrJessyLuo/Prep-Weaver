import pandas as pd

# Access preloaded tables
df_customers = tables['table_1']  # spider_cf094995_input_0.pkl
df_orders = tables['table_2']     # spider_cf094995_input_1.pkl
# df_branches = tables['table_3'] # Not needed for the final result

# Identify dish columns (all columns in orders except keys)
non_dish_cols = {"Customer_ID", "Branch_ID"}
dish_cols = [c for c in df_orders.columns if c not in non_dish_cols]

# Unpivot orders to long format: one row per (Customer, Dish) with Quantity
df_orders_long = (
    df_orders
    .melt(
        id_vars=["Customer_ID", "Branch_ID"],
        value_vars=dish_cols,
        var_name="Dish",
        value_name="Quantity"
    )
    .dropna(subset=["Quantity"])
    .reset_index(drop=True)
)

# Join with customers to get names
df_orders_with_names = df_orders_long.merge(
    df_customers[["Customer_ID", "Name"]],
    on="Customer_ID",
    how="left"
)

# Select and sort as required
final_df = (
    df_orders_with_names[["Name", "Dish", "Quantity"]]
    .sort_values(by=["Quantity", "Name", "Dish"], ascending=[False, True, True])
    .reset_index(drop=True)
)

# Package final result
result = {"name_dish_quantity_sorted": final_df}