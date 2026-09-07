import pandas as pd
import numpy as np
import re

# The `tables` dict with DataFrames is assumed to be already in scope per the guidelines.

# Source tables per mapping
fclt_bldg = tables['table_6'].copy()  # FCLT_BUILDING.pkl
emp = tables['table_10'].copy()       # DRUPAL_EMPLOYEE_DIRECTORY.pkl
addr = tables['table_5'].copy()       # FCLT_BUILDING_ADDRESS.pkl

# Helper functions (from reference approach, adapted)
def extract_building_number_from_office_location(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    s = s.replace("–", "-").replace("—", "-")
    if "-" in s:
        left = s.split("-", 1)[0].strip()
        left = re.sub(r"[^A-Za-z0-9]+$", "", left)
        return left if left else None
    m = re.match(r"^([A-Za-z0-9]+)", s)
    return m.group(1) if m else None

def norm_bldg_num(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    s = s.replace("–", "-").replace("—", "-")
    return s.upper()

# Normalize building numbers in buildings table
if "BUILDING_NUMBER" in fclt_bldg.columns:
    fclt_bldg["BUILDING_NUMBER_NORM"] = fclt_bldg["BUILDING_NUMBER"].apply(norm_bldg_num)
else:
    fclt_bldg["BUILDING_NUMBER_NORM"] = None

# Determine subdivision flag if available; otherwise default to False (not a subdivision)
subdiv_col_candidates = [c for c in fclt_bldg.columns if c.upper() in ("IS_SUBDIVISION", "SUBDIVISION", "SUBDIVISION_FLAG", "IS_SUBDIVIDED")]
if subdiv_col_candidates:
    subcol = subdiv_col_candidates[0]
    # Normalize to boolean: treat truthy-like as True, else False
    fclt_bldg["_IS_SUBDIVISION"] = fclt_bldg[subcol].astype(str).str.upper().isin(
        ["1", "Y", "YES", "TRUE", "T"]
    )
else:
    fclt_bldg["_IS_SUBDIVISION"] = False

# Parse and normalize employee office building numbers
emp = emp.copy()
emp["OFFICE_BUILDING_NUMBER"] = emp["OFFICE_LOCATION"].apply(extract_building_number_from_office_location)
emp["OFFICE_BUILDING_NUMBER_NORM"] = emp["OFFICE_BUILDING_NUMBER"].apply(lambda x: norm_bldg_num(x) if pd.notna(x) else None)

# Employee counts per building number
emp_counts = (
    emp.dropna(subset=["OFFICE_BUILDING_NUMBER_NORM"])
       .groupby("OFFICE_BUILDING_NUMBER_NORM")
       .size()
       .reset_index(name="EMPLOYEE_COUNT")
)

# Prepare building subset with needed fields
bldg_keep_cols = [
    "FCLT_BUILDING_KEY",
    "BUILDING_NUMBER",
    "BUILDING_NUMBER_NORM",
    "BUILDING_NAME_LONG",
    "BUILDING_TYPE",
    "EXT_GROSS_AREA",
    "ASSIGNABLE_AREA",
    "NON_ASSIGNABLE_AREA",
    "_IS_SUBDIVISION",
]
bldg_subset = fclt_bldg.loc[:, [c for c in bldg_keep_cols if c in fclt_bldg.columns]].copy()

# Join employee counts to buildings on normalized number
bldg_with_counts = pd.merge(
    bldg_subset,
    emp_counts,
    left_on="BUILDING_NUMBER_NORM",
    right_on="OFFICE_BUILDING_NUMBER_NORM",
    how="left"
).drop(columns=["OFFICE_BUILDING_NUMBER_NORM"])

# Bring in address data: assume standard fields exist; if not, create empties
addr_cols_map = {
    "FCLT_BUILDING_KEY": "FCLT_BUILDING_KEY",
    "STREET_ADDRESS": None,
    "CITY": None,
    "STATE": None,
    "POSTAL_CODE": None
}
addr_df = addr.copy()
# Identify likely columns for address fields if exact names differ
def find_col(df, options):
    for o in options:
        if o in df.columns:
            return o
    return None

if "STREET_ADDRESS" not in addr_df.columns:
    cand = find_col(addr_df, ["ADDRESS_LINE1","ADDRESS1","ADDR_LINE1","STREET","ADDRESS"])
    if cand is not None:
        addr_df = addr_df.rename(columns={cand: "STREET_ADDRESS"})
    else:
        addr_df["STREET_ADDRESS"] = pd.NA

if "CITY" not in addr_df.columns:
    cand = find_col(addr_df, ["CITY_NAME","ADDR_CITY"])
    if cand is not None:
        addr_df = addr_df.rename(columns={cand: "CITY"})
    else:
        addr_df["CITY"] = pd.NA

if "STATE" not in addr_df.columns:
    cand = find_col(addr_df, ["STATE_CODE","STATE_PROVINCE","ADDR_STATE"])
    if cand is not None:
        addr_df = addr_df.rename(columns={cand: "STATE"})
    else:
        addr_df["STATE"] = pd.NA

if "POSTAL_CODE" not in addr_df.columns:
    cand = find_col(addr_df, ["ZIP","ZIP_CODE","POSTAL","POSTALCODE","ADDR_ZIP"])
    if cand is not None:
        addr_df = addr_df.rename(columns={cand: "POSTAL_CODE"})
    else:
        addr_df["POSTAL_CODE"] = pd.NA

addr_keep = ["FCLT_BUILDING_KEY","STREET_ADDRESS","CITY","STATE","POSTAL_CODE"]
addr_keep = [c for c in addr_keep if c in addr_df.columns]
addr_subset = addr_df.loc[:, addr_keep].copy()

# If multiple addresses per building, choose one; for uniqueness counts later, we will deduplicate on values per type
# For now, merge and keep all (for unique value counts we can groupby)
bldg_addr = pd.merge(
    bldg_with_counts,
    addr_subset,
    on="FCLT_BUILDING_KEY",
    how="left"
)

# For group-by at building level, collapse addresses per building (unique values per field)
# We'll compute unique counts across buildings within each type, not per address rows.
# First, aggregate addresses to a single row per building with lists of unique values.
agg_addr = (
    bldg_addr.groupby("FCLT_BUILDING_KEY", as_index=False)
    .agg({
        "STREET_ADDRESS": lambda s: tuple(pd.unique(s.dropna())) if "STREET_ADDRESS" in bldg_addr.columns else tuple(),
        "CITY": lambda s: tuple(pd.unique(s.dropna())) if "CITY" in bldg_addr.columns else tuple(),
        "STATE": lambda s: tuple(pd.unique(s.dropna())) if "STATE" in bldg_addr.columns else tuple(),
        "POSTAL_CODE": lambda s: tuple(pd.unique(s.dropna())) if "POSTAL_CODE" in bldg_addr.columns else tuple(),
    })
)

# Merge collapsed address back to unique buildings
bcols_for_unique = [c for c in bldg_with_counts.columns]  # building-level fields once
bldg_unique = pd.merge(
    bldg_with_counts.drop_duplicates(subset=["FCLT_BUILDING_KEY"]),
    agg_addr,
    on="FCLT_BUILDING_KEY",
    how="left"
)

# Define building type normalization: 'resident' -> 'RESIDENTIAL', else upper-case
def norm_bldg_type(x):
    if pd.isna(x):
        return "UNKNOWN"
    s = str(x).strip()
    if s.lower() == "resident":
        return "RESIDENTIAL"
    return s.upper()

bldg_unique["BUILDING_TYPE_NORM"] = bldg_unique["BUILDING_TYPE"].apply(norm_bldg_type) if "BUILDING_TYPE" in bldg_unique.columns else "UNKNOWN"

# Only count buildings that are not subdivisions
bldg_not_sub = bldg_unique.loc[~bldg_unique["_IS_SUBDIVISION"]].copy()

# Prepare metrics per building type
# - number of buildings (not subdivisions)
# - number of employees (sum employee_count across those buildings; missing counts -> 0)
# - number of unique building street address (unique strings across buildings within type)
# - number of unique city
# - number of unique state
# - number of unique postal code
# - average gross square footage per employee: sum(EXT_GROSS_AREA) / sum(EMPLOYEE_COUNT), avoid div by zero

bldg_not_sub["EMPLOYEE_COUNT"] = bldg_not_sub["EMPLOYEE_COUNT"].fillna(0).astype(float)
if "EXT_GROSS_AREA" in bldg_not_sub.columns:
    bldg_not_sub["EXT_GROSS_AREA"] = pd.to_numeric(bldg_not_sub["EXT_GROSS_AREA"], errors="coerce")
else:
    bldg_not_sub["EXT_GROSS_AREA"] = np.nan

# Expand the address tuples into sets at aggregation time
def uniq_count(series_of_tuples):
    vals = set()
    for t in series_of_tuples:
        if isinstance(t, (list, tuple, pd.Series, np.ndarray)):
            for v in t:
                if pd.notna(v):
                    vals.add(v)
        elif pd.notna(t):
            vals.add(t)
    return len(vals)

grp = bldg_not_sub.groupby("BUILDING_TYPE_NORM", dropna=False)

summary = grp.agg(
    BUILDINGS_NOT_SUBDIVISIONS=("FCLT_BUILDING_KEY", "nunique"),
    EMPLOYEES=("EMPLOYEE_COUNT", "sum"),
    GROSS_SF=("EXT_GROSS_AREA", "sum"),
    STREET_TUP=("STREET_ADDRESS", lambda s: tuple(s) if len(s) else tuple()),
    CITY_TUP=("CITY", lambda s: tuple(s) if len(s) else tuple()),
    STATE_TUP=("STATE", lambda s: tuple(s) if len(s) else tuple()),
    POSTAL_TUP=("POSTAL_CODE", lambda s: tuple(s) if len(s) else tuple()),
)

summary["UNIQUE_STREET_ADDRESS"] = summary["STREET_TUP"].apply(uniq_count)
summary["UNIQUE_CITY"] = summary["CITY_TUP"].apply(uniq_count)
summary["UNIQUE_STATE"] = summary["STATE_TUP"].apply(uniq_count)
summary["UNIQUE_POSTAL_CODE"] = summary["POSTAL_TUP"].apply(uniq_count)

summary = summary.drop(columns=["STREET_TUP","CITY_TUP","STATE_TUP","POSTAL_TUP"])

# Average gross square footage per employee
summary["AVG_GROSS_SF_PER_EMPLOYEE"] = summary.apply(
    lambda r: (r["GROSS_SF"] / r["EMPLOYEES"]) if r["EMPLOYEES"] and not pd.isna(r["EMPLOYEES"]) else np.nan,
    axis=1
)

# Prepare grand total row
total = pd.DataFrame({
    "BUILDINGS_NOT_SUBDIVISIONS": [bldg_not_sub["FCLT_BUILDING_KEY"].nunique()],
    "EMPLOYEES": [bldg_not_sub["EMPLOYEE_COUNT"].sum()],
    "GROSS_SF": [bldg_not_sub["EXT_GROSS_AREA"].sum()],
    "UNIQUE_STREET_ADDRESS": [uniq_count(bldg_not_sub["STREET_ADDRESS"])],
    "UNIQUE_CITY": [uniq_count(bldg_not_sub["CITY"])],
    "UNIQUE_STATE": [uniq_count(bldg_not_sub["STATE"])],
    "UNIQUE_POSTAL_CODE": [uniq_count(bldg_not_sub["POSTAL_CODE"])],
}, index=["TOTAL"])

total["AVG_GROSS_SF_PER_EMPLOYEE"] = (total["GROSS_SF"] / total["EMPLOYEES"]).where(total["EMPLOYEES"] != 0, np.nan)

# Combine
final_df = pd.concat([summary, total], axis=0)

# Reorder columns and rename type index to requested display
final_df = final_df.reset_index().rename(columns={
    "index": "BUILDING_TYPE"
})

# Ensure 'RESIDENTIAL' label present where applicable and 'TOTAL' row labeled as such already
# Sort with TOTAL at bottom
final_df = final_df.sort_values(
    by=["BUILDING_TYPE"],
    key=lambda s: s.map(lambda x: "ZZZ" if x == "TOTAL" else x)
).reset_index(drop=True)

# Round numeric fields where appropriate for readability
for c in ["EMPLOYEES","GROSS_SF","AVG_GROSS_SF_PER_EMPLOYEE"]:
    if c in final_df.columns:
        final_df[c] = pd.to_numeric(final_df[c], errors="coerce")

# Assign to result as required
result = {
    "building_type_summary": final_df[
        [
            "BUILDING_TYPE",
            "BUILDINGS_NOT_SUBDIVISIONS",
            "EMPLOYEES",
            "UNIQUE_STREET_ADDRESS",
            "UNIQUE_CITY",
            "UNIQUE_STATE",
            "UNIQUE_POSTAL_CODE",
            "AVG_GROSS_SF_PER_EMPLOYEE",
        ]
    ]
}