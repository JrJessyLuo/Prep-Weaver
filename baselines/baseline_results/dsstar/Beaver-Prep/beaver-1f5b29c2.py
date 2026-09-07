import pandas as pd

# Source DataFrames from provided `tables` dict
fclt_rooms = tables["table_2"]
fclt_building = tables["table_6"]
space_detail = tables["table_10"]

# 1) Select/join columns of interest (replicate reference logic)
bldg_keep_cols = [
    "FCLT_BUILDING_KEY",
    "BUILDING_NUMBER",
    "BUILDING_NAME_LONG",
    "OWNERSHIP_TYPE",
]
bldg_df = fclt_building[[c for c in bldg_keep_cols if c in fclt_building.columns]].copy()

rooms_keep_cols = [
    "FCLT_ROOM_KEY",
    "FCLT_BUILDING_KEY",
    "BUILDING_ROOM",
    "FLOOR",
    "ROOM",
    "SPACE_ID",
    "AREA",
    "ORGANIZATION_NAME",
    "ACCESS_LEVEL",
]
rooms_df = fclt_rooms[[c for c in rooms_keep_cols if c in fclt_rooms.columns]].copy()

space_keep_cols = [
    "BUILDING_ROOM",
    "ROOM_SQUARE_FOOTAGE",
    "ROOM_COUNTER",
    "BUILDING_COMPONENT",
]
space_df = space_detail[[c for c in space_keep_cols if c in space_detail.columns]].copy()

# 2) Join FCLT_ROOMS -> FCLT_BUILDING (many_to_one on FCLT_BUILDING_KEY)
rooms_bldg = rooms_df.merge(
    bldg_df,
    on="FCLT_BUILDING_KEY",
    how="left",
    validate="many_to_one",
)

# 3) Join with SPACE_DETAIL on BUILDING_ROOM (left join, may be many-to-many)
rooms_bldg_space = rooms_bldg.merge(
    space_df.add_suffix("_SPACE"),
    left_on="BUILDING_ROOM",
    right_on="BUILDING_ROOM_SPACE",
    how="left",
)

# 4) Standardize output columns
out_cols = [
    "FCLT_ROOM_KEY",
    "BUILDING_NUMBER",
    "BUILDING_NAME_LONG",
    "OWNERSHIP_TYPE",
    "FLOOR",
    "ROOM",
    "ORGANIZATION_NAME",
    "AREA",  # from FCLT_ROOMS
    "ROOM_COUNTER_SPACE",  # from SPACE_DETAIL
    "ROOM_SQUARE_FOOTAGE_SPACE",
    "BUILDING_ROOM",
    "ACCESS_LEVEL",
]
for c in out_cols:
    if c not in rooms_bldg_space.columns:
        rooms_bldg_space[c] = pd.NA

base_rooms = rooms_bldg_space[out_cols].copy()

# 5) Compute per-building total area (using AREA from FCLT_ROOMS)
building_totals = (
    base_rooms
    .groupby("BUILDING_NUMBER", dropna=False, as_index=False)["AREA"]
    .sum(min_count=1)
    .rename(columns={"AREA": "building_total_area"})
)

# 6) Attach building_total_area back to room-level rows
base_rooms = base_rooms.merge(
    building_totals, on="BUILDING_NUMBER", how="left", validate="many_to_one"
)

# 7) Compute room's share of building total area
base_rooms["room_area_share_of_building"] = (
    base_rooms["AREA"] / base_rooms["building_total_area"]
)

# 8) Prepare core fields required by question
df = base_rooms.copy()

# Number of rooms per BUILDING_ROOM from SPACE_DETAIL. If missing, treat as 1 (the room itself)
# But per reference, ROOM_COUNTER_SPACE is kept as-is. We'll default to 1 where NaN for display.
df["num_rooms_raw"] = df["ROOM_COUNTER_SPACE"]
df["num_rooms"] = df["num_rooms_raw"].fillna(1)

