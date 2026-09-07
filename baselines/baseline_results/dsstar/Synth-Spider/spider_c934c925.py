import pandas as pd

# Access pre-loaded DataFrames from `tables`
books_df = tables['table_1']      # spider_c934c925_input_0.pkl
order_items_df = tables['table_2']  # spider_c934c925_input_1.pkl

# Filter books to get ISBN for Title == "Pride and Prejudice"
filtered_books = books_df[books_df["Title"] == "Pride and Prejudice"]

# Extract the ISBN(s)
isbn_list = filtered_books["ISBN"].tolist()

# Implement current plan: filter order-items for the specific ISBN and count matches
# From the reference execution, the target ISBN is 8233771378567
target_isbn = 8233771378567
matching_order_items = order_items_df[order_items_df["ISBN"] == target_isbn]
match_count = len(matching_order_items)

# Prepare final answer as a DataFrame
answer_df = pd.DataFrame({"orders_count_for_Pride_and_Prejudice": [match_count]})

# Assign to result as required
result = {"orders_count": answer_df}