import pandas as pd
import re

# The input tables are provided in a dict named `tables`
# tables['table_1'] -> FCLT_BUILDING_HIST.pkl
# tables['table_2'] -> FCLT_BUILDING_HIST_1.pkl
# tables['table_3'] -> FAC_BUILDING.pkl
# tables['table_4'] -> FCLT_BUILDING.pkl
# tables['table_5'] -> BUILDINGS.pkl
# tables['table_6'] -> DRUPAL_EMPLOYEE_DIRECTORY.pkl
# tables['table_7'] -> FCLT_BUILDING_ADDRESS_HIST.pkl
# tables['table_8'] -> EMPLOYEE_DIRECTORY.pkl
# tables['table_9'] -> ZPM_ROOMS_LOAD.pkl
# tables['table_10'] -> SPACE_DETAIL.pkl

# ------------------------------------------------------------
# Load DataFrames from provided `tables` mapping
# ------------------------------------------------------------
df_hist = tables.get('table_1')
df_hist_1 = tables.get('table_2')
df_fac_building = tables.get('table_3')
df_fclt_building = tables.get('table_4')
df_buildings = tables.get('table_5')
df_drupal_emp = tables.get('table_6')
df_emp_dir = tables.get('table_8')
df_addr_hist = tables.get('table_7')
df_zpm = tables.get('table_9')
df_space = tables.get('table_10')

# Choose a canonical FCLT building dimension (non-historical) for core attributes
dim_bldg = None
if isinstance(df_fclt_building, pd.DataFrame):
    dim_bldg = df_fclt_building.copy()
elif isinstance(df_fac_building, pd.DataFrame):
    dim_bldg = df_fac_building.copy()

# ------------------------------------------------------------
# Utility to extract building number from office location-like strings
# ------------------------------------------------------------
def extract_building_number_from_office_location(series: pd.Series) -> pd.Series:
    s = series.fillna("").astype(str).str.strip()
    bldg = s.str.extract(r"^\s*([A-Za-z]*\d+)\s*-\s*")[0]
    bldg = bldg.fillna(s.str.extract(r"^\s*([A-Za-z]*\d+)\s*[–-]\s*")[0])
    bldg = bldg.fillna("").str.upper().str.strip()
    bldg = bldg.replace({"": pd.NA})
    return bldg

