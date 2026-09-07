import pandas as pd

# Helper to coerce numeric
def safe_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")

# 1) Pick building DF: prefer FAC_BUILDING then FCLT_BUILDING, ensure required cols
if isinstance(tables.get("table_1"), pd.DataFrame):
    df_bldg = tables["table_1"].copy()
    bldg_label = "FAC_BUILDING"
    bldg_key_col = "FAC_BUILDING_KEY" if "FAC_BUILDING_KEY" in df_bldg.columns else None
    gross_sqft_col = "EXT_GROSS_AREA" if "EXT_GROSS_AREA" in df_bldg.columns else None
    if not (bldg_key_col and gross_sqft_col):
        df_bldg = None
else:
    df_bldg = None

if df_bldg is None:
    if isinstance(tables.get("table_3"), pd.DataFrame):
        df_bldg = tables["table_3"].copy()
        bldg_label = "FCLT_BUILDING"
        bldg_key_col = "FCLT_BUILDING_KEY" if "FCLT_BUILDING_KEY" in df_bldg.columns else None
        gross_sqft_col = "EXT_GROSS_AREA" if "EXT_GROSS_AREA" in df_bldg.columns else None

# Ensure mandatory columns
assert df_bldg is not None, "No suitable building table found."
assert bldg_key_col in df_bldg.columns, "Building key column missing."
assert gross_sqft_col in df_bldg.columns, "Gross sqft column missing."
assert "OWNERSHIP_TYPE" in df_bldg.columns, "OWNERSHIP_TYPE missing."
assert "BUILDING_USE" in df_bldg.columns, "BUILDING_USE missing."

# Coerce gross sqft numeric
df_bldg[gross_sqft_col] = safe_numeric(df_bldg[gross_sqft_col])

# 2) Pick rooms DF: prefer FCLT_ROOMS then FAC_ROOMS
df_rooms = None
rooms_label = None
rooms_bldg_key_col = None
room_col = None
org_col = None

if isinstance(tables.get("table_7"), pd.DataFrame):
    tmp = tables["table_7"]
    if all(c in tmp.columns for c in ["FCLT_BUILDING_KEY", "ROOM", "FCLT_ORGANIZATION_KEY"]):
        df_rooms = tmp.copy()
        rooms_label = "FCLT_ROOMS"
        rooms_bldg_key_col = "FCLT_BUILDING_KEY"
        room_col = "ROOM"
        org_col = "FCLT_ORGANIZATION_KEY"

if df_rooms is None and isinstance(tables.get("table_10"), pd.DataFrame):
    tmp = tables["table_10"]
    if all(c in tmp.columns for c in ["BUILDING_KEY", "ROOM", "ORGANIZATION_KEY"]):
        df_rooms = tmp.copy()
        rooms_label = "FAC_ROOMS"
        rooms_bldg_key_col = "BUILDING_KEY"
        room_col = "ROOM"
        org_col = "ORGANIZATION_KEY"

assert df_rooms is not None, "No suitable rooms table found."

# 3) Aggregate rooms and orgs per building
grp_rooms = (
    df_rooms.groupby(rooms_bldg_key_col)
    .agg(
        rooms_per_building=(room_col, pd.Series.nunique),
        orgs_per_building=(org_col, pd.Series.nunique),
    )
    .reset_index()
)

# 4) Merge to buildings; align keys if possible, else leave counts as 0 (replicating reference behavior)
if bldg_key_col == rooms_bldg_key_col:
    df_bldg_enriched = df_bldg.merge(grp_rooms, how="left", left_on=bldg_key_col, right_on=rooms_bldg_key_col)
elif rooms_bldg_key_col in df_bldg.columns:
    df_bldg_enriched = df_bldg.merge(grp_rooms, how="left", on=rooms_bldg_key_col)
