import pandas as pd

# The input tables are already loaded into a dict named `tables`
# Mapping reminder:
# tables['table_1'] -> EMPLOYEE_DIRECTORY.pkl
# tables['table_2'] -> SE_PERSON.pkl
# tables['table_3'] -> WAREHOUSE_USERS.pkl
# tables['table_4'] -> DRUPAL_EMPLOYEE_DIRECTORY.pkl
# tables['table_5'] -> BUILDINGS.pkl
# tables['table_6'] -> MOIRA_LIST.pkl
# tables['table_7'] -> FAC_ROOMS.pkl
# tables['table_8'] -> FAC_BUILDING.pkl
# tables['table_9'] -> FCLT_ROOMS.pkl
# tables['table_10'] -> FCLT_BUILDING.pkl

# Load required tables from provided dict
fac_rooms = tables['table_7'].copy()
fac_building = tables['table_8'].copy()
buildings = tables['table_5'].copy()
moira_list = tables['table_6'].copy()
# Employee/people sources (we will use common kerberos identifiers if present)
emp_dir = tables['table_1'].copy()
se_person = tables['table_2'].copy()
warehouse_users = tables['table_3'].copy()
drupal_emp = tables['table_4'].copy()

# 1) Reproduce logic to find building(s) with maximum distinct floors from FAC_ROOMS
required_cols = {"BUILDING_KEY", "FLOOR"}
missing = required_cols - set(fac_rooms.columns)
if missing:
    raise ValueError(f"Missing required columns in FAC_ROOMS: {missing}")

fac_rooms["FLOOR_str"] = fac_rooms["FLOOR"].astype(str)
distinct_floors_per_building = (
    fac_rooms.groupby("BUILDING_KEY")["FLOOR_str"]
    .nunique(dropna=True)
    .rename("distinct_floor_count")
    .reset_index()
)
max_count = distinct_floors_per_building["distinct_floor_count"].max()
buildings_with_max = distinct_floors_per_building[
    distinct_floors_per_building["distinct_floor_count"] == max_count
].sort_values("BUILDING_KEY")

# 2) Resolve official building name for the building(s) with max floors
# Join paths as in reference: try FAC_BUILDING via BUILDING_NUMBER, fallback to BUILDINGS.BUILDING_NAME
fac_building_cols = [c for c in fac_building.columns if ("BUILDING" in c or "NAME" in c)]
fac_building_min_cols = ["BUILDING_NUMBER"] + [c for c in fac_building_cols if c != "BUILDING_NUMBER"]
fac_building_min = fac_building[fac_building_min_cols].drop_duplicates()

# We'll resolve names for all max buildings (though reference had E37, generalize here)
keys_with_max = buildings_with_max["BUILDING_KEY"].drop_duplicates()
tmp_df = pd.DataFrame({"BUILDING_KEY": keys_with_max})

# Attempt join to FAC_BUILDING
joined_fac_building = tmp_df.merge(
    fac_building_min, how="left", left_on="BUILDING_KEY", right_on="BUILDING_NUMBER", suffixes=("", "_facb")
)

# Fallback BUILDINGS
buildings_min = buildings[["BUILDING_NUMBER", "BUILDING_NAME"]].drop_duplicates()
joined_buildings = tmp_df.merge(
    buildings_min, how="left", left_on="BUILDING_KEY", right_on="BUILDING_NUMBER", suffixes=("", "_b")
)

# Coalesce name columns with preference order
candidate_name_cols = [
    "BUILDING_NAME_LONG",
    "PARENT_BUILDING_NAME_LONG",
    "PARENT_BUILDING_NAME",
    "BUILDING_NAME"
]

name_df = tmp_df.copy()
# Add candidate columns from FAC_BUILDING
for col in candidate_name_cols[:-1]:
    if col in joined_fac_building.columns:
        name_df = name_df.merge(
            joined_fac_building[["BUILDING_KEY", col]].drop_duplicates(),
            on="BUILDING_KEY", how="left"
        )
# Add BUILDINGS fallback
if "BUILDING_NAME" in joined_buildings.columns:
    name_df = name_df.merge(
        joined_buildings[["BUILDING_KEY", "BUILDING_NAME"]].drop_duplicates(),
        on="BUILDING_KEY", how="left", suffixes=("", "_from_buildings")
    )

def coalesce_name(row):
    for c in candidate_name_cols:
        if c in row and pd.notna(row[c]) and str(row[c]).strip():
            return str(row[c]).strip()
    if "BUILDING_NAME_from_buildings" in row and pd.notna(row["BUILDING_NAME_from_buildings"]) and str(row["BUILDING_NAME_from_buildings"]).strip():
        return str(row["BUILDING_NAME_from_buildings"]).strip()
    return None

name_df["OFFICIAL_BUILDING_NAME"] = name_df.apply(coalesce_name, axis=1)

# 3) Identify employees in that building with kerberos starting with 'c' (case-insensitive)
# There isn't a direct employee-to-building link provided in the guidelines tables besides directory-like tables.
# We'll assume EMPLOYEE_DIRECTORY and DRUPAL_EMPLOYEE_DIRECTORY and SE_PERSON/WAREHOUSE_USERS carry kerberos identifiers,
# and use any available building key/number field to link to BUILDING_KEY if present.
# We will union possible sources and then filter by building key and kerberos criteria.

