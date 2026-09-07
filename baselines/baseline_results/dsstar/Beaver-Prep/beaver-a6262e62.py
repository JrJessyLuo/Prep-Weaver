import pandas as pd
import numpy as np

# Source input tables from provided `tables` dict
fac_org = tables['table_1'].copy()      # FAC_ORGANIZATION.pkl
fac_rooms = tables['table_10'].copy()   # FAC_ROOMS.pkl

# 1) Filter FAC_ORGANIZATION to exclude "Cambridge-MIT Institute"
org = fac_org.loc[fac_org["ORGANIZATION_NAME"] != "Cambridge-MIT Institute"].copy()

# 2) Prepare join keys: organization_key (int) vs FAC_ROOMS.ORGANIZATION_KEY (cast to int)
rooms = fac_rooms.copy()
rooms["ORG_KEY_INT"] = pd.to_numeric(rooms["ORGANIZATION_KEY"], errors="coerce").astype("Int64")
org["ORG_KEY_INT"] = pd.to_numeric(org["organization_key"], errors="coerce").astype("Int64")

# 3) Aggregate rooms per organization: total_area, room_count
agg_rooms = (
    rooms.dropna(subset=["ORG_KEY_INT"])
         .groupby("ORG_KEY_INT", as_index=False)
         .agg(
             total_area=("AREA", "sum"),
             room_count=("ROOM", "count")
         )
)

# 4) Left-join filtered organizations to aggregated rooms on ORG_KEY_INT
joined = org.merge(agg_rooms, on="ORG_KEY_INT", how="left")

# 5) Compute avg_room_area = total_area / room_count
joined["avg_room_area"] = joined["total_area"] / joined["room_count"]

# 6) Format name with indentation by level: level 2 -> 1 leading space, level 3 -> 2 spaces, ... up to 6 -> 5 spaces
def format_name(row):
    lvl = pd.to_numeric(row.get("ORGANIZATION_LEVEL"), errors="coerce")
    lvl = int(lvl) if pd.notna(lvl) else None
    spaces = 0
    if lvl is not None and 2 <= lvl <= 6:
        spaces = lvl - 1
    return (" " * spaces) + str(row.get("ORGANIZATION_NAME", ""))

# 7) Assignable label
assignable_label = np.where(joined["ASSIGNABLE"].astype(str).str.upper().eq("Y"), "ASSIGNABLE", "NON-ASSIGNABLE")

# 8) Round totals and counts to integers and format with commas; compute avg as float (no rounding instruction given, keep as numeric)
#    Also, ensure that NaNs remain as NaN for numeric fields before string formatting
joined["total_area_rounded"] = joined["total_area"].round(0)
joined["room_count_rounded"] = joined["room_count"].round(0)
joined["avg_room_area"] = joined["avg_room_area"]  # keep numeric; no rounding instruction provided

# 9) Build final output DataFrame
out = pd.DataFrame({
    "ORGANIZATION_ID": joined["ORGANIZATION_ID"],
    "ORGANIZATION_NUMBER": joined["ORGANIZATION_NUMBER"],
    "ORGANIZATION_LEVEL": joined["ORGANIZATION_LEVEL"],
    "FORMATTED_NAME": joined.apply(format_name, axis=1),
    "ASSIGNABLE_STATUS": assignable_label,
    "TOTAL_AREA": joined["total_area_rounded"],
    "NUMBER_OF_ROOMS": joined["room_count_rounded"],
    "AVERAGE_ROOM_AREA": joined["avg_room_area"]
})

# 10) Format TOTAL_AREA and NUMBER_OF_ROOMS with commas (as strings). Leave AVERAGE_ROOM_AREA numeric.
def fmt_commas(x):
    if pd.isna(x):
        return None
    try:
        return f"{int(x):,}"
    except Exception:
        return None

out["TOTAL_AREA"] = out["TOTAL_AREA"].apply(fmt_commas)
out["NUMBER_OF_ROOMS"] = out["NUMBER_OF_ROOMS"].apply(fmt_commas)

# 11) Sort for readability: by TOTAL_AREA (numeric sort where possible, descending)
# Convert TOTAL_AREA back to numeric for sorting (ignoring commas), then sort, then drop helper
sort_key = pd.to_numeric(out["TOTAL_AREA"].str.replace(",", "", regex=False), errors="coerce")
out = out.assign(_sort_total_area=sort_key).sort_values("_sort_total_area", ascending=False).drop(columns=["_sort_total_area"])

# 12) Package final answer
result = {
    "organization_room_aggregates_formatted": out
}