import pandas as pd

# Source table: Community posts
posts = tables["table_7"]

tags = posts["Tags"].fillna("").astype(str)
total_posts = len(posts)

# Strict R tag only (exclude "<r-...>" by requiring not followed by "-")
r_posts_ci_strict_mask = tags.str.contains(r"(?i)<r>", regex=True) & ~tags.str.contains(r"(?i)<r-", regex=True)
final_r_posts = int(r_posts_ci_strict_mask.sum())

final_percentage = 100 * final_r_posts / total_posts if total_posts else float("nan")

answer_df = pd.DataFrame(
    {
        "total_posts": [total_posts],
        "r_posts": [final_r_posts],
        "percentage_r_posts": [final_percentage],
    }
)

result = {"r_language_post_percentage": answer_df}