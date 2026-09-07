import pandas as pd

# Input tables are provided in `tables` dict:
# tables['table_1'] -> FAC_BUILDING_ADDRESS.pkl
# tables['table_2'] -> FCLT_BUILDING_ADDRESS_HIST.pkl
# tables['table_3'] -> FCLT_BUILDING_ADDRESS.pkl
# tables['table_4'] -> BUILDINGS.pkl
# tables['table_5'] -> FCLT_BUILDING_HIST_1.pkl
# tables['table_6'] -> FCLT_BUILDING_HIST.pkl
# tables['table_7'] -> IR_INSTITUTION.pkl
# tables['table_8'] -> FCLT_ROOMS_HIST.pkl
# tables['table_9'] -> FCLT_BUILDING.pkl
# tables['table_10'] -> FAC_BUILDING.pkl

# 1) Load the FAC_BUILDING_ADDRESS DataFrame (for parity with reference; not used directly in final join)
dfa = tables['table_1']

# 2) Filter rows where ADDRESS_PURPOSE == "STREET"
street_df = dfa.loc[dfa["ADDRESS_PURPOSE"].astype(str).str.upper() == "STREET"].copy()

# Implement current plan:
# - Search FCLT_ROOMS_HIST for ORGANIZATION_NAME or MINOR_ORGANIZATION containing "History" (case-insensitive)
# - Extract distinct FCLT_BUILDING_KEYs
# - Join to FCLT_BUILDING_ADDRESS filtered to ADDRESS_PURPOSE='STREET'
# - Compose STREET address

# Load rooms hist
rooms = tables['table_8'][["FCLT_BUILDING_KEY", "ORGANIZATION_NAME", "MINOR_ORGANIZATION"]]

# History mask on either ORGANIZATION_NAME or MINOR_ORGANIZATION
hist_mask = (
    rooms["ORGANIZATION_NAME"].astype(str).str.contains("History", case=False, na=False)
    | rooms["MINOR_ORGANIZATION"].astype(str).str.contains("History", case=False, na=False)
)

hist_rooms = rooms.loc[hist_mask, ["FCLT_BUILDING_KEY"]].dropna().drop_duplicates()

# Map FCLT_BUILDING_KEY -> BUILDING_NUMBER via FCLT_BUILDING
fclt_building = tables['table_9'][["FCLT_BUILDING_KEY", "BUILDING_NUMBER"]].drop_duplicates()
hist_buildings = hist_rooms.merge(fclt_building, on="FCLT_BUILDING_KEY", how="left")

# Use FCLT_BUILDING_ADDRESS as the authoritative address table keyed by BUILDING_NUMBER
fclt_addr = tables['table_3']

# Keep only STREET purpose addresses there as well
fclt_addr_street = fclt_addr.loc[fclt_addr["ADDRESS_PURPOSE"].astype(str).str.upper() == "STREET"].copy()

# Join to get address components
hist_bldg_addr = (
    hist_buildings
    .merge(fclt_addr_street, on="BUILDING_NUMBER", how="left", suffixes=("", "_addr"))
)

# Compose a street address string: [STREET_NUMBER][STREET_NUMBER_SUFFIX?] [PRE_DIRECTIONAL?] [STREET_NAME] [STREET_SUFFIX] [POST_DIRECTIONAL?]
def compose_street(row):
    parts = []
    num = str(row.get("STREET_NUMBER")).strip() if pd.notna(row.get("STREET_NUMBER")) else ""
    sns = str(row.get("STREET_NUMBER_SUFFIX")).strip() if pd.notna(row.get("STREET_NUMBER_SUFFIX")) else ""
    if num and sns:
        parts.append(f"{num}{sns if sns.startswith(('/', '-', '#')) else ' ' + sns}")
    elif num:
        parts.append(num)
    pre = row.get("PRE_DIRECTIONAL")
    if pd.notna(pre) and str(pre).strip():
        parts.append(str(pre).strip())
    if pd.notna(row.get("STREET_NAME")) and str(row.get("STREET_NAME")).strip():
        parts.append(str(row.get("STREET_NAME")).strip())
    if pd.notna(row.get("STREET_SUFFIX")) and str(row.get("STREET_SUFFIX")).strip():
        parts.append(str(row.get("STREET_SUFFIX")).strip())
    post = row.get("POST_DIRECTIONAL")
    if pd.notna(post) and str(post).strip():
        parts.append(str(post).strip())
    return " ".join(" ".join(parts).split())

hist_bldg_addr["STREET_ADDRESS_COMPOSED"] = hist_bldg_addr.apply(compose_street, axis=1)

# Select and clean final columns
final_cols = [
    "FCLT_BUILDING_KEY",
    "BUILDING_NUMBER",
    "STREET_ADDRESS_COMPOSED",
    "CITY",
    "STATE",
    "POSTAL_CODE",
    "WAREHOUSE_LOAD_DATE",
]
history_addresses = (
    hist_bldg_addr[final_cols]
    .dropna(subset=["BUILDING_NUMBER"])
    .drop_duplicates()
    .sort_values(["BUILDING_NUMBER", "CITY", "STATE", "POSTAL_CODE"])
    .reset_index(drop=True)
)

# Prepare final answer table with requested fields
answer_cols = [
    "FCLT_BUILDING_KEY",
    "STREET_ADDRESS_COMPOSED",
    "CITY",
    "STATE",
    "POSTAL_CODE",
]
final_answer = history_addresses.rename(columns={
    "FCLT_BUILDING_KEY": "BUILDING_KEY",
    "STREET_ADDRESS_COMPOSED": "BUILDING_STREET_ADDRESS"
})[["BUILDING_KEY", "BUILDING_STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"]]

# Package into result dict
result = {"history_department_current_address": final_answer}