def count_employees_by_building(emp_df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    df = emp_df.copy()
    if "OFFICE_LOCATION" not in df.columns:
        return pd.DataFrame(columns=["BUILDING_NUMBER", "EMPLOYEE_COUNT", "SOURCE"])
    df["BUILDING_NUMBER"] = extract_building_number_from_office_location(df["OFFICE_LOCATION"])
    id_col = None
    for c in ["MIT_ID", "EMAIL_ADDRESS", "EMAIL_ADDRESS_UPPERCASE", "krb_name", "KRB_NAME_UPPERCASE"]:
        if c in df.columns:
            id_col = c
            break
    if id_col is None:
        grp = df.dropna(subset=["BUILDING_NUMBER"])\
                .groupby("BUILDING_NUMBER", dropna=True).size().reset_index(name="EMPLOYEE_COUNT")
    else:
        grp = (df.dropna(subset=["BUILDING_NUMBER"])
                 .drop_duplicates(subset=[id_col, "BUILDING_NUMBER"])
                 .groupby("BUILDING_NUMBER", dropna=True)[id_col]
                 .nunique()
                 .reset_index(name="EMPLOYEE_COUNT"))
    grp["SOURCE"] = source_name
    return grp

# ------------------------------------------------------------
# Build inferred employee counts from EMPLOYEE_DIRECTORY and DRUPAL_EMPLOYEE_DIRECTORY
# ------------------------------------------------------------
emp_counts = []
if isinstance(df_emp_dir, pd.DataFrame):
    emp_counts.append(count_employees_by_building(df_emp_dir, "EMPLOYEE_DIRECTORY"))
if isinstance(df_drupal_emp, pd.DataFrame):
    emp_counts.append(count_employees_by_building(df_drupal_emp, "DRUPAL_EMPLOYEE_DIRECTORY"))

emp_counts = [g for g in emp_counts if isinstance(g, pd.DataFrame) and len(g) > 0]
if emp_counts:
    emp_counts_all = pd.concat(emp_counts, ignore_index=True)
    emp_counts_pivot = emp_counts_all.pivot_table(
        index="BUILDING_NUMBER", columns="SOURCE", values="EMPLOYEE_COUNT", aggfunc="max"
    )
    emp_counts_pivot["EMPLOYEE_COUNT_BEST"] = emp_counts_pivot.max(axis=1, numeric_only=True)
    emp_counts_best = emp_counts_pivot.reset_index()
else:
    emp_counts_best = pd.DataFrame(columns=["BUILDING_NUMBER", "EMPLOYEE_COUNT_BEST"])

# ------------------------------------------------------------
# Prepare building dimension with long name and built year (DATE_BUILT present per reference run)
# ------------------------------------------------------------
dim = None
if isinstance(dim_bldg, pd.DataFrame):
    dim = dim_bldg.copy()
elif isinstance(df_fac_building, pd.DataFrame):
    dim = df_fac_building.copy()

if isinstance(dim, pd.DataFrame):
    cols = list(dim.columns)
    keep_cols = []
    for c in ["FCLT_BUILDING_KEY", "FAC_BUILDING_KEY", "BUILDING_NUMBER",
              "PARENT_BUILDING_NUMBER", "PARENT_BUILDING_NAME",
              "PARENT_BUILDING_NAME_LONG", "BUILDING_NAME_LONG", "DATE_BUILT"]:
        if c in cols and c not in keep_cols:
            keep_cols.append(c)
    dim_small = dim[keep_cols].drop_duplicates()
else:
    dim_small = pd.DataFrame(columns=["BUILDING_NUMBER", "BUILDING_NAME_LONG", "DATE_BUILT"])

# ------------------------------------------------------------
# Join inferred employee counts to building dimension
# ------------------------------------------------------------
if "BUILDING_NUMBER" in dim_small.columns and "BUILDING_NUMBER" in emp_counts_best.columns:
    bldg_with_counts = dim_small.merge(emp_counts_best, on="BUILDING_NUMBER", how="left")
else:
    bldg_with_counts = dim_small.copy()
    bldg_with_counts["EMPLOYEE_COUNT_BEST"] = pd.NA

# ------------------------------------------------------------
# Filter: constructed before 1950 and more than 100 employees
# ------------------------------------------------------------
# Coerce DATE_BUILT to numeric if present
if "DATE_BUILT" in bldg_with_counts.columns:
    bldg_with_counts["DATE_BUILT_NUM"] = pd.to_numeric(bldg_with_counts["DATE_BUILT"], errors="coerce")
else:
    bldg_with_counts["DATE_BUILT_NUM"] = pd.NA

bldg_with_counts["EMPLOYEE_COUNT_BEST_NUM"] = pd.to_numeric(bldg_with_counts["EMPLOYEE_COUNT_BEST"], errors="coerce")

filtered = bldg_with_counts[
    (bldg_with_counts["DATE_BUILT_NUM"].notna()) &
    (bldg_with_counts["DATE_BUILT_NUM"] < 1950) &
    (bldg_with_counts["EMPLOYEE_COUNT_BEST_NUM"] > 100)
]

answer_cols = []
if "BUILDING_NAME_LONG" in filtered.columns:
    answer_cols.append("BUILDING_NAME_LONG")
elif "PARENT_BUILDING_NAME_LONG" in filtered.columns:
    answer_cols.append("PARENT_BUILDING_NAME_LONG")
else:
    # Fallback to any name-like column if available
    name_like = [c for c in filtered.columns if "NAME" in c.upper()]
    if name_like:
        answer_cols.append(name_like[0])

# Ensure we include year built and employee count and building number for clarity
for c in ["DATE_BUILT_NUM", "EMPLOYEE_COUNT_BEST_NUM", "BUILDING_NUMBER"]:
    if c in filtered.columns and c not in answer_cols:
        answer_cols.append(c)

final_answer = filtered[answer_cols].drop_duplicates().sort_values(
    by=["EMPLOYEE_COUNT_BEST_NUM", "DATE_BUILT_NUM"], ascending=[False, True]
)

# Rename columns to match the question phrasing
rename_map = {}
if "BUILDING_NAME_LONG" in final_answer.columns:
    rename_map["BUILDING_NAME_LONG"] = "Building Long Name"
if "PARENT_BUILDING_NAME_LONG" in final_answer.columns:
    rename_map["PARENT_BUILDING_NAME_LONG"] = "Building Long Name"
if "DATE_BUILT_NUM" in final_answer.columns:
    rename_map["DATE_BUILT_NUM"] = "Year Built"
if "EMPLOYEE_COUNT_BEST_NUM" in final_answer.columns:
    rename_map["EMPLOYEE_COUNT_BEST_NUM"] = "Employee Count"
if "BUILDING_NUMBER" in final_answer.columns:
    rename_map["BUILDING_NUMBER"] = "Building Number"

final_answer = final_answer.rename(columns=rename_map)
preferred_order = [c for c in ["Building Long Name", "Year Built", "Employee Count", "Building Number"] if c in final_answer.columns]
final_answer = final_answer[preferred_order]

# Package result
result = {
    "buildings_pre1950_over100_employees": final_answer.reset_index(drop=True)
}