import pandas as pd

posts = tables["table_2"].copy()

# Clean types
posts["Id"] = posts["Id"].astype(str).str.strip('"')
posts["Id"] = pd.to_numeric(posts["Id"], errors="coerce").astype("Int64")
posts["ViewCount"] = pd.to_numeric(posts["ViewCount"], errors="coerce")

out = posts.loc[posts["ViewCount"].eq(1910), ["Id", "CommentCount"]].rename(
    columns={"Id": "PostId", "CommentCount": "comment_count"}
).reset_index(drop=True)

result = {"post_1910_views_comment_count": out}
