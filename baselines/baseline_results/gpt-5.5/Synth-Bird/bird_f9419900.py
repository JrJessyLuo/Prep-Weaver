import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Build full uuid from parts in table_2
t2 = t2.copy()
t2["uuid"] = (
    t2["uuid_part1"].astype(str) + "-" +
    t2["uuid_part2"].astype(str) + "-" +
    t2["uuid_part3"].astype(str) + "-" +
    t2["uuid_part4"].astype(str) + "-" +
    t2["uuid_part5"].astype(str)
)

# Uuids that have Chinese Simplified foreign language data
cn_uuids = set(
    t2.loc[
        (t2["attribute"].astype(str) == "language") &
        (t2["value"].astype(str) == "Chinese Simplified"),
        "uuid"
    ].dropna().unique()
)

total_cards = t1["uuid"].dropna().nunique()
cn_cards = t1.loc[t1["uuid"].isin(cn_uuids), "uuid"].nunique()

percentage = (cn_cards / total_cards * 100) if total_cards else 0.0

result = {
    "cards_chinese_simplified_percentage": pd.DataFrame(
        {"percentage_chinese_simplified": [percentage]}
    )
}
