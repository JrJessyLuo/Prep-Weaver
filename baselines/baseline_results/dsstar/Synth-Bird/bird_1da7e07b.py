import pandas as pd

posts = tables["table_2"]

target = 1910

# Drop rows with missing ViewCount, then compute absolute distance to target
vc = posts[["Id", "ViewCount", "CommentCount"]].dropna(subset=["ViewCount"]).copy()
vc["abs_diff"] = (vc["ViewCount"] - target).abs()

# Find the closest ViewCount to 1910 (handle ties by returning all minima)
min_diff = vc["abs_diff"].min()
closest = vc.loc[vc["abs_diff"] == min_diff].sort_values(["abs_diff", "ViewCount", "Id"])

answer = closest[["CommentCount"]].reset_index(drop=True)

result = {"answer": answer}