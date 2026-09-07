import pandas as pd

b = tables["table_1"].copy()
r = tables["table_2"].copy()

min_book = b.sort_values(["Pages", "Book_ID"], ascending=[True, True]).head(1)[["Book_ID"]]

out = (
    min_book.merge(r[["Book_ID", "rk"]], on="Book_ID", how="left")
    .rename(columns={"rk": "rank"})
    [["rank"]]
)

result = {"book_smallest_pages_rank": out.reset_index(drop=True)}
