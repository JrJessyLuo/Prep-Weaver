import pandas as pd

# Helpers
def to_str_series(s):
    return s.astype(str).str.strip()

# Source tables from provided dict `tables`
SPACE_DETAIL = tables['table_1'].copy()
BUILDINGS = tables['table_3'].copy()
FCLT_ROOMS = tables['table_4'].copy()
FAC_ROOMS = tables['table_5'].copy()
SPACE_FLOOR = tables['table_9'].copy()
SPACE_USAGE = tables['table_10'].copy()

# Normalize keys to string
SPACE_DETAIL["BUILDING_KEY_str"] = to_str_series(SPACE_DETAIL["BUILDING_KEY"])
SPACE_DETAIL["FLOOR_KEY_str"] = to_str_series(SPACE_DETAIL["FLOOR_KEY"])
SPACE_DETAIL["SPACE_USAGE_KEY_str"] = to_str_series(SPACE_DETAIL["SPACE_USAGE_KEY"])

BUILDINGS["BUILDING_KEY_str"] = to_str_series(BUILDINGS["BUILDING_KEY"])

SPACE_FLOOR["FLOOR_KEY_str"] = to_str_series(SPACE_FLOOR["FLOOR_KEY"])

SPACE_USAGE["space_usage_key_str"] = to_str_series(SPACE_USAGE["space_usage_key"])

# Target building key
target_building_key = "36"

# Filter SPACE_DETAIL to target building
sd_b36 = SPACE_DETAIL[SPACE_DETAIL["BUILDING_KEY_str"] == target_building_key].copy()

# Enrich with floor name (FLOOR and FLOOR_NAME)
sd_b36 = sd_b36.merge(
    SPACE_FLOOR[["FLOOR_KEY_str", "FLOOR", "FLOOR_NAME"]],
    on="FLOOR_KEY_str",
    how="left"
)

# Enrich with SPACE_USAGE text
sd_b36 = sd_b36.merge(
    SPACE_USAGE[["space_usage_key_str", "SPACE_USAGE"]].rename(columns={"space_usage_key_str": "SPACE_USAGE_KEY_str"}),
    on="SPACE_USAGE_KEY_str",
    how="left"
)

# Attach building info (BUILDING_NAME and BUILDING_STREET_ADDRESS)
bldg_cols_available = [c for c in ["BUILDING_KEY", "BUILDING_NUMBER", "BUILDING_NAME", "BUILDING_STREET_ADDRESS", "BLDG_GROSS_SQUARE_FOOTAGE", "BLDG_ASSIGNABLE_SQUARE_FOOTAGE"] if c in BUILDINGS.columns]
bldg_36_info = BUILDINGS[BUILDINGS["BUILDING_KEY_str"] == target_building_key][bldg_cols_available + ["BUILDING_KEY_str"]].drop_duplicates()

sd_b36 = sd_b36.merge(
    bldg_36_info.drop_duplicates(subset=["BUILDING_KEY_str"]),
    on="BUILDING_KEY_str",
    how="left",
    suffixes=("", "_BLDG")
)

# Compute per (BUILDING_KEY, FLOOR_KEY) counts:
# - distinct SPACE_UNIT_KEY from SPACE_DETAIL (within building 36)
# - distinct ORGANIZATION_KEY from FAC_ROOMS for same building and floor
spaceunit_counts = (
    sd_b36.groupby(["BUILDING_KEY_str", "FLOOR_KEY_str"])["SPACE_UNIT_KEY"]
    .nunique(dropna=True)
    .reset_index(name="distinct_SPACE_UNIT_KEY_cnt")
)

# Prepare FAC_ROOMS distinct org counts
FAC_ROOMS["_BUILDING_KEY_str"] = to_str_series(FAC_ROOMS["BUILDING_KEY"])
FAC_ROOMS["_FLOOR_str"] = to_str_series(FAC_ROOMS["FLOOR"])
org_counts = (
    FAC_ROOMS
    .groupby(["_BUILDING_KEY_str", "_FLOOR_str"])["ORGANIZATION_KEY"]
    .nunique(dropna=True)
    .reset_index()
    .rename(columns={
        "_BUILDING_KEY_str": "BUILDING_KEY_str",
        "_FLOOR_str": "FLOOR_KEY_str",
        "ORGANIZATION_KEY": "distinct_ORGANIZATION_KEY_cnt"
    })
)

# Merge counts back to sd_b36
sd_b36 = sd_b36.merge(spaceunit_counts, on=["BUILDING_KEY_str", "FLOOR_KEY_str"], how="left")
sd_b36 = sd_b36.merge(org_counts, on=["BUILDING_KEY_str", "FLOOR_KEY_str"], how="left")

# Arrange final columns per question:
# For building 36, list all space units, their floor and building name, building street address, their space usage,
# and the number of organizations and space units on the same building and floor.
final_cols = [
    "SPACE_UNIT_KEY",
    "FLOOR", "FLOOR_NAME",
    "BUILDING_NAME", "BUILDING_STREET_ADDRESS",
    "SPACE_USAGE",
    "distinct_ORGANIZATION_KEY_cnt",
    "distinct_SPACE_UNIT_KEY_cnt"
]
final_cols = [c for c in final_cols if c in sd_b36.columns]

answer_df = (
    sd_b36[final_cols]
    .drop_duplicates()
    .sort_values(by=["FLOOR", "SPACE_UNIT_KEY"], kind="stable")
    .reset_index(drop=True)
)

result = {"building_36_space_units_with_counts": answer_df}