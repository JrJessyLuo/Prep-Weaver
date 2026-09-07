import pandas as pd

df_platforms = tables["table_1"].copy()
df_games = tables["table_2"].copy()

# Platform IDs in market districts Asia or USA
df_platforms["md"] = df_platforms["md"].astype(str).str.strip()
platform_ids = df_platforms.loc[df_platforms["md"].isin(["Asia", "USA"]), "Platform_ID"].astype(str).unique().tolist()

# Only keep platform-id columns that actually exist in the games table
platform_cols = [c for c in platform_ids if c in df_games.columns]

mask = df_games[platform_cols].notna().any(axis=1) if platform_cols else pd.Series(False, index=df_games.index)

titles = (
    df_games.loc[mask, ["Title"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"game_titles": titles}
