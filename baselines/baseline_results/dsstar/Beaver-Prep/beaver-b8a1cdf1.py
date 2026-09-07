import os
import pandas as pd
import numpy as np

# Inputs already loaded in 'tables'
fac_rooms = tables['table_5'].copy()

# Expect a STATA_BUILDING_KEY to identify Stata building
STATA_BUILDING_KEY = os.environ.get("STATA_BUILDING_KEY", "").strip()
if not STATA_BUILDING_KEY:
    raise ValueError(
        "Please provide the Stata building BUILDING_KEY via environment variable STATA_BUILDING_KEY."
    )

# Filter to Stata building
fac_rooms["BUILDING_KEY"] = fac_rooms.get("BUILDING_KEY", pd.Series(index=fac_rooms.index, dtype=object)).astype(str)
stata_rooms = fac_rooms[fac_rooms["BUILDING_KEY"].astype(str) == STATA_BUILDING_KEY].copy()

# Exclude records where MAJOR_USE_DESC or MINOR_USE_DESC contains 'STORAGE'
mask_major_storage = stata_rooms.get("MAJOR_USE_DESC", pd.Series(index=stata_rooms.index, dtype=object)).astype(str).str.contains("STORAGE", case=False, na=False)
minor_use_series = stata_rooms.get("MINOR_USE_DESC", pd.Series(index=stata_rooms.index, dtype=object))
mask_minor_storage = minor_use_series.astype(str).str.contains("STORAGE", case=False, na=False)
filtered = stata_rooms[~(mask_major_storage | mask_minor_storage)].copy()

# Build a SPACE_ID -> space name mapping
space_name = filtered.get("ROOM_FULL_NAME", pd.Series(index=filtered.index, dtype=object))
if space_name is None or space_name.empty:
    space_name = pd.Series(index=filtered.index, dtype=object)

space_name = space_name.astype(str)
space_name = space_name.where(~space_name.str.strip().isin(["", "nan", "NaN", "None"]), np.nan)
fallback_room = filtered.get("ROOM", pd.Series(index=filtered.index, dtype=object)).astype(str)
fallback_room = fallback_room.where(~fallback_room.str.strip().isin(["", "nan", "NaN", "None"]), np.nan)
space_id_str = filtered.get("SPACE_ID", pd.Series(index=filtered.index, dtype=object)).astype(str)
space_id_str = space_id_str.where(~space_id_str.str.strip().isin(["", "nan", "NaN", "None"]), "UNKNOWN_SPACE_ID")
final_space_name = space_name.fillna(fallback_room).fillna(space_id_str)

filtered = filtered.assign(SPACE_NAME=final_space_name)

# Ensure numeric AREA
if "AREA" in filtered.columns:
    filtered["AREA"] = pd.to_numeric(filtered["AREA"], errors="coerce")
else:
    filtered["AREA"] = np.nan

# Ensure MAJOR_USE_DESC exists
if "MAJOR_USE_DESC" not in filtered.columns:
    filtered["MAJOR_USE_DESC"] = "UNKNOWN"

# Ensure ACCESS_LEVEL exists
if "ACCESS_LEVEL" not in filtered.columns:
    filtered["ACCESS_LEVEL"] = np.nan

# Ensure SPACE_ID exists (string for grouping)
if "SPACE_ID" not in filtered.columns:
    filtered["SPACE_ID"] = "UNKNOWN_SPACE_ID"
else:
    filtered["SPACE_ID"] = filtered["SPACE_ID"].astype(str).where(
        ~filtered["SPACE_ID"].astype(str).str.strip().isin(["", "nan", "NaN", "None"]),
        "UNKNOWN_SPACE_ID"
    )

# Prepare the base aggregation by space
group_cols = ["ACCESS_LEVEL", "MAJOR_USE_DESC", "SPACE_ID", "SPACE_NAME"]
agg_df = (
    filtered.groupby(group_cols, dropna=False)
    .agg(
        rooms_count=("SPACE_ID", "size"),
        total_area=("AREA", "sum"),
        avg_area=("AREA", "mean"),
    )
    .reset_index()
)

# Sort for readability
agg_df = agg_df.sort_values(by=["ACCESS_LEVEL", "MAJOR_USE_DESC", "SPACE_NAME"]).reset_index(drop=True)

# Helper: format numbers as integers with commas
def fmt_int(x):
    if pd.isna(x):
        return ""
    try:
        return f"{int(round(x)):,}"
    except Exception:
        return ""

# Build hierarchical report with subtotals:
# Levels:
# - Detail rows: by ACCESS_LEVEL, MAJOR_USE_DESC, SPACE_NAME (SPACE_ID collapsed within)
# - Subtotal by (ACCESS_LEVEL, MAJOR_USE_DESC)
# - Subtotal by ACCESS_LEVEL
# - Grand total
report_rows = []

