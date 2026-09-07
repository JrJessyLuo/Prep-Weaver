import pandas as pd

# The `tables` dict with DataFrames is assumed to be preloaded in the environment.
# Mapping:
# tables['table_1'] -> FAC_ROOMS.pkl
# tables['table_2'] -> FCLT_ROOMS.pkl
# tables['table_3'] -> FAC_BUILDING.pkl
# tables['table_4'] -> FCLT_ROOMS_HIST.pkl
# tables['table_5'] -> FAC_BUILDING_ADDRESS.pkl
# tables['table_6'] -> FCLT_BUILDING.pkl
# tables['table_7'] -> FCLT_BUILDING_HIST.pkl
# tables['table_8'] -> CIS_COURSE_CATALOG.pkl
# tables['table_9'] -> SUBJECT_ENROLLABLE.pkl
# tables['table_10'] -> FCLT_BUILDING_HIST_1.pkl

df_enroll = tables['table_9'].copy()
df_catalog = tables['table_8'].copy()
fac_rooms = tables['table_1'].copy()
fclt_rooms = tables['table_2'].copy()
fac_bldg = tables['table_3'].copy()
fac_bldg_addr = tables['table_5'].copy()
fclt_bldg = tables['table_6'].copy()

# ----- Step 1: Identify CS-like subjects from SUBJECT_ENROLLABLE (replicating the reference logic) -----
cs_like_codes = {
    "6", "6-1", "6-2", "6-3", "6-4", "6-7", "6-9", "6-14",
    "6C", "6P", "6M", "6A", "6E", "CS", "COMP SCI", "COMPSCI", "COMP_SCI",
    "EECS", "EE&CS", "EECS/CS", "CSAIL", "CSC", "CSE", "SCS"
}

offer_dept_norm = (
    df_enroll["OFFER_DEPT_CODE"]
    .astype(str)
    .str.strip()
    .str.upper()
)

mask_cs = offer_dept_norm.isin({c.upper() for c in cs_like_codes})
mask_cs |= offer_dept_norm.str.startswith("6", na=False)

cs_subject_ids = (
    df_enroll.loc[mask_cs, "SUBJECT_ID"]
    .dropna()
    .astype(str)
    .unique()
)

# ----- Step 2: Join with CIS_COURSE_CATALOG on SUBJECT_ID to get potential location fields (same as reference) -----
df_enroll["SUBJECT_ID_STR"] = df_enroll["SUBJECT_ID"].astype(str)
df_catalog["SUBJECT_ID_STR"] = df_catalog["SUBJECT_ID"].astype(str)

df_enroll_cs = df_enroll[df_enroll["SUBJECT_ID_STR"].isin(cs_subject_ids)].copy()

enroll_cols = ["TERM_CODE", "SUBJECT_ID_STR", "SUBJECT_ID", "SUBJECT_TITLE", "SUBJECT_TITLE_LONG"]
df_enroll_cs_small = df_enroll_cs[enroll_cols].drop_duplicates()

catalog_cols = set(df_catalog.columns.str.upper())
possible_location_cols = []
for col in df_catalog.columns:
    cu = col.upper()
    if any(kw in cu for kw in [
        "BUILDING_ROOM", "FCLT_BUILDING_KEY", "BUILDING_KEY", "ROOM", "SPACE_ID",
        "FLOOR_KEY", "FCLT_ROOM_KEY", "FCLT_FLOOR_KEY", "LOCATION", "MEETING", "MEETS", "ROOM_FULL_NAME"
    ]):
        possible_location_cols.append(col)

df_join = df_enroll_cs_small.merge(
    df_catalog[["SUBJECT_ID_STR"] + possible_location_cols] if possible_location_cols else df_catalog[["SUBJECT_ID_STR"]],
    on="SUBJECT_ID_STR",
    how="left"
)

# ----- Step 3: From catalog, try to extract explicit facility keys to map to rooms/buildings -----
# Heuristics to find keys to rooms/buildings present in catalog
def norm_cols(df):
    return {c.upper(): c for c in df.columns}

cat_map = norm_cols(df_catalog)

col_room_key = cat_map.get("FCLT_ROOM_KEY")
col_building_key = cat_map.get("FCLT_BUILDING_KEY") or cat_map.get("BUILDING_KEY")
col_space_id = cat_map.get("SPACE_ID")
col_room_full_name = cat_map.get("ROOM_FULL_NAME")
col_building_room = cat_map.get("BUILDING_ROOM")

# Build a working set of possible room identifiers from catalog rows associated with CS subjects
cat_cs = df_catalog[df_catalog["SUBJECT_ID_STR"].isin(cs_subject_ids)].copy()

# Normalize potential keys
for c in [col_room_key, col_building_key, col_space_id, col_room_full_name, col_building_room]:
    if c and c not in cat_cs.columns:
        c = None

