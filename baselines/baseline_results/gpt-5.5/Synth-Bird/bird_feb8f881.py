import pandas as pd

df1 = tables["table_1"]
df2 = tables["table_2"]

# Normalize table_2 in case it stores lists inside cells
df2_norm = df2.copy()
for c in ["id", "value"]:
    df2_norm[c] = df2_norm[c].apply(lambda x: x if isinstance(x, list) else [x])

df2_norm = df2_norm.explode(["id", "value"], ignore_index=True)

# Extract format/status/uuid from the packed 'value' field
parts = df2_norm["value"].astype(str).str.split("|", n=2, expand=True)
df2_norm["format"] = parts[0]
df2_norm["status"] = parts[1]
df2_norm["uuid"] = parts[2]

banned_uuids = df2_norm.loc[df2_norm["status"].eq("Banned"), "uuid"].dropna().unique()

white_border_banned_count = (
    df1.loc[df1["uuid"].isin(banned_uuids) & df1["borderColor"].astype(str).str.lower().eq("white"), "uuid"]
    .drop_duplicates()
    .shape[0]
)

result = {
    "white_border_banned_cards_count": pd.DataFrame(
        {"white_border_banned_cards_count": [white_border_banned_count]}
    )
}
