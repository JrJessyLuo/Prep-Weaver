import pandas as pd

books = tables["table_1"]
order_items = tables["table_2"]

# ISBN(s) for "Pride and Prejudice"
pride_isbns = set(books.loc[books["Title"].eq("Pride and Prejudice"), "ISBN"].astype(str))

# Extract ISBN from packed "ISBN_amount" and count distinct orders containing the book
items = order_items.copy()
items["ISBN"] = items["ISBN_amount"].astype(str).str.split("-", n=1, expand=True)[0]

num_orders = items.loc[items["ISBN"].isin(pride_isbns), "IdOrder"].nunique()

result = {
    "orders_for_pride_and_prejudice": pd.DataFrame({"number_of_orders": [num_orders]})
}
