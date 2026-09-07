import pandas as pd
import numpy as np

# Source tables from the provided dict 'tables'
df_rooms = tables['table_1'].copy()
df_build = tables['table_5'].copy()

# 1) Identify Stata building keys from building names (fallback to known keys '32','32P' if needed)
name_cols = [c for c in df_build.columns if "BUILDING" in c and "NAME" in c]
mask_build_name = pd.Series(False, index=df_build.index)
for c in name_cols:
    mask_build_name |= df_build[c].astype(str).str.contains("Stata", case=False, na=False)

stata_buildings = df_build.loc[mask_build_name, ["FCLT_BUILDING_KEY"] + name_cols].drop_duplicates()
stata_building_keys_detected = set(stata_buildings["FCLT_BUILDING_KEY"].astype(str))

# Known MIT Stata Center complex building numbers often include 32 and 32P
known_stata_keys = {"32", "32P"}

# Final set of Stata building keys
stata_building_keys = stata_building_keys_detected.union(known_stata_keys)

# 2) Filter rooms for Stata buildings
df_rooms = df_rooms.copy()
df_rooms["FCLT_BUILDING_KEY_str"] = df_rooms["FCLT_BUILDING_KEY"].astype(str)
rooms_stata_build = df_rooms[df_rooms["FCLT_BUILDING_KEY_str"].isin(stata_building_keys)].copy()
rooms_stata_build.drop(columns=["FCLT_BUILDING_KEY_str"], inplace=True)

# 3) Clean AREA and filter out null/zero areas
rooms_stata_build["AREA"] = pd.to_numeric(rooms_stata_build["AREA"], errors="coerce")
rooms_stata_nonzero = rooms_stata_build.dropna(subset=["AREA"])
rooms_stata_nonzero = rooms_stata_nonzero[rooms_stata_nonzero["AREA"] > 0]

# Ensure necessary columns exist
group_cols = []
floor_col = None
if "FCLT_FLOOR_KEY" in rooms_stata_nonzero.columns:
    floor_col = "FCLT_FLOOR_KEY"
    group_cols.append("FCLT_FLOOR_KEY")
elif "FLOOR" in rooms_stata_nonzero.columns:
    floor_col = "FLOOR"
    group_cols.append("FLOOR")

org_col = None
if "ORGANIZATION_NAME" in rooms_stata_nonzero.columns:
    org_col = "ORGANIZATION_NAME"
    group_cols.append("ORGANIZATION_NAME")
elif "FCLT_ORGANIZATION_KEY" in rooms_stata_nonzero.columns:
    org_col = "FCLT_ORGANIZATION_KEY"
    group_cols.append("FCLT_ORGANIZATION_KEY")

if not group_cols or floor_col is None or org_col is None:
    raise ValueError("Required grouping columns not found in rooms dataframe.")

# 4) Group and aggregate: room count, total area, average area per room
room_key_col = "FCLT_ROOM_KEY" if "FCLT_ROOM_KEY" in rooms_stata_nonzero.columns else None
if room_key_col is not None:
    room_count_spec = ("FCLT_ROOM_KEY", "nunique")
else:
    # Fallback count
    any_col = "ROOM" if "ROOM" in rooms_stata_nonzero.columns else rooms_stata_nonzero.columns[0]
    room_count_spec = (any_col, "count")

agg_df = (
    rooms_stata_nonzero
    .groupby(group_cols, dropna=False)
    .agg(
        room_count=room_count_spec,
        total_area=("AREA", "sum"),
    )
    .reset_index()
)
agg_df = agg_df[agg_df["room_count"] > 0].copy()
agg_df["avg_area_per_room"] = agg_df["total_area"] / agg_df["room_count"]

# Sort by floor and department name/key ascending
sort_cols = [floor_col, org_col]
agg_df = agg_df.sort_values(sort_cols + [org_col], ascending=[True, True, True])

# Build subtotals per floor and grand total
def fmt_int_comma(x):
    # round to nearest integer and format with commas
    return f"{int(round(x)):,}"

# Prepare detailed rows
detail_cols = {
    "Floor Key": agg_df[floor_col].astype(str),
    "Department": agg_df[org_col].astype(str),
    "Number of Rooms": agg_df["room_count"],
    "Total Area": agg_df["total_area"],
    "Average Area per Room": agg_df["avg_area_per_room"],
}
details = pd.DataFrame(detail_cols)

# Compute subtotals per floor
floor_groups = []
for fkey, g in details.groupby("Floor Key", sort=True):
    subtotal_rooms = g["Number of Rooms"].sum()
    subtotal_area = g["Total Area"].sum()
    subtotal_avg = subtotal_area / subtotal_rooms if subtotal_rooms != 0 else np.nan

    g2 = g.copy()
    # Only the first row of each floor should have the floor key
    if len(g2) > 0:
        g2.iloc[1:, g2.columns.get_loc("Floor Key")] = ""

    floor_groups.append(g2)

    # Append subtotal row (no floor key or department)
    subtotal_row = pd.DataFrame({
        "Floor Key": [""],
        "Department": [""],
        "Number of Rooms": [subtotal_rooms],
        "Total Area": [subtotal_area],
        "Average Area per Room": [subtotal_avg],
    })
    floor_groups.append(subtotal_row)

combined = pd.concat(floor_groups, ignore_index=True)

# Grand total row
grand_rooms = details["Number of Rooms"].sum()
grand_area = details["Total Area"].sum()
grand_avg = grand_area / grand_rooms if grand_rooms != 0 else np.nan
grand_row = pd.DataFrame({
    "Floor Key": [""],
    "Department": [""],
    "Number of Rooms": [grand_rooms],
    "Total Area": [grand_area],
    "Average Area per Room": [grand_avg],
})
combined = pd.concat([combined, grand_row], ignore_index=True)

# Round and format numeric columns
for c in ["Number of Rooms", "Total Area", "Average Area per Room"]:
    combined[c] = combined[c].round(0)

combined["Number of Rooms"] = combined["Number of Rooms"].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
combined["Total Area"] = combined["Total Area"].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
combined["Average Area per Room"] = combined["Average Area per Room"].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")

# Ensure sorting by floor key already applied via grouping; departments already sorted
final_df = combined[["Floor Key", "Department", "Number of Rooms", "Total Area", "Average Area per Room"]]

# Package result
result = {"Stata floor-department room and area summary": final_df}