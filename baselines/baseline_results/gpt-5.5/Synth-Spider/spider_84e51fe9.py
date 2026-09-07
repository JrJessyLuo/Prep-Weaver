import pandas as pd

discounts = tables["table_1"]
rental_history = tables["table_2"]

top_discount_id = (
    rental_history.groupby("discount_id")
    .size()
    .reset_index(name="rental_history_records")
    .sort_values(["rental_history_records", "discount_id"], ascending=[False, True])
    .iloc[0]["discount_id"]
)

out = (
    discounts.loc[discounts["id"].eq(top_discount_id), ["nm"]]
    .rename(columns={"nm": "discount_name"})
    .reset_index(drop=True)
)

result = {"most_common_discount": out}