room_keys = pd.Series([], dtype=object)
if col_room_key:
    room_keys = pd.Series(cat_cs[col_room_key].dropna().astype(str).unique())
space_ids = pd.Series([], dtype=object)
if col_space_id:
    space_ids = pd.Series(cat_cs[col_space_id].dropna().astype(str).unique())

# We'll try to resolve to rooms via:
# 1) FCLT_ROOM_KEY -> FCLT_ROOMS -> FAC_ROOMS
# 2) SPACE_ID -> FAC_ROOMS
# Then to building via FAC_ROOMS.BUILDING_KEY or FCLT_ROOMS.FCLT_BUILDING_KEY

# Prepare keys in facilities tables
# Normalize keys as strings for joins
def to_str_series(s):
    return s.astype(str)

# FCLT_ROOMS key columns guess
fclt_cols = norm_cols(fclt_rooms)
fclt_room_key_col = fclt_cols.get("FCLT_ROOM_KEY") or fclt_cols.get("ROOM_KEY") or list(fclt_rooms.columns)[0]
fclt_space_id_col = fclt_cols.get("SPACE_ID")
fclt_bldg_key_col = fclt_cols.get("FCLT_BUILDING_KEY") or fclt_cols.get("BUILDING_KEY")

# FAC_ROOMS key columns guess
facr_cols = norm_cols(fac_rooms)
fac_space_id_col = facr_cols.get("SPACE_ID") or list(fac_rooms.columns)[0]
fac_bldg_key_col = facr_cols.get("BUILDING_KEY")
fac_room_name_col = facr_cols.get("ROOM_FULL_NAME") or facr_cols.get("ROOM_NAME") or facr_cols.get("ROOM") or list(fac_rooms.columns)[0]

# FAC_BUILDING columns guess (names, heights)
facb_cols = norm_cols(fac_bldg)
facb_bldg_key_col = facb_cols.get("BUILDING_KEY") or list(fac_bldg.columns)[0]
facb_name_col = facb_cols.get("BUILDING_NAME") or facb_cols.get("BLDG_NAME") or facb_cols.get("NAME") or list(fac_bldg.columns)[0]
# Try heights: look for common terms
height_col = None
for cand in ["HEIGHT", "BLDG_HEIGHT", "BUILDING_HEIGHT", "TOTAL_HEIGHT", "HEIGHT_FT"]:
    if cand in facb_cols:
        height_col = facb_cols[cand]
        break

# FAC_BUILDING_ADDRESS columns guess
addr_cols = norm_cols(fac_bldg_addr)
addr_bldg_key_col = addr_cols.get("BUILDING_KEY") or list(fac_bldg_addr.columns)[0]
street_col = addr_cols.get("STREET_ADDRESS") or addr_cols.get("ADDRESS") or addr_cols.get("ADDR_LINE1")
city_col = addr_cols.get("CITY")
state_col = addr_cols.get("STATE") or addr_cols.get("STATE_CODE")
zip_col = addr_cols.get("POSTAL_CODE") or addr_cols.get("ZIP") or addr_cols.get("ZIP_CODE")

# Resolve via FCLT_ROOM_KEY to fclt_rooms then to fac_rooms via SPACE_ID (if available)
df_rooms_via_fclt = pd.DataFrame(columns=["ROOM_FULL_NAME", "BUILDING_KEY"])
if not room_keys.empty and fclt_room_key_col in fclt_rooms.columns:
    fclt_subset = fclt_rooms[[c for c in [fclt_room_key_col, fclt_space_id_col, fclt_bldg_key_col] if c]].copy()
    fclt_subset[fclt_room_key_col] = fclt_subset[fclt_room_key_col].astype(str)
    match_fclt = fclt_subset[fclt_subset[fclt_room_key_col].isin(room_keys.tolist())].copy()

    # Prefer using FAC_ROOMS via SPACE_ID to get full room names; fallback to what exists in fclt if any
    if not match_fclt.empty and fclt_space_id_col and fclt_space_id_col in match_fclt.columns and fac_space_id_col in fac_rooms.columns:
        fac_subset = fac_rooms[[c for c in [fac_space_id_col, fac_bldg_key_col, fac_room_name_col] if c]].copy()
        fac_subset[fac_space_id_col] = fac_subset[fac_space_id_col].astype(str)
        match_fclt[fclt_space_id_col] = match_fclt[fclt_space_id_col].astype(str)
        df_rooms_via_fclt = match_fclt.merge(
            fac_subset,
            left_on=fclt_space_id_col,
            right_on=fac_space_id_col,
            how="left"
        )
        # Standardize columns
        if "ROOM_FULL_NAME" not in df_rooms_via_fclt.columns and fac_room_name_col in df_rooms_via_fclt.columns:
            df_rooms_via_fclt = df_rooms_via_fclt.rename(columns={fac_room_name_col: "ROOM_FULL_NAME"})
        if "BUILDING_KEY" not in df_rooms_via_fclt.columns and fac_bldg_key_col in df_rooms_via_fclt.columns:
            df_rooms_via_fclt = df_rooms_via_fclt.rename(columns={fac_bldg_key_col: "BUILDING_KEY"})
        # If still missing BUILDING_KEY, fallback to fclt building key
        if "BUILDING_KEY" not in df_rooms_via_fclt.columns and fclt_bldg_key_col in df_rooms_via_fclt.columns:
            df_rooms_via_fclt = df_rooms_via_fclt.rename(columns={fclt_bldg_key_col: "BUILDING_KEY"})
        df_rooms_via_fclt = df_rooms_via_fclt[["ROOM_FULL_NAME", "BUILDING_KEY"]].dropna(subset=["ROOM_FULL_NAME", "BUILDING_KEY"])
    elif not match_fclt.empty and fclt_bldg_key_col in match_fclt.columns:
        # No FAC_ROOMS path; just carry building key (room name may be unavailable)
        tmp = match_fclt[[fclt_bldg_key_col]].copy()
        tmp = tmp.rename(columns={fclt_bldg_key_col: "BUILDING_KEY"})
        tmp["ROOM_FULL_NAME"] = None
        df_rooms_via_fclt = tmp[["ROOM_FULL_NAME", "BUILDING_KEY"]].dropna(subset=["BUILDING_KEY"])