# Helper to standardize kerberos column detection
def find_kerb_col(df):
    for col in df.columns:
        lc = col.lower()
        if lc in {"kerberos", "kerb", "username", "user_name", "athena_username", "uid"}:
            return col
        if lc.endswith("kerberos") or "kerberos" in lc or "athena" in lc or lc == "mit_id":
            return col
    return None

def find_building_key_col(df):
    # Try to find a column that matches building key/number
    priority = ["BUILDING_KEY", "BUILDING_NUMBER", "building_key", "building_number", "Bldg", "BLDG", "BLDG_NUM"]
    for p in priority:
        if p in df.columns:
            return p
    # fuzzy search
    for col in df.columns:
        lc = col.lower()
        if "building" in lc and ("key" in lc or "number" in lc or lc.endswith("no") or "num" in lc):
            return col
    return None

def extract_emp(df):
    kerb_col = find_kerb_col(df)
    bcol = find_building_key_col(df)
    cols = []
    if kerb_col:
        cols.append(kerb_col)
    if bcol:
        cols.append(bcol)
    if not cols:
        return pd.DataFrame(columns=["KERB", "BUILDING_KEY"])
    sub = df[cols].copy()
    sub.columns = [("KERB" if i==0 else "BUILDING_KEY") for i in range(len(cols))]
    if "BUILDING_KEY" not in sub.columns:
        sub["BUILDING_KEY"] = pd.NA
    return sub[["KERB", "BUILDING_KEY"]]

emp_frames = []
for src in [emp_dir, drupal_emp, se_person, warehouse_users]:
    emp_frames.append(extract_emp(src))

employees = pd.concat(emp_frames, ignore_index=True).dropna(subset=["KERB"])
# Normalize kerberos and building key strings
employees["KERB"] = employees["KERB"].astype(str).str.strip()
employees["BUILDING_KEY"] = employees["BUILDING_KEY"].astype(str).str.strip()

# If building key appears to be empty or 'nan', set to NA
employees.loc[employees["BUILDING_KEY"].str.lower().isin(["", "nan", "na", "none"]), "BUILDING_KEY"] = pd.NA

# Filter to the building(s) with max floors
target_keys = set(keys_with_max.astype(str))
employees_in_target = employees[employees["BUILDING_KEY"].isin(target_keys)].copy()

# Filter kerberos starting with 'c' (case-insensitive)
employees_in_target = employees_in_target[employees_in_target["KERB"].str.len() > 0]
employees_in_target = employees_in_target[employees_in_target["KERB"].str.lower().str.startswith("c")].drop_duplicates()

# 4) From MOIRA_LIST, find lists that these employees subscribe to, with list name starting with 'a' (case-insensitive)
# Heuristic for MOIRA_LIST columns:
# - list name column likely named "LIST_NAME" or similar
# - subscriber column likely named "KERB" or "USER_NAME" or "MEMBER"
def find_list_name_col(df):
    for col in df.columns:
        lc = col.lower()
        if lc in {"list_name", "name", "moira_list", "list"}:
            return col
        if "list" in lc and "name" in lc:
            return col
    return None

def find_member_col(df):
    for col in df.columns:
        lc = col.lower()
        if lc in {"kerberos", "member", "user_name", "username", "uid", "athena_username"}:
            return col
        if "member" in lc or "kerb" in lc or "athena" in lc:
            return col
    return None

list_name_col = find_list_name_col(moira_list)
member_col = find_member_col(moira_list)

if list_name_col is None or member_col is None:
    # If structure not as expected, create empty result
    final_df = pd.DataFrame(columns=["BUILDING_KEY", "BUILDING_NAME", "KERB", "LIST_NAME"]).head(0)
else:
    ml = moira_list[[list_name_col, member_col]].copy()
    ml.columns = ["LIST_NAME", "KERB"]
    ml["KERB"] = ml["KERB"].astype(str).str.strip()
    ml["LIST_NAME"] = ml["LIST_NAME"].astype(str).str.strip()

    # Filter list names starting with 'a' (case-insensitive)
    ml = ml[ml["LIST_NAME"].str.lower().str.startswith("a")]

    # Join with employees in target buildings (kerberos match, case-insensitive)
    # Normalize case
    ml["KERB_lower"] = ml["KERB"].str.lower()
    employees_in_target["KERB_lower"] = employees_in_target["KERB"].str.lower()

    subs = employees_in_target.merge(ml[["KERB_lower", "LIST_NAME"]], on="KERB_lower", how="inner")

    # Attach official building name
    name_map = name_df[["BUILDING_KEY", "OFFICIAL_BUILDING_NAME"]].drop_duplicates()
    subs = subs.merge(name_map, on="BUILDING_KEY", how="left")

    # Prepare final columns
    final_df = subs[["BUILDING_KEY", "OFFICIAL_BUILDING_NAME", "KERB", "LIST_NAME"]].drop_duplicates()
    final_df = final_df.rename(columns={"OFFICIAL_BUILDING_NAME": "BUILDING_NAME"})

# If multiple buildings tie, include all; otherwise, show the single one (like E37).
# Assemble result as required: dict[str, DataFrame]
result = {
    "building_employee_mailing_lists": final_df.reset_index(drop=True)
}