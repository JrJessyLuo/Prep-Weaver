import pandas as pd
import numpy as np

# Identify the Stata building from the current building table
buildings = tables["table_1"].copy()
name_cols = [c for c in ["BUILDING_NAME_LONG", "BUILDING_NAME", "PARENT_BUILDING_NAME_LONG", "PARENT_BUILDING_NAME"] if c in buildings.columns]

stata_mask = pd.Series(False, index=buildings.index)
for c in name_cols:
    stata_mask |= buildings[c].astype(str).str.contains("STATA", case=False, na=False)

key_cols = [c for c in ["FCLT_BUILDING_KEY", "FAC_BUILDING_KEY", "BUILDING_NUMBER"] if c in buildings.columns]
stata_keys = set()
for c in key_cols:
    stata_keys.update(buildings.loc[stata_mask, c].dropna().astype(str))

# Fallback for the Ray and Maria Stata Center if name matching is unavailable
if not stata_keys:
    stata_keys = {"32"}

# Current room-level data with areas
rooms = tables["table_5"].copy()

building_col = "BUILDING_KEY" if "BUILDING_KEY" in rooms.columns else "FCLT_BUILDING_KEY"
room_key_col = "fac_room_key" if "fac_room_key" in rooms.columns else ("FCLT_ROOM_KEY" if "FCLT_ROOM_KEY" in rooms.columns else "BUILDING_ROOM")
space_id_col = "SPACE_ID" if "SPACE_ID" in rooms.columns else room_key_col

rooms = rooms[rooms[building_col].astype(str).isin(stata_keys)].copy()

# Join space usage labels where available
if "table_8" in tables:
    usage_lookup = tables["table_8"].copy()
    if {"BUILDING_ROOM", "SPACE_USAGE"}.issubset(usage_lookup.columns):
        usage_lookup = usage_lookup[["BUILDING_ROOM", "SPACE_USAGE"]].drop_duplicates("BUILDING_ROOM")
        rooms = rooms.merge(
            usage_lookup,
            how="left",
            left_on=room_key_col,
            right_on="BUILDING_ROOM"
        )

# Define final semantic fields
if "SPACE_USAGE" in rooms.columns and rooms["SPACE_USAGE"].notna().any():
    rooms["_usage_type"] = rooms["SPACE_USAGE"]
elif "MAJOR_USE_DESC" in rooms.columns:
    rooms["_usage_type"] = rooms["MAJOR_USE_DESC"]
else:
    rooms["_usage_type"] = "Unknown"

if "ROOM_FULL_NAME" in rooms.columns:
    rooms["_space_name"] = rooms["ROOM_FULL_NAME"].where(rooms["ROOM_FULL_NAME"].notna(), rooms[space_id_col])
else:
    rooms["_space_name"] = rooms[space_id_col]

rooms["_usage_type"] = rooms["_usage_type"].fillna("Unknown").astype(str)
rooms["_space_name"] = rooms["_space_name"].fillna(rooms[space_id_col]).fillna("Unknown").astype(str)
rooms["_space_id"] = rooms[space_id_col].fillna(rooms[room_key_col]).astype(str)
rooms["_access"] = rooms["ACCESS_LEVEL"]

# Exclude usage types containing STORAGE
rooms = rooms[~rooms["_usage_type"].str.contains("STORAGE", case=False, na=False)].copy()

# Avoid accidental duplicate room rows after joins
rooms = rooms.drop_duplicates(subset=["_space_id", "_access", "_usage_type", "_space_name"])

def summarize(df):
    return {
        "Number of Spaces": df["_space_id"].nunique(),
        "Total Area": df["AREA"].sum(),
        "Average Area": df["AREA"].mean()
    }

rows = []

def sort_key(x):
    if pd.isna(x):
        return (1, "")
    try:
        return (0, float(x))
    except Exception:
        return (0, str(x))

for access in sorted(rooms["_access"].dropna().unique(), key=sort_key):
    access_df = rooms[rooms["_access"] == access]

    for usage in sorted(access_df["_usage_type"].dropna().unique()):
        usage_df = access_df[access_df["_usage_type"] == usage]

        detail = (
            usage_df.groupby("_space_name", dropna=False)
            .agg(
                **{
                    "Number of Spaces": ("_space_id", "nunique"),
                    "Total Area": ("AREA", "sum"),
                    "Average Area": ("AREA", "mean")
                }
            )
            .reset_index()
            .sort_values("_space_name")
        )

        for _, r in detail.iterrows():
            rows.append({
                "_access_sort": access,
                "Access Level": access,
                "Usage Type": usage,
                "Name of Space": r["_space_name"],
                "Number of Spaces": r["Number of Spaces"],
                "Total Area": r["Total Area"],
                "Average Area": r["Average Area"]
            })

        usage_summary = summarize(usage_df)
        rows.append({
            "_access_sort": access,
            "Access Level": access,
            "Usage Type": usage,
            "Name of Space": "Subtotal",
            **usage_summary
        })

    access_summary = summarize(access_df)
    rows.append({
        "_access_sort": access,
        "Access Level": access,
        "Usage Type": "Access Level Subtotal",
        "Name of Space": "",
        **access_summary
    })

grand_summary = summarize(rooms)
rows.append({
    "_access_sort": np.nan,
    "Access Level": "",
    "Usage Type": "Grand Total",
    "Name of Space": "",
    **grand_summary
})

out = pd.DataFrame(rows)

def fmt_int(x):
    if pd.isna(x):
        return ""
    return f"{int(round(float(x))):,}"

def fmt_access(x):
    if pd.isna(x) or x == "":
        return ""
    try:
        xf = float(x)
        return str(int(xf)) if xf.is_integer() else str(x)
    except Exception:
        return str(x)

# Display access level only when it changes from the previous entry
display_access = []
prev_access = object()
for x in out["_access_sort"]:
    if pd.isna(x):
        display_access.append("")
    elif x != prev_access:
        display_access.append(fmt_access(x))
    else:
        display_access.append("")
    prev_access = x

out["Access Level"] = display_access

for col in ["Number of Spaces", "Total Area", "Average Area"]:
    out[col] = out[col].apply(fmt_int)

out = out[[
    "Access Level",
    "Usage Type",
    "Name of Space",
    "Number of Spaces",
    "Total Area",
    "Average Area"
]]

result = {
    "stata_building_spaces_by_access_and_usage": out
}
