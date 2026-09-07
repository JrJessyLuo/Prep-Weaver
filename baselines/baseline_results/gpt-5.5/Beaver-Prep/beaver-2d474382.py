import pandas as pd

def _norm_str(s):
    return s.astype("string").str.strip()

def _norm_key(s):
    return _norm_str(s).str.upper()

def _norm_id(s):
    return _norm_str(s).str.lower()

def _office_to_building(s):
    x = _norm_str(s).str.upper()
    return x.str.extract(r"^([A-Z]*\d+[A-Z]*|[A-Z]+)", expand=False)

# Floors per building
room_parts = []
for name, df in tables.items():
    if {"BUILDING_KEY", "FLOOR"}.issubset(df.columns):
        tmp = df[["BUILDING_KEY", "FLOOR"]].copy()
        tmp.columns = ["building_key", "floor"]
        room_parts.append(tmp)
    elif {"FCLT_BUILDING_KEY", "FLOOR"}.issubset(df.columns):
        tmp = df[["FCLT_BUILDING_KEY", "FLOOR"]].copy()
        tmp.columns = ["building_key", "floor"]
        room_parts.append(tmp)

rooms = pd.concat(room_parts, ignore_index=True).dropna(subset=["building_key", "floor"])
rooms["building_key"] = _norm_key(rooms["building_key"])
rooms["floor"] = _norm_str(rooms["floor"]).str.upper()
rooms = rooms[(rooms["building_key"].notna()) & (rooms["floor"].notna()) & (rooms["floor"] != "")]

floor_counts = (
    rooms.drop_duplicates(["building_key", "floor"])
    .groupby("building_key", as_index=False)
    .agg(num_floors=("floor", "nunique"))
)

max_floors = floor_counts["num_floors"].max()
top_buildings = floor_counts.loc[floor_counts["num_floors"].eq(max_floors), ["building_key"]].copy()

# Building names
building_name_parts = []
for df in tables.values():
    key_col = None
    for c in ["FAC_BUILDING_KEY", "FCLT_BUILDING_KEY", "BUILDING_KEY", "BUILDING_NUMBER"]:
        if c in df.columns:
            key_col = c
            break
    if key_col and "BUILDING_NAME" in df.columns:
        tmp = df[[key_col, "BUILDING_NAME"]].dropna(subset=[key_col]).copy()
        tmp.columns = ["building_key", "building_name"]
        building_name_parts.append(tmp)

building_names = pd.concat(building_name_parts, ignore_index=True).drop_duplicates() if building_name_parts else pd.DataFrame(columns=["building_key", "building_name"])
building_names["building_key"] = _norm_key(building_names["building_key"])
building_names["building_name"] = _norm_str(building_names["building_name"])
top_buildings = top_buildings.merge(building_names, on="building_key", how="left").drop_duplicates("building_key")

# Employees in the top building(s), with kerberos starting with c
employee_parts = []
for df in tables.values():
    office_cols = [c for c in df.columns if c.upper() == "OFFICE_LOCATION"]
    if not office_cols:
        continue

    krb_cols = [c for c in df.columns if "KRB" in c.upper() or "KERBEROS" in c.upper()]
    if not krb_cols and "EMAIL_ADDRESS" in df.columns:
        tmp = df[[office_cols[0], "EMAIL_ADDRESS"]].copy()
        tmp["krb_name"] = _norm_id(tmp["EMAIL_ADDRESS"]).str.split("@").str[0]
        tmp = tmp[[office_cols[0], "krb_name"]]
        tmp.columns = ["office_location", "krb_name"]
        employee_parts.append(tmp)
    else:
        for kc in krb_cols:
            tmp = df[[office_cols[0], kc]].copy()
            tmp.columns = ["office_location", "krb_name"]
            employee_parts.append(tmp)

employees = pd.concat(employee_parts, ignore_index=True) if employee_parts else pd.DataFrame(columns=["office_location", "krb_name"])
employees["krb_name"] = _norm_id(employees["krb_name"])
employees["building_key"] = _office_to_building(employees["office_location"])
employees = employees[
    employees["building_key"].isin(top_buildings["building_key"])
    & employees["krb_name"].str.startswith("c", na=False)
].drop_duplicates(["building_key", "krb_name"])

employee_ids = set(employees["krb_name"].dropna())

# Mailing lists starting with a
lists = tables["table_6"].copy()
lists["list_key_norm"] = _norm_id(lists["MOIRA_LIST_KEY"])
lists["list_name_norm"] = _norm_id(lists["MOIRA_LIST_NAME"])
lists["mailing_list_name"] = _norm_str(lists["MOIRA_LIST_NAME"])

a_lists = lists[
    lists["list_name_norm"].str.startswith("a", na=False)
    & lists["IS_MOIRA_MAILING_LIST"].astype("string").str.strip().str.upper().eq("Y")
][["list_key_norm", "list_name_norm", "mailing_list_name"]].drop_duplicates()

# Find subscription/membership rows, if such a table is present
subscription_matches = []
for df in tables.values():
    cols_upper = {c: c.upper() for c in df.columns}

    list_cols = [
        c for c, cu in cols_upper.items()
        if "LIST" in cu
        and "DESCRIPTION" not in cu
        and not cu.startswith("IS_")
        and cu not in {"IS_ACTIVE", "IS_PUBLIC", "IS_HIDDEN", "IS_MOIRA_GROUP", "IS_NFS_GROUP", "IS_MOIRA_MAILING_LIST"}
    ]
    member_cols = [
        c for c, cu in cols_upper.items()
        if (
            "KRB" in cu
            or "KERBEROS" in cu
            or "MEMBER" in cu
            or "SUBSCRIBER" in cu
            or cu in {"USER", "USERNAME", "USER_NAME", "EMAIL", "EMAIL_ADDRESS"}
        )
        and "LIST" not in cu
    ]

    for lc in list_cols:
        for mc in member_cols:
            tmp = df[[lc, mc]].dropna().copy()
            if tmp.empty:
                continue

            tmp["list_norm"] = _norm_id(tmp[lc])
            tmp["member_norm"] = _norm_id(tmp[mc])
            tmp["member_krb"] = tmp["member_norm"].str.split("@").str[0]
            tmp = tmp[tmp["member_krb"].isin(employee_ids)]
            if tmp.empty:
                continue

            m1 = tmp.merge(a_lists, left_on="list_norm", right_on="list_key_norm", how="inner")
            m2 = tmp.merge(a_lists, left_on="list_norm", right_on="list_name_norm", how="inner")
            matched = pd.concat([m1, m2], ignore_index=True)
            if not matched.empty:
                subscription_matches.append(matched[["member_krb", "mailing_list_name"]].drop_duplicates())

if subscription_matches:
    subscriptions = pd.concat(subscription_matches, ignore_index=True).drop_duplicates()
else:
    subscriptions = pd.DataFrame(columns=["member_krb", "mailing_list_name"])

answer = (
    employees[["building_key", "krb_name"]]
    .merge(subscriptions, left_on="krb_name", right_on="member_krb", how="inner")
    .merge(top_buildings[["building_key", "building_name"]], on="building_key", how="left")
    [["building_name", "mailing_list_name"]]
    .drop_duplicates()
    .sort_values(["building_name", "mailing_list_name"], na_position="last")
    .reset_index(drop=True)
)

result = {"building_mailing_lists": answer}
