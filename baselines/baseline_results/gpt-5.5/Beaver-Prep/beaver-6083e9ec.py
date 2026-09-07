import pandas as pd

rooms = tables["table_8"]

current_period = rooms["FISCAL_PERIOD"].max()
rooms_current = rooms.loc[
    rooms["FISCAL_PERIOD"].eq(current_period),
    ["FCLT_BUILDING_KEY", "FCLT_ROOM_KEY", "ORGANIZATION_NAME", "AREA"]
].copy()

org_norm = rooms_current["ORGANIZATION_NAME"].fillna("").astype(str).str.upper().str.strip()
history_mask = org_norm.str.contains(r"(?:^|[^A-Z0-9])HIST(?:ORY)?(?:[^A-Z0-9]|$)", regex=True, na=False)
history_rooms = rooms_current.loc[history_mask].copy()

if history_rooms.empty:
    org_norm_all = rooms["ORGANIZATION_NAME"].fillna("").astype(str).str.upper().str.strip()
    history_mask_all = org_norm_all.str.contains(r"(?:^|[^A-Z0-9])HIST(?:ORY)?(?:[^A-Z0-9]|$)", regex=True, na=False)
    history_all = rooms.loc[
        history_mask_all,
        ["FISCAL_PERIOD", "FCLT_BUILDING_KEY", "FCLT_ROOM_KEY", "ORGANIZATION_NAME", "AREA"]
    ].copy()
    if not history_all.empty:
        latest_history_period = history_all["FISCAL_PERIOD"].max()
        history_rooms = history_all.loc[history_all["FISCAL_PERIOD"].eq(latest_history_period)].copy()

dept_buildings = (
    history_rooms
    .groupby("FCLT_BUILDING_KEY", as_index=False)
    .agg(
        _total_area=("AREA", lambda s: s.fillna(0).sum()),
        _room_count=("FCLT_ROOM_KEY", "nunique")
    )
    .sort_values(["_total_area", "_room_count", "FCLT_BUILDING_KEY"], ascending=[False, False, True])
    .rename(columns={"FCLT_BUILDING_KEY": "BUILDING_KEY"})
)

address_frames = []
address_parts = [
    "STREET_NUMBER",
    "STREET_NUMBER_SUFFIX",
    "PRE_DIRECTIONAL",
    "STREET_NAME",
    "STREET_SUFFIX",
    "POST_DIRECTIONAL",
]

for source_order, (table_name, key_col) in enumerate([
    ("table_3", "FCLT_BUILDING_KEY"),
    ("table_1", "BUILDING_KEY"),
]):
    a = tables[table_name].copy()
    a = a.loc[a["ADDRESS_PURPOSE"].fillna("").astype(str).str.upper().eq("STREET")].copy()
    for col in address_parts:
        if col not in a.columns:
            a[col] = pd.NA

    a["BUILDING_KEY"] = a[key_col].astype(str)

    def make_street_address(row):
        vals = []
        for col in address_parts:
            val = row[col]
            if pd.notna(val) and str(val).strip() != "":
                vals.append(str(val).strip())
        return " ".join(vals) if vals else pd.NA

    a["_ADDRESS_STREET"] = a.apply(make_street_address, axis=1)
    a["_source_order"] = source_order
    address_frames.append(a[["BUILDING_KEY", "_ADDRESS_STREET", "CITY", "STATE", "POSTAL_CODE", "_source_order"]])

addresses = (
    pd.concat(address_frames, ignore_index=True)
    .sort_values("_source_order")
    .drop_duplicates("BUILDING_KEY", keep="first")
    .drop(columns="_source_order")
)

building_street = (
    tables["table_4"][["BUILDING_KEY", "BUILDING_STREET_ADDRESS"]]
    .drop_duplicates("BUILDING_KEY", keep="first")
)

out = (
    dept_buildings
    .merge(building_street, on="BUILDING_KEY", how="left")
    .merge(addresses, on="BUILDING_KEY", how="left")
)

out["BUILDING_STREET_ADDRESS"] = out["BUILDING_STREET_ADDRESS"].combine_first(out["_ADDRESS_STREET"])

def format_postal_code(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.zfill(5) if s.isdigit() and len(s) < 5 else s

out["POSTAL_CODE"] = out["POSTAL_CODE"].apply(format_postal_code)

final = (
    out[["BUILDING_KEY", "BUILDING_STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"history_department_building_address": final}
