import pandas as pd

books = tables["table_1"]
order_items = tables["table_2"]

pp_isbns = books.loc[books["Title"].eq("Pride and Prejudice"), "ISBN"].unique()

num_orders = order_items.loc[order_items["ISBN"].isin(pp_isbns), "oid"].nunique()

result = {
    "pride_and_prejudice_order_count": pd.DataFrame(
        {"number_of_orders": [num_orders]}
    )
}