# Compute grand total area (sum over all buildings; use building_totals unique buildings)
grand_total_area = building_totals["building_total_area"].sum(min_count=1)

# Compute building-level share vs grand total
building_share_vs_all = building_totals.copy()
building_share_vs_all["pct_of_all_buildings"] = building_share_vs_all["building_total_area"] / grand_total_area

# 9) Build detail rows (one per room row in df)
detail_cols = [
    "Building Name",
    "Floor",
    "Room",
    "Ownership Type",
    "Organization Name",
    "Number of Rooms",
    "Area",
    "Percent of Building Area",
    "BUILDING_NUMBER",
    "FLOOR",
]
details = pd.DataFrame({
    "Building Name": df["BUILDING_NAME_LONG"],
    "Floor": df["FLOOR"],
    "Room": df["ROOM"],
    "Ownership Type": df["OWNERSHIP_TYPE"],
    "Organization Name": df["ORGANIZATION_NAME"],
    "Number of Rooms": df["num_rooms"],
    "Area": df["AREA"],
    "Percent of Building Area": df["room_area_share_of_building"],
    "BUILDING_NUMBER": df["BUILDING_NUMBER"],
    "FLOOR": df["FLOOR"],
})

# 10) Floor-level subtotals per (BUILDING_NUMBER, FLOOR)
floor_grp = df.groupby(["BUILDING_NUMBER", "FLOOR"], dropna=False, as_index=False)
floor_sub = floor_grp.agg(
    **{
        "Area": ("AREA", "sum"),
        "Number of Rooms": ("num_rooms", "sum"),
        # For floor subtotal, percent relative to its building total area = floor_area / building_total_area
        "building_total_area": ("building_total_area", "first"),
        "BUILDING_NAME_LONG": ("BUILDING_NAME_LONG", "first"),
        "OWNERSHIP_TYPE": ("OWNERSHIP_TYPE", "first"),
        "ORGANIZATION_NAME": ("ORGANIZATION_NAME", "first"),
    }
)
floor_sub["Percent of Building Area"] = floor_sub["Area"] / floor_sub["building_total_area"]
floor_sub["Building Name"] = floor_sub["BUILDING_NAME_LONG"]
floor_sub["Floor"] = floor_sub["FLOOR"].astype(object)  # keep as-is for grouping
floor_sub["Room"] = "Subtotal (Floor)"
floor_sub["Ownership Type"] = floor_sub["OWNERSHIP_TYPE"]
floor_sub["Organization Name"] = ""  # blank at subtotal row

floor_sub_rows = floor_sub[[
    "Building Name", "Floor", "Room", "Ownership Type", "Organization Name",
    "Number of Rooms", "Area", "Percent of Building Area",
    "BUILDING_NUMBER", "FLOOR"
]]

# 11) Building-level subtotal (across all floors per building)
bldg_grp = df.groupby("BUILDING_NUMBER", dropna=False, as_index=False)
bldg_sub = bldg_grp.agg(
    **{
        "Area": ("AREA", "sum"),
        "Number of Rooms": ("num_rooms", "sum"),
        "BUILDING_NAME_LONG": ("BUILDING_NAME_LONG", "first"),
        "OWNERSHIP_TYPE": ("OWNERSHIP_TYPE", "first"),
    }
)
# Join to get share vs all buildings
bldg_sub = bldg_sub.merge(
    building_share_vs_all[["BUILDING_NUMBER", "pct_of_all_buildings", "building_total_area"]],
    on="BUILDING_NUMBER",
    how="left",
    validate="one_to_one",
)
bldg_sub["Building Name"] = bldg_sub["BUILDING_NAME_LONG"]
bldg_sub["Floor"] = ""
bldg_sub["Room"] = "Subtotal (Building)"
bldg_sub["Ownership Type"] = bldg_sub["OWNERSHIP_TYPE"]
bldg_sub["Organization Name"] = ""
# For building subtotal, percent should be relative to all buildings
bldg_sub["Percent of Building Area"] = bldg_sub["pct_of_all_buildings"]