# Resolve via SPACE_ID directly from catalog -> FAC_ROOMS
df_rooms_via_space = pd.DataFrame(columns=["ROOM_FULL_NAME", "BUILDING_KEY"])
if not space_ids.empty and fac_space_id_col in fac_rooms.columns:
    fac_subset = fac_rooms[[c for c in [fac_space_id_col, fac_bldg_key_col, fac_room_name_col] if c]].copy()
    fac_subset[fac_space_id_col] = fac_subset[fac_space_id_col].astype(str)
    df_rooms_via_space = fac_subset[fac_subset[fac_space_id_col].isin(space_ids.tolist())].copy()
    if "ROOM_FULL_NAME" not in df_rooms_via_space.columns and fac_room_name_col in df_rooms_via_space.columns:
        df_rooms_via_space = df_rooms_via_space.rename(columns={fac_room_name_col: "ROOM_FULL_NAME"})
    if "BUILDING_KEY" not in df_rooms_via_space.columns and fac_bldg_key_col in df_rooms_via_space.columns:
        df_rooms_via_space = df_rooms_via_space.rename(columns={fac_bldg_key_col: "BUILDING_KEY"})
    df_rooms_via_space = df_rooms_via_space[["ROOM_FULL_NAME", "BUILDING_KEY"]].dropna(subset=["BUILDING_KEY"])

# If catalog directly has ROOM_FULL_NAME but no keys, we will carry those and try to map later via building_room if present
direct_room_names = pd.DataFrame(columns=["ROOM_FULL_NAME"])
if col_room_full_name and col_room_full_name in cat_cs.columns:
    direct_room_names = cat_cs[[col_room_full_name]].rename(columns={col_room_full_name: "ROOM_FULL_NAME"}).dropna().drop_duplicates()

# Combine room candidates
room_candidates = pd.concat([
    df_rooms_via_fclt,
    df_rooms_via_space
], ignore_index=True)

# Deduplicate candidates by room name + building key when available
if not room_candidates.empty:
    room_candidates["ROOM_FULL_NAME"] = room_candidates["ROOM_FULL_NAME"].astype(str)
    room_candidates["BUILDING_KEY"] = room_candidates["BUILDING_KEY"].astype(str)
    room_candidates = room_candidates.drop_duplicates()

# If we have bare room names without building, try to enrich by matching FAC_ROOMS room names uniquely
if not direct_room_names.empty:
    direct_room_names["ROOM_FULL_NAME"] = direct_room_names["ROOM_FULL_NAME"].astype(str).str.strip()
    # Attempt to match exact room full names in FAC_ROOMS to fetch building
    if fac_room_name_col in fac_rooms.columns:
        fac_match = fac_rooms[[fac_room_name_col, fac_bldg_key_col]].copy()
        fac_match = fac_match.rename(columns={fac_room_name_col: "ROOM_FULL_NAME", fac_bldg_key_col: "BUILDING_KEY"})
        fac_match["ROOM_FULL_NAME"] = fac_match["ROOM_FULL_NAME"].astype(str).str.strip()
        fac_match["BUILDING_KEY"] = fac_match["BUILDING_KEY"].astype(str)
        dm = direct_room_names.merge(fac_match.dropna(subset=["ROOM_FULL_NAME", "BUILDING_KEY"]).drop_duplicates(),
                                     on="ROOM_FULL_NAME",
                                     how="left")
        dm = dm.dropna(subset=["BUILDING_KEY"])
        dm = dm[["ROOM_FULL_NAME", "BUILDING_KEY"]].drop_duplicates()
        if not dm.empty:
            room_candidates = pd.concat([room_candidates, dm], ignore_index=True)

