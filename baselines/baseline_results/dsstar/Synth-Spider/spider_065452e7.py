import pandas as pd

# Access pre-loaded tables
df_books = tables['table_1']
df_reviews = tables['table_2']

# Perform inner join on Book_ID
df_joined = df_books.merge(df_reviews, on="Book_ID", how="inner")

# Identify the book(s) with the minimum number of pages
min_pages = df_books["Pages"].min()
books_min_pages = df_books[df_books["Pages"] == min_pages][["Book_ID", "Title", "Pages"]]

# Retrieve rk for those Book_ID(s)
min_page_book_ids = books_min_pages["Book_ID"].unique()
rk_for_min_pages = df_joined[df_joined["Book_ID"].isin(min_page_book_ids)][["Book_ID", "rk"]].drop_duplicates()

# Prepare final result mapping
result = {
    "rk_for_book_with_min_pages": rk_for_min_pages.reset_index(drop=True)
}