# Compute detail rows per unique (ACCESS_LEVEL, MAJOR_USE_DESC, SPACE_NAME)
detail_group_cols = ["ACCESS_LEVEL", "MAJOR_USE_DESC", "SPACE_NAME"]
detail = (
    agg_df.groupby(detail_group_cols, dropna=False)
    .agg(
        rooms_count=("rooms_count", "sum"),
        total_area=("total_area", "sum"),
        avg_area=("avg_area", "mean"),  # average of averages; alternative could be weighted but spec doesn't require
    )
    .reset_index()
).sort_values(detail_group_cols).reset_index(drop=True)

# Compute subtotals per (ACCESS_LEVEL, MAJOR_USE_DESC)
sub_mu = (
    detail.groupby(["ACCESS_LEVEL", "MAJOR_USE_DESC"], dropna=False)
    .agg(
        rooms_count=("rooms_count", "sum"),
        total_area=("total_area", "sum"),
        avg_area=("avg_area", "mean"),
    )
    .reset_index()
)

# Compute subtotals per ACCESS_LEVEL
sub_al = (
    detail.groupby(["ACCESS_LEVEL"], dropna=False)
    .agg(
        rooms_count=("rooms_count", "sum"),
        total_area=("total_area", "sum"),
        avg_area=("avg_area", "mean"),
    )
    .reset_index()
)

# Grand total
grand = pd.DataFrame({
    "rooms_count": [detail["rooms_count"].sum()],
    "total_area": [detail["total_area"].sum()],
    "avg_area": [detail["avg_area"].mean()]
})

# Assemble the report with "display access level only if differs from previous"
prev_access_level = None

# Iterate access levels in sorted order as they appear in detail
for access_level, df_al in detail.groupby("ACCESS_LEVEL", dropna=False):
    # Within access level, iterate usage types
    for mu, df_mu in df_al.groupby("MAJOR_USE_DESC", dropna=False):
        # Detail rows (space-level)
        for _, r in df_mu.sort_values("SPACE_NAME").iterrows():
            disp_access = "" if prev_access_level == access_level else ("" if pd.isna(access_level) else str(access_level))
            report_rows.append({
                "Access Level": disp_access,
                "Usage Type": "" if pd.isna(mu) else str(mu),
                "Space Name": "" if pd.isna(r["SPACE_NAME"]) else str(r["SPACE_NAME"]),
                "Number of Spaces": fmt_int(r["rooms_count"]),
                "Total Area": fmt_int(r["total_area"]),
                "Average Area": fmt_int(r["avg_area"]),
                "Row Type": "Detail"
            })
            prev_access_level = access_level
        # Subtotal for Access+Usage
        mu_sub = sub_mu[(sub_mu["ACCESS_LEVEL"].astype(object) == access_level) & (sub_mu["MAJOR_USE_DESC"].astype(object) == mu)].iloc[0]
        report_rows.append({
            "Access Level": "",  # keep compact
            "Usage Type": f"{'' if pd.isna(mu) else str(mu)} — Subtotal",
            "Space Name": "",
            "Number of Spaces": fmt_int(mu_sub["rooms_count"]),
            "Total Area": fmt_int(mu_sub["total_area"]),
            "Average Area": fmt_int(mu_sub["avg_area"]),
            "Row Type": "Subtotal: Access+Usage"
        })
    # Subtotal for Access Level
    al_sub = sub_al[sub_al["ACCESS_LEVEL"].astype(object) == access_level].iloc[0]
    report_rows.append({
        "Access Level": "",  # not repeated
        "Usage Type": "Subtotal (Access Level)",
        "Space Name": "",
        "Number of Spaces": fmt_int(al_sub["rooms_count"]),
        "Total Area": fmt_int(al_sub["total_area"]),
        "Average Area": fmt_int(al_sub["avg_area"]),
        "Row Type": "Subtotal: Access"
    })

# Grand total row
report_rows.append({
    "Access Level": "",
    "Usage Type": "Grand Total",
    "Space Name": "",
    "Number of Spaces": fmt_int(grand.iloc[0]["rooms_count"]),
    "Total Area": fmt_int(grand.iloc[0]["total_area"]),
    "Average Area": fmt_int(grand.iloc[0]["avg_area"]),
    "Row Type": "Grand Total"
})

report_df = pd.DataFrame(report_rows, columns=[
    "Access Level", "Usage Type", "Space Name",
    "Number of Spaces", "Total Area", "Average Area", "Row Type"
])

# Assign final answer
result = {
    "Stata Spaces by Access and Usage with Subtotals": report_df
}