# Final unique room-building pairs
room_building_pairs = pd.DataFrame(columns=["ROOM_FULL_NAME", "BUILDING_KEY"])
if not room_candidates.empty:
    room_building_pairs = room_candidates.dropna(subset=["BUILDING_KEY"]).copy()
    room_building_pairs["BUILDING_KEY"] = room_building_pairs["BUILDING_KEY"].astype(str)
    room_building_pairs["ROOM_FULL_NAME"] = room_building_pairs["ROOM_FULL_NAME"].astype(str)
    room_building_pairs = room_building_pairs.drop_duplicates()

# Join building attributes: name, address, city, state, postal, height
# Prepare building dimension table
bldg_dim = fac_bldg.copy()
if facb_bldg_key_col not in bldg_dim.columns:
    # If BUILDING_KEY wasn't found, use first column as key fallback
    bldg_dim = bldg_dim.rename(columns={bldg_dim.columns[0]: "BUILDING_KEY"})
    facb_bldg_key_col = "BUILDING_KEY"

# Standardize building name and height columns
rename_bldg = {}
if facb_name_col and facb_name_col in bldg_dim.columns:
    rename_bldg[facb_name_col] = "BUILDING_NAME"
if height_col and height_col in bldg_dim.columns:
    rename_bldg[height_col] = "BUILDING_HEIGHT"
if facb_bldg_key_col != "BUILDING_KEY":
    rename_bldg[facb_bldg_key_col] = "BUILDING_KEY"
bldg_dim = bldg_dim.rename(columns=rename_bldg)

# Keep only necessary columns
keep_bldg_cols = [c for c in ["BUILDING_KEY", "BUILDING_NAME", "BUILDING_HEIGHT"] if c in bldg_dim.columns]
bldg_dim = bldg_dim[keep_bldg_cols].drop_duplicates()

# Address table
addr_dim = fac_bldg_addr.copy()
rename_addr = {}
if addr_bldg_key_col and addr_bldg_key_col in addr_dim.columns and addr_bldg_key_col != "BUILDING_KEY":
    rename_addr[addr_bldg_key_col] = "BUILDING_KEY"
if street_col and street_col in addr_dim.columns:
    rename_addr[street_col] = "STREET_ADDRESS"
if city_col and city_col in addr_dim.columns:
    rename_addr[city_col] = "CITY"
if state_col and state_col in addr_dim.columns:
    rename_addr[state_col] = "STATE"
if zip_col and zip_col in addr_dim.columns:
    rename_addr[zip_col] = "POSTAL_CODE"
addr_dim = addr_dim.rename(columns=rename_addr)

addr_keep = [c for c in ["BUILDING_KEY", "STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"] if c in addr_dim.columns]
addr_dim = addr_dim[addr_keep].drop_duplicates()

# Merge room-building pairs to building dims and address
final_df = pd.DataFrame(columns=["ROOM_FULL_NAME", "BUILDING_NAME", "STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE", "BUILDING_HEIGHT"])

if not room_building_pairs.empty and "BUILDING_KEY" in room_building_pairs.columns:
    rb = room_building_pairs.copy()
    rb["BUILDING_KEY"] = rb["BUILDING_KEY"].astype(str)

    # Attach building name/height
    if "BUILDING_KEY" in bldg_dim.columns:
        bldg_dim_m = bldg_dim.copy()
        bldg_dim_m["BUILDING_KEY"] = bldg_dim_m["BUILDING_KEY"].astype(str)
        rb = rb.merge(bldg_dim_m, on="BUILDING_KEY", how="left")

    # Attach address
    if "BUILDING_KEY" in addr_dim.columns:
        addr_dim_m = addr_dim.copy()
        addr_dim_m["BUILDING_KEY"] = addr_dim_m["BUILDING_KEY"].astype(str)
        rb = rb.merge(addr_dim_m, on="BUILDING_KEY", how="left")

    # Select and deduplicate
    cols_out = ["ROOM_FULL_NAME", "BUILDING_NAME", "STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE", "BUILDING_HEIGHT"]
    existing_out = [c for c in cols_out if c in rb.columns]
    final_df = rb[existing_out].drop_duplicates().sort_values(existing_out).reset_index(drop=True)

# Assign to result as required
result = {
    "rooms_with_building_and_address": final_df
}