import pandas as pd
import numpy as np
import re

tokens = ["summer", "haynes"]

def _clean_series(s):
    return s.astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "<NA>": pd.NA})

def _token_match(df, tokens, cols=None):
    if df is None or df.empty:
        return df.iloc[0:0].copy()
    if cols is None:
        cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    else:
        cols = [c for c in cols if c in df.columns]
    if not cols:
        return df.iloc[0:0].copy()

    mask = pd.Series(True, index=df.index)
    for tok in tokens:
        tok_mask = pd.Series(False, index=df.index)
        for c in cols:
            tok_mask |= df[c].astype("string").str.contains(tok, case=False, na=False, regex=False)
        mask &= tok_mask
    return df.loc[mask].copy()

def _extract_location_candidates(df, source_table):
    if df is None or df.empty:
        return pd.DataFrame(columns=[
            "building_key", "floor", "room", "_source_table", "_source_priority",
            "_office_score", "_fiscal_period"
        ])

    idx = df.index
    building = pd.Series(pd.NA, index=idx, dtype="object")
    floor = pd.Series(pd.NA, index=idx, dtype="object")
    room = pd.Series(pd.NA, index=idx, dtype="object")

    for c in ["BUILDING_KEY", "FCLT_BUILDING_KEY"]:
        if c in df.columns:
            building = building.fillna(_clean_series(df[c]))

    for c in ["FLOOR"]:
        if c in df.columns:
            floor = floor.fillna(_clean_series(df[c]))

    for c in ["FCLT_FLOOR_KEY", "FLOOR_KEY"]:
        if c in df.columns:
            vals = _clean_series(df[c])
            vals = vals.str.replace(r"^[^-]+-", "", regex=True)
            floor = floor.fillna(vals)

    for c in ["ROOM", "ROOM_NUMBER"]:
        if c in df.columns:
            room = room.fillna(_clean_series(df[c]))

    for c in ["BUILDING_ROOM", "BUILDING_ROOM_NAME", "FCLT_ROOM_KEY", "fac_room_key"]:
        if c in df.columns:
            parsed = _clean_series(df[c]).str.extract(r"^\s*([^-]+)-(.+?)\s*$")
            building = building.fillna(parsed[0])
            room = room.fillna(parsed[1])

    obj_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    if obj_cols:
        row_text = df[obj_cols].astype("string").fillna("").agg(" ".join, axis=1).str.lower()
        office_score = (
            row_text.str.contains("office", na=False).astype(int)
            + row_text.str.contains("professor", na=False).astype(int)
        )
    else:
        office_score = pd.Series(0, index=idx)

    if "MAJOR_USE_DESC" in df.columns:
        office_score = office_score + df["MAJOR_USE_DESC"].astype("string").str.contains("office", case=False, na=False).astype(int)

    source_priority = {
        "table_5": 0,
        "table_6": 1,
        "table_7": 2,
        "table_9": 9,
    }.get(source_table, 5)

    fiscal_period = df["FISCAL_PERIOD"] if "FISCAL_PERIOD" in df.columns else pd.Series(pd.NA, index=idx)

    out = pd.DataFrame({
        "building_key": building,
        "floor": floor,
        "room": room,
        "_source_table": source_table,
        "_source_priority": source_priority,
        "_office_score": office_score,
        "_fiscal_period": fiscal_period
    })

    return out.dropna(subset=["building_key", "room"], how="any")

matched_frames = []
for table_name, df in tables.items():
    if table_name == "table_9":
        continue
    if len(df) <= 100000:
        m = _token_match(df, tokens)
        if not m.empty:
            matched_frames.append((table_name, m))

candidate_frames = [_extract_location_candidates(m, t) for t, m in matched_frames]
candidates = pd.concat(candidate_frames, ignore_index=True) if candidate_frames else pd.DataFrame()

if candidates.empty and "table_9" in tables:
    hist_match = _token_match(tables["table_9"], tokens, cols=["ROOM_FULL_NAME"])
    candidates = _extract_location_candidates(hist_match, "table_9")

# If floor is missing, look it up from current room tables.
lookup_frames = []
for t in ["table_5", "table_6", "table_7"]:
    if t in tables:
        lk = _extract_location_candidates(tables[t], t)[["building_key", "room", "floor"]]
        lk = lk.dropna(subset=["building_key", "room"]).drop_duplicates(["building_key", "room"])
        lookup_frames.append(lk)

