import pandas as pd
import numpy as np

df = tables["table_2"].copy() if "table_2" in tables else tables["table_1"].copy()

def is_null_like(s):
    return s.isna() | s.astype(str).str.strip().str.upper().isin(["", "(NULL)", "NULL", "NAN", "NONE"])

owned = df["OWNERSHIP_TYPE"].astype(str).str.strip().str.upper().eq("OWNED")
not_subdivision = is_null_like(df["PARENT_BUILDING_NUMBER"])
if "BUILDING_TYPE" in df.columns:
    not_subdivision &= ~df["BUILDING_TYPE"].astype(str).str.strip().str.upper().eq("SUBDIVISION")

work = df.loc[owned & not_subdivision].copy()
work = work.drop_duplicates(subset=["BUILDING_NUMBER"])

work["construction_start_dt"] = pd.to_datetime(work["DATE_BUILT"], errors="coerce")
work["initial_occupancy_dt"] = pd.to_datetime(work["DATE_OCCUPIED"], errors="coerce")

work["construction_start_year_full"] = work["construction_start_dt"].dt.year.astype("Int64").astype(str)
work.loc[work["construction_start_dt"].isna(), "construction_start_year_full"] = "UNKNOWN"

work["year_of_initial_occupancy"] = work["initial_occupancy_dt"].dt.year.astype("Int64").astype(str)
work.loc[work["initial_occupancy_dt"].isna(), "year_of_initial_occupancy"] = "UNKNOWN"

work["sort_year"] = work["construction_start_dt"].dt.year
work["sort_year_missing"] = work["sort_year"].isna()
work["sort_building"] = work.get("BUILDING_SORT", work["BUILDING_NUMBER"]).astype(str)

work = work.sort_values(
    ["sort_year_missing", "sort_year", "sort_building", "BUILDING_NUMBER"],
    kind="mergesort"
).reset_index(drop=True)

work["construction_start_year"] = work["construction_start_year_full"]
work.loc[
    work["construction_start_year_full"].eq(work["construction_start_year_full"].shift()),
    "construction_start_year"
] = ""

out = work[[
    "construction_start_year",
    "BUILDING_NUMBER",
    "year_of_initial_occupancy"
]].rename(columns={
    "BUILDING_NUMBER": "building_number"
})

total_row = pd.DataFrame([{
    "construction_start_year": None,
    "building_number": f"{len(work)} Buildings",
    "year_of_initial_occupancy": None
}])

out = pd.concat([out, total_row], ignore_index=True)

result = {"owned_non_subdivision_buildings": out}
