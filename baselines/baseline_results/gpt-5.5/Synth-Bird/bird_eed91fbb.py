import pandas as pd

posts = tables["table_2"].copy()
users = tables["table_3"].copy()

targets = ["Mornington", "Amos"]

# Ensure numeric ViewCount
posts["ViewCount"] = pd.to_numeric(posts["ViewCount"], errors="coerce").fillna(0)

# Get all user IDs that match each display name (in case of duplicates)
name_to_ids = (
    users[users["DisplayName"].isin(targets)]
    .groupby("DisplayName")["Id"]
    .apply(list)
    .to_dict()
)

def total_views_for(name: str) -> float:
    ids = name_to_ids.get(name, [])
    m = False
    if ids:
        m = m | posts["oui"].isin(ids)
    if "OwnerDisplayName" in posts.columns:
        m = m | (posts["OwnerDisplayName"] == name)
    return float(posts.loc[m, "ViewCount"].sum())

mornington_views = total_views_for("Mornington")
amos_views = total_views_for("Amos")

out = pd.DataFrame(
    {
        "Mornington_ViewCount": [mornington_views],
        "Amos_ViewCount": [amos_views],
        "ViewCount_Difference": [mornington_views - amos_views],
    }
)

result = {"viewcount_difference": out}