if lookup_frames and not candidates.empty:
    room_lookup = pd.concat(lookup_frames, ignore_index=True).drop_duplicates(["building_key", "room"])
    candidates = candidates.merge(
        room_lookup.rename(columns={"floor": "_lookup_floor"}),
        on=["building_key", "room"],
        how="left"
    )
    candidates["floor"] = candidates["floor"].fillna(candidates["_lookup_floor"])
    candidates = candidates.drop(columns=["_lookup_floor"])

if not candidates.empty:
    candidates["building_key"] = candidates["building_key"].astype("string").str.strip()
    candidates["room"] = candidates["room"].astype("string").str.strip()
    candidates["floor"] = candidates["floor"].astype("string").str.strip()

    candidates = candidates.sort_values(
        ["_source_priority", "_office_score", "_fiscal_period"],
        ascending=[True, False, False],
        na_position="last"
    )

    min_priority = candidates["_source_priority"].min()
    candidates = candidates[candidates["_source_priority"] == min_priority]

    if min_priority >= 9 and candidates["_fiscal_period"].notna().any():
        candidates = candidates[candidates["_fiscal_period"] == candidates["_fiscal_period"].max()]

    candidates = candidates.drop_duplicates(["building_key", "floor", "room"])

# Building street address
buildings = tables["table_2"].copy()
buildings = buildings.rename(columns={
    "BUILDING_KEY": "building_key",
    "BUILDING_STREET_ADDRESS": "building_street_address"
})
buildings["building_key"] = buildings["building_key"].astype("string").str.strip()
buildings = buildings[["building_key", "building_street_address"]].drop_duplicates("building_key")

def _make_street_address(df):
    parts = ["STREET_NUMBER", "STREET_NUMBER_SUFFIX", "PRE_DIRECTIONAL", "STREET_NAME", "STREET_SUFFIX", "POST_DIRECTIONAL"]
    for c in parts:
        if c not in df.columns:
            df[c] = pd.NA

    def join_parts(row):
        vals = []
        for v in row:
            if pd.notna(v):
                s = str(v).strip()
                if s and s.lower() != "nan":
                    vals.append(s)
        return " ".join(vals) if vals else pd.NA

    return df[parts].apply(join_parts, axis=1)

address_frames = []
for t in ["table_1", "table_4"]:
    if t in tables:
        a = tables[t].copy()
        key_col = "BUILDING_KEY" if "BUILDING_KEY" in a.columns else "FCLT_BUILDING_KEY"
        if key_col in a.columns:
            a["building_key"] = a[key_col].astype("string").str.strip()
            a["addr_street"] = _make_street_address(a)
            a["_address_priority"] = (
                a["ADDRESS_PURPOSE"].astype("string").str.upper()
                .map({"STREET": 0, "E911_1": 1, "MAIL": 2})
                .fillna(99)
            )
            address_frames.append(a[[
                "building_key", "addr_street", "CITY", "STATE", "POSTAL_CODE", "_address_priority"
            ]])

if address_frames:
    addresses = pd.concat(address_frames, ignore_index=True)
    addresses = addresses.sort_values("_address_priority").drop_duplicates("building_key")
    addresses = addresses.rename(columns={
        "CITY": "city",
        "STATE": "state",
        "POSTAL_CODE": "postal_code"
    })
    addresses = addresses[["building_key", "addr_street", "city", "state", "postal_code"]]
else:
    addresses = pd.DataFrame(columns=["building_key", "addr_street", "city", "state", "postal_code"])

def _fmt_postal(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if re.fullmatch(r"\d+\.0", s):
        s = s.split(".")[0]
    if s.isdigit() and len(s) <= 5:
        return s.zfill(5)
    return s

if candidates.empty:
    final = pd.DataFrame(columns=[
        "room", "floor", "building_key", "building_street_address", "city", "state", "postal_code"
    ])
else:
    final = (
        candidates[["room", "floor", "building_key"]]
        .merge(buildings, on="building_key", how="left")
        .merge(addresses, on="building_key", how="left")
    )
    final["building_street_address"] = final["building_street_address"].fillna(final["addr_street"])
    final["postal_code"] = final["postal_code"].apply(_fmt_postal)
    final = final[[
        "room", "floor", "building_key", "building_street_address", "city", "state", "postal_code"
    ]].drop_duplicates().reset_index(drop=True)

result = {"professor_summer_haynes_office": final}
