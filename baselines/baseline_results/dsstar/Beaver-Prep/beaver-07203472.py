import pandas as pd
import numpy as np

# --- Assume input DataFrames are provided in `tables` dict as per guidelines ---
# Mapping:
# tables['table_1'] -> FCLT_ROOMS.pkl
# tables['table_6'] -> FCLT_BUILDING.pkl
# tables['table_9'] -> BUILDINGS.pkl

# Load from provided tables dict
fclt_rooms = tables['table_1']
fclt_building = tables['table_6']
buildings = tables['table_9']

# --- Utilities ---
def try_cast_numeric_to_str(s: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(s):
        return s.astype("Int64").astype(str)
    return s.astype(str)

def normalize_use(use: pd.Series) -> pd.Series:
    s = use.fillna("").astype(str).str.strip().str.lower()
    s = s.str.replace(r"\s+", " ", regex=True)

    residential_patterns = [
        "residential",
        "residence",
        "housing",
        "dorm",
        "dormitory",
        "apt",
        "apartment",
        "student housing",
        "undergrad housing",
        "graduate housing",
        "family housing",
        "res hall",
        "res hall(s)?",
        "res halls",
        "res life",
        "living",
        "res life housing",
    ]
    pat = r"(" + r"|".join(residential_patterns) + r")"
    is_res = s.str.contains(pat, case=False, regex=True)

    out = s.str.upper()
    out = out.where(~is_res, "RESIDENTIAL")
    return out

# --- Prepare BUILDINGS mapping (BUILDING_KEY -> BLDG_GROSS_SQUARE_FOOTAGE) ---
b_sel = buildings[["BUILDING_KEY", "BLDG_GROSS_SQUARE_FOOTAGE"]].copy()
b_sel["BUILDING_KEY_STD"] = try_cast_numeric_to_str(b_sel["BUILDING_KEY"])
building_sqft_map = (
    b_sel.drop_duplicates(subset=["BUILDING_KEY_STD"])
         .set_index("BUILDING_KEY_STD")["BLDG_GROSS_SQUARE_FOOTAGE"]
)

# --- Prepare FCLT_ROOMS with std building key for join to sqft ---
room_cols_needed = [c for c in ["FCLT_BUILDING_KEY", "FCLT_ROOM_KEY", "FCLT_ORGANIZATION_KEY"] if c in fclt_rooms.columns]
r_sel = fclt_rooms[room_cols_needed].copy()
r_sel["BUILDING_KEY_STD"] = try_cast_numeric_to_str(r_sel["FCLT_BUILDING_KEY"])

# Enrich FCLT_ROOMS with building gross sqft via mapping
r_sel["BLDG_GROSS_SQUARE_FOOTAGE"] = r_sel["BUILDING_KEY_STD"].map(building_sqft_map)

# --- Join FCLT_ROOMS to FCLT_BUILDING on FCLT_BUILDING_KEY to bring in BUILDING_USE ---
fb_cols = ["FCLT_BUILDING_KEY", "BUILDING_USE"]
fb_avail = [c for c in fb_cols if c in fclt_building.columns]
fb = fclt_building[fb_avail].drop_duplicates(subset=["FCLT_BUILDING_KEY"]).copy()

rooms_with_bldg = r_sel.merge(fb, on="FCLT_BUILDING_KEY", how="left")

# Normalize/standardize BUILDING_USE; map residential-related to "RESIDENTIAL"
if "BUILDING_USE" in rooms_with_bldg.columns:
    rooms_with_bldg["BUILDING_USE_STD"] = normalize_use(rooms_with_bldg["BUILDING_USE"])
else:
    rooms_with_bldg["BUILDING_USE_STD"] = pd.NA

# --- Create per-building table with BUILDING_USE, building gross sqft, and set of organizations ---
def set_agg(x):
    return sorted(pd.unique(x.dropna().astype("Int64").astype(str)))

per_building = (
    rooms_with_bldg.groupby(["BUILDING_KEY_STD"], dropna=False)
    .agg(
        BUILDING_USE_STD=("BUILDING_USE_STD", lambda s: next((v for v in s.dropna().unique()), pd.NA)),
        BLDG_GROSS_SQUARE_FOOTAGE=("BLDG_GROSS_SQUARE_FOOTAGE", "first"),
        ORG_SET=("FCLT_ORGANIZATION_KEY", set_agg),
        ORG_COUNT=("FCLT_ORGANIZATION_KEY", lambda s: s.dropna().nunique()),
        ROOM_COUNT=("FCLT_ROOM_KEY", "nunique"),
    )
    .reset_index()
)

# Optional: also keep original BUILDING_USE for reference if present (not needed for final group-by)
if "BUILDING_USE" in rooms_with_bldg.columns:
    per_b_use = (
        rooms_with_bldg.groupby(["BUILDING_KEY_STD"], dropna=False)["BUILDING_USE"]
        .agg(lambda s: next((v for v in s.dropna().unique()), pd.NA))
        .reset_index()
    )
    per_building = per_building.merge(per_b_use, on="BUILDING_KEY_STD", how="left")

# --- Exclude subdivisions when counting distinct buildings ---
# Heuristic: subdivisions often have suffix letters; treat base numeric/primary key as the parent.
# We'll create a "PARENT_KEY" by stripping trailing letters after digits/hyphens/underscores.
# Fallback to the original key if not matched.
bk = per_building["BUILDING_KEY_STD"].fillna("")
parent_key = bk.str.extract(r"^(\d+[A-Za-z\-]*\d*|\d+|\w+)", expand=False)
parent_key = parent_key.fillna(bk)
per_building["PARENT_KEY"] = parent_key

# --- Group by standardized building use ---
by_use = (
    per_building.groupby("BUILDING_USE_STD", dropna=False)
    .agg(
        BUILDING_COUNT=("PARENT_KEY", lambda s: pd.Series(s).nunique()),
        TOTAL_GROSS_SQFT=("BLDG_GROSS_SQUARE_FOOTAGE", "sum"),
        ORG_UNION=("ORG_SET", lambda sets: sorted(set().union(*sets))),
    )
    .reset_index()
)

# Replace <NA> with string "(NULL)" for display consistency with reference code
by_use["BUILDING_USE_STD"] = by_use["BUILDING_USE_STD"].astype(object).where(by_use["BUILDING_USE_STD"].notna(), "(NULL)")

# Compute organization counts from union sets
by_use["ORG_COUNT"] = by_use["ORG_UNION"].apply(lambda s: len(set(s)))

# Select and rename columns per requirements
final = by_use[["BUILDING_USE_STD", "BUILDING_COUNT", "TOTAL_GROSS_SQFT", "ORG_COUNT"]].copy()

# Round to integers and format with commas
for c in ["BUILDING_COUNT", "TOTAL_GROSS_SQFT", "ORG_COUNT"]:
    final[c] = final[c].fillna(0).round(0).astype("Int64")

# Add totals row across all types
total_row = pd.DataFrame({
    "BUILDING_USE_STD": ["TOTAL"],
    "BUILDING_COUNT": [final["BUILDING_COUNT"].sum()],
    "TOTAL_GROSS_SQFT": [final["TOTAL_GROSS_SQFT"].sum()],
    "ORG_COUNT": [final["ORG_COUNT"].sum()]  # number of orgs across types summed; if union desired, compute separately
})

final_with_total = pd.concat([final.sort_values("BUILDING_USE_STD").reset_index(drop=True), total_row], ignore_index=True)

# Format numbers with commas
def fmt_int_commas(x):
    if pd.isna(x):
        return ""
    return f"{int(x):,}"

final_with_total_fmt = final_with_total.copy()
for c in ["BUILDING_COUNT", "TOTAL_GROSS_SQFT", "ORG_COUNT"]:
    final_with_total_fmt[c] = final_with_total_fmt[c].apply(fmt_int_commas)

# Assign to result dict as required
result = {"buildings_by_use": final_with_total_fmt}