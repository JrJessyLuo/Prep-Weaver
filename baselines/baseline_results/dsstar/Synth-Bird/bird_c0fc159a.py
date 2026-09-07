import pandas as pd

# Tables are assumed to be preloaded in a dict named `tables`
cards_df = tables["table_1"]      # bird_c0fc159a_input_0.pkl
legality_df = tables["table_2"]   # bird_c0fc159a_input_1.pkl

# 1) Filter to future-frame cards and keep distinct uuids
future_cards = (
    cards_df.loc[cards_df["frameVersion"] == "future", ["uuid"]]
    .dropna()
    .drop_duplicates()
)

# 2) Join with legality data (uuid -> format/status)
future_legality = future_cards.merge(
    legality_df[["uuid", "format", "status"]],
    on="uuid",
    how="inner"
)

# 3) Distinct future-frame card count (among cards with at least one legality row after join)
distinct_future_frame_card_count = future_legality["uuid"].nunique()

# Pivot: uuid × format -> status (if multiple statuses exist for same uuid/format, keep unique sorted)
future_legality_pivot = (
    future_legality.pivot_table(
        index="uuid",
        columns="format",
        values="status",
        aggfunc=lambda s: "|".join(sorted(set(s.dropna().astype(str))))
    )
    .sort_index()
)

# Summarize each card’s set of legality statuses across formats
# (normalize any multi-status cells split by "|" and take union across all formats)
status_set_by_uuid = (
    future_legality_pivot.apply(
        lambda row: tuple(
            sorted(
                {
                    token
                    for cell in row.dropna().astype(str)
                    for token in cell.split("|")
                    if token != ""
                }
            )
        ),
        axis=1
    )
    .rename("status_set")
    .reset_index()
)

# Distribution of status sets across cards
status_set_summary = (
    status_set_by_uuid.groupby("status_set")
    .size()
    .reset_index(name="card_count")
    .sort_values(["card_count", "status_set"], ascending=[False, True])
    .reset_index(drop=True)
)

# Final answer as required: dict[str, pandas.DataFrame]
result = {
    "future_frame_card_count": pd.DataFrame(
        {"distinct_future_frame_card_count": [distinct_future_frame_card_count]}
    ),
    "future_frame_legality_status_distribution": status_set_summary,
}