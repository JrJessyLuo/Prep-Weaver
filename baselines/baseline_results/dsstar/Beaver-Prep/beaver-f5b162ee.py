import pandas as pd

# Source tables from provided dict `tables`
fclt_rooms = tables["table_7"]
fclt_major_use = tables["table_2"]
fclt_major_use_hist = tables["table_8"]

# Filter out rows where MAJOR_USE_DESC starts with 'ZUSE' or MAJOR_USE starts with 'ZUSE'
mask_zuse_desc = fclt_rooms["MAJOR_USE_DESC"].astype(str).str.startswith("ZUSE", na=False)
mask_zuse_code = fclt_rooms["MAJOR_USE"].astype(str).str.startswith("ZUSE", na=False) if "MAJOR_USE" in fclt_rooms.columns else False
rooms_no_zuse = fclt_rooms.loc[~(mask_zuse_desc | mask_zuse_code)].copy()

# Determine latest hist attributes per key (use HIST to ensure authoritative ASSIGNABLE flag)
latest_hist = (
    fclt_major_use_hist.sort_values(["FCLT_MAJOR_USE_KEY", "FISCAL_PERIOD"])
    .groupby("FCLT_MAJOR_USE_KEY", as_index=False)
    .tail(1)[["FCLT_MAJOR_USE_KEY", "ASSIGNABLE"]]
)

# Join filtered rooms with latest ASSIGNABLE from HIST
rooms_joined = rooms_no_zuse.merge(latest_hist, on="FCLT_MAJOR_USE_KEY", how="left")

# If ASSIGNABLE still null (no hist), fallback to current dim
if rooms_joined["ASSIGNABLE"].isna().any():
    dim_assign = fclt_major_use[["FCLT_MAJOR_USE_KEY", "ASSIGNABLE"]].drop_duplicates()
    rooms_joined = rooms_joined.merge(
        dim_assign,
        on="FCLT_MAJOR_USE_KEY",
        how="left",
        suffixes=("", "_DIM")
    )
    rooms_joined["ASSIGNABLE"] = rooms_joined["ASSIGNABLE"].fillna(rooms_joined["ASSIGNABLE_DIM"])
    rooms_joined = rooms_joined.drop(columns=[c for c in rooms_joined.columns if c.endswith("_DIM")])

# Ensure ASSIGNABLE is integer for grouping
rooms_joined["ASSIGNABLE"] = rooms_joined["ASSIGNABLE"].astype("Int64")

# Map ASSIGNABLE to labels
assignable_map = {1: "ASSIGNABLE", 0: "NON-ASSIGNABLE"}
rooms_joined["ASSIGNABLE_LABEL"] = rooms_joined["ASSIGNABLE"].map(assignable_map)

# Core aggregation by ASSIGNABLE and MAJOR_USE_DESC
group_cols = ["ASSIGNABLE_LABEL", "MAJOR_USE_DESC"]
agg_df = (
    rooms_joined
    .groupby(group_cols, dropna=False, as_index=False)
    .agg(
        rooms_count=("FCLT_ROOM_KEY", "count"),
        area_sum=("AREA", "sum"),
        area_mean=("AREA", "mean"),
    )
)

# Sort by assignable status then major use description
agg_df = agg_df.sort_values(group_cols, na_position="last").reset_index(drop=True)

# Build subtotals per ASSIGNABLE_LABEL
subtotals = (
    agg_df
    .groupby(["ASSIGNABLE_LABEL"], dropna=False, as_index=False)
    .agg(
        rooms_count=("rooms_count", "sum"),
        area_sum=("area_sum", "sum"),
        area_mean=("area_mean", "mean"),
    )
)
subtotals["MAJOR_USE_DESC"] = "Subtotal"

# Prepare grand total row
grand_total = pd.DataFrame({
    "ASSIGNABLE_LABEL": [pd.NA],
    "MAJOR_USE_DESC": ["Grand Total"],
    "rooms_count": [rooms_joined["FCLT_ROOM_KEY"].shape[0]],
    "area_sum": [rooms_joined["AREA"].sum()],
    "area_mean": [rooms_joined["AREA"].mean()],
})

# Concatenate detail + subtotals and place subtotal after each group
combined = pd.concat([agg_df, subtotals], ignore_index=True)
combined["is_subtotal"] = (combined["MAJOR_USE_DESC"] == "Subtotal")
combined = combined.sort_values(["ASSIGNABLE_LABEL", "is_subtotal", "MAJOR_USE_DESC"], na_position="last")
combined = combined.drop(columns="is_subtotal").reset_index(drop=True)

# Append grand total
final_df = pd.concat([combined, grand_total], ignore_index=True)

# Suppress repeating labels: assign null where same as previous row, but keep for first in group
final_df["ASSIGNABLE_LABEL_DISPLAY"] = final_df["ASSIGNABLE_LABEL"]
final_df["MAJOR_USE_DESC_DISPLAY"] = final_df["MAJOR_USE_DESC"]

# For subtotal and grand total rows, blank out labels
is_total_row = final_df["MAJOR_USE_DESC"].isin(["Subtotal", "Grand Total"])
final_df.loc(is_total_row, ["ASSIGNABLE_LABEL_DISPLAY", "MAJOR_USE_DESC_DISPLAY"])

# For non-total rows, suppress repeats when equal to previous row
for col in ["ASSIGNABLE_LABEL_DISPLAY", "MAJOR_USE_DESC_DISPLAY"]:
    prev = final_df[col].shift(1)
    same_as_prev = final_df[col] == prev
    # Do not blank first row or when previous is NA and current is not
    final_df.loc[same_as_prev & ~is_total_row, col] = pd.NA

# Select and rename columns as required
answer = final_df.rename(columns={
    "ASSIGNABLE_LABEL_DISPLAY": "ASSIGNABLE_STATUS",
    "MAJOR_USE_DESC_DISPLAY": "MAJOR_USE_DESC",
    "rooms_count": "TOTAL_ROOMS",
    "area_sum": "TOTAL_AREA",
    "area_mean": "AVERAGE_AREA",
})[["ASSIGNABLE_STATUS", "MAJOR_USE_DESC", "TOTAL_ROOMS", "TOTAL_AREA", "AVERAGE_AREA"]]

# Package result
result = {"assignable_by_major_use_with_totals": answer}