else:
    df_bldg_enriched = df_bldg.copy()
    df_bldg_enriched["rooms_per_building"] = pd.NA
    df_bldg_enriched["orgs_per_building"] = pd.NA

df_bldg_enriched["rooms_per_building"] = pd.to_numeric(df_bldg_enriched["rooms_per_building"], errors="coerce").fillna(0).astype(int)
df_bldg_enriched["orgs_per_building"] = pd.to_numeric(df_bldg_enriched["orgs_per_building"], errors="coerce").fillna(0).astype(int)

# 5) Group by OWNERSHIP_TYPE, BUILDING_USE
grp_cols = ["OWNERSHIP_TYPE", "BUILDING_USE"]
grouped = (
    df_bldg_enriched.groupby(grp_cols, dropna=False)
    .agg(
        building_count=(bldg_key_col, pd.Series.nunique),
        gross_sqft=(gross_sqft_col, "sum"),
        rooms_total=("rooms_per_building", "sum"),
        orgs_total=("orgs_per_building", "sum"),
    )
    .reset_index()
)

# 6) Subtotals per OWNERSHIP_TYPE
subtotals = (
    grouped.groupby("OWNERSHIP_TYPE", dropna=False)
    .agg(
        building_count=("building_count", "sum"),
        gross_sqft=("gross_sqft", "sum"),
        rooms_total=("rooms_total", "sum"),
        orgs_total=("orgs_total", "sum"),
    )
    .reset_index()
)
subtotals["BUILDING_USE"] = "Subtotal"

# 7) Grand total
grand_total = pd.DataFrame({
    "OWNERSHIP_TYPE": ["Grand Total"],
    "BUILDING_USE": [""],
    "building_count": [grouped["building_count"].sum()],
    "gross_sqft": [grouped["gross_sqft"].sum()],
    "rooms_total": [grouped["rooms_total"].sum()],
    "orgs_total": [grouped["orgs_total"].sum()],
})

# 8) Sort and interleave subtotals
grouped_sorted = grouped.sort_values(["OWNERSHIP_TYPE", "BUILDING_USE"]).reset_index(drop=True)

out_parts = []
for own_type, df_part in grouped_sorted.groupby("OWNERSHIP_TYPE", sort=False, dropna=False):
    out_parts.append(df_part)
    out_parts.append(subtotals[subtotals["OWNERSHIP_TYPE"] == own_type])

final_df = pd.concat(out_parts + [grand_total], ignore_index=True)

# 9) Format gross_sqft as rounded integers with thousands separators
def fmt_int_thousands(x):
    try:
        return f"{int(round(x)):,}"
    except Exception:
        return ""

final_df["gross_sqft"] = final_df["gross_sqft"].apply(fmt_int_thousands)

# 10) Suppress repeating OWNERSHIP_TYPE per consecutive rows, and blank out subtotal/grand total ownership/use per instructions
def suppress_repeats(series: pd.Series) -> pd.Series:
    prev = None
    result = []
    for val in series:
        if val == "Grand Total":
            result.append(val)
            prev = val
            continue
        if val == prev:
            result.append("")
        else:
            result.append(val)
            prev = val
    return pd.Series(result, index=series.index)

final_df["OWNERSHIP_TYPE"] = suppress_repeats(final_df["OWNERSHIP_TYPE"])

# Per guideline: subtotal and grand total rows should not include ownership type and usage type
is_subtotal = final_df["BUILDING_USE"].eq("Subtotal")
is_grand_total = final_df["OWNERSHIP_TYPE"].eq("Grand Total")
final_df.loc[is_subtotal | is_grand_total, "OWNERSHIP_TYPE"] = ""
final_df.loc[is_subtotal | is_grand_total, "BUILDING_USE"] = ""

# Order columns
final_df = final_df[["OWNERSHIP_TYPE", "BUILDING_USE", "building_count", "gross_sqft", "rooms_total", "orgs_total"]]

# Package result
result = {"ownership_usage_summary": final_df}