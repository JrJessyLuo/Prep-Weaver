import pandas as pd

# Access preloaded tables
books = tables['table_1']        # spider_876d06b8_input_0.pkl
orders_details = tables['table_2']  # spider_876d06b8_input_1.pkl

# Reproduce the same logic as the reference code
target_title = "Pride and Prejudice"
isbn_series = books.loc[books["Title"] == target_title, "ISBN"]

if isbn_series.empty:
    count = 0
else:
    isbn_str = str(isbn_series.iloc[0])
    prefix = f"{isbn_str}-"
    isbn_amount_str = orders_details["ISBN_amount"].astype(str)
    count = isbn_amount_str.str.startswith(prefix).sum()

# Prepare final answer as a DataFrame and assign to `result`
answer_df = pd.DataFrame({"orders_count": [int(count)]})
result = {"pride_and_prejudice_orders_count": answer_df}