bldg_sub_rows = bldg_sub[[
    "Building Name", "Floor", "Room", "Ownership Type", "Organization Name",
    "Number of Rooms", "Area", "Percent of Building Area",
    "BUILDING_NUMBER"
]].copy()
bldg_sub_rows["FLOOR"] = pd.NA  # for sort alignment

# 12) Grand total across all buildings
grand_area = df["AREA"].sum(min_count=1)
grand_num_rooms = df["num_rooms"].sum(min_count=1)
grand_pct = 1.0 if pd.notna(grand_area) and grand_area != 0 else pd.NA

grand_row = pd.DataFrame([{
    "Building Name": "",
    "Floor": "",
    "Room": "Grand Total",
    "Ownership Type": "",
    "Organization Name": "",
    "Number of Rooms": grand_num_rooms,
    "Area": grand_area,
    "Percent of Building Area": grand_pct,
    "BUILDING_NUMBER": pd.NA,
    "FLOOR": pd.NA,
}])

# 13) Combine: details + floor subtotals + building subtotals + grand total
combined = pd.concat(
    [details, floor_sub_rows, bldg_sub_rows, grand_row],
    ignore_index=True
)

# 14) Sort: by BUILDING_NUMBER, then Floor (with subtotals and totals placed after details for each floor and building).
# We'll define a helper sort key:
def sort_keys(df_):
    # Order: details (actual rooms), then floor subtotal, then building subtotal, then grand total
    # Create an order rank based on "Room" markers
    marker = pd.Series(0, index=df_.index)
    marker = marker.where(df_["Room"] != "Subtotal (Floor)", 1)
    marker = marker.where(df_["Room"] != "Subtotal (Building)", 2)
    marker = marker.where(df_["Room"] != "Grand Total", 3)
    return marker

combined["_order"] = sort_keys(combined)

# For numeric sortable floor: try to coerce to numeric; non-numeric floors go after numerics but keep original order
def coerce_floor(v):
    try:
        return float(v)
    except Exception:
        return float("inf")

combined["_floor_sort"] = combined["FLOOR"].map(coerce_floor)

# For BUILDING_NUMBER, keep as string but sort lexicographically; Grand total with NA goes last
combined["_bldg_null"] = combined["BUILDING_NUMBER"].isna()

combined = combined.sort_values(
    by=["_bldg_null", "BUILDING_NUMBER", "_floor_sort", "_order", "Room"],
    kind="mergesort"
).reset_index(drop=True)

# 15) Formatting:
# - Round numeric to integers with commas, except percentages rounded to two decimals.
# Keep a clean copy before formatting for safety
final = combined.copy()

# Compute display percentage:
# For detail and floor subtotal rows, "Percent of Building Area" already computed.
# For building subtotal and grand total, we set previously.
# Format percentages to 2 decimals
final["Percent of Building Area"] = (final["Percent of Building Area"] * 100).round(2)

# Round Number of Rooms and Area to integers
for col in ["Number of Rooms", "Area"]:
    # Round then cast to Int64 to preserve NaNs, then format
    final[col] = pd.to_numeric(final[col], errors="coerce").round(0)

# Build formatted display columns
def fmt_int_with_commas(x):
    if pd.isna(x):
        return ""
    try:
        return f"{int(round(float(x))):,}"
    except Exception:
        return ""

def fmt_pct(x):
    if pd.isna(x):
        return ""
    return f"{float(x):,.2f}%"

final["Number of Rooms"] = final["Number of Rooms"].apply(fmt_int_with_commas)
final["Area"] = final["Area"].apply(fmt_int_with_commas)
final["Percent of Building Area"] = final["Percent of Building Area"].apply(fmt_pct)

# Select and rename columns per question
answer = final[[
    "Building Name",
    "Floor",
    "Room",
    "Ownership Type",
    "Organization Name",
    "Number of Rooms",
    "Area",
    "Percent of Building Area",
]]

# Assign to result dict as required
result = {"rooms_with_subtotals": answer}