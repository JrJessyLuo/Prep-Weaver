import pandas as pd

# Access pre-loaded tables
df_platforms = tables['table_1']  # spider_00f8fe7f_input_0.pkl
df_games = tables['table_2']      # spider_00f8fe7f_input_1.pkl

# Reproduce the SAME logic as the reference code:
# 1) Filter platforms where md is in ["Asia", "USA"]
filtered_platforms = df_platforms[df_platforms['md'].isin(["Asia", "USA"])]

# 2) Collect their Platform_IDs (though there is no join key with games per reference)
platform_ids = filtered_platforms['Platform_ID'].unique().tolist()

# Since there are no shared columns and no explicit linkage,
# following the reference logic, we simply take the Titles from df_games.
# The question asks: "titles of games that have platforms in the market districts of Asia or the USA?"
# With no join available, the reproduced logic yields all game titles.
answer_df = df_games[['Title']].copy()

# Prepare final result mapping
result = {
    "titles_with_platforms_in_Asia_or_USA": answer_df
}