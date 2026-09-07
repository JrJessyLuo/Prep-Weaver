import pandas as pd

# Helper to safely search text
def contains_needle(series, needle):
    return series.astype(str).str.lower().str.contains(needle, na=False)

# 1) Search current FCLT_ROOMS for 'haynes' in ROOM_FULL_NAME or ORGANIZATION_NAME
fclt_rooms = tables['table_6'].copy()

for col in ["ROOM_FULL_NAME", "ORGANIZATION_NAME"]:
    if col not in fclt_rooms.columns:
        fclt_rooms[col] = pd.NA

needle = "haynes"
mask_current = contains_needle(fclt_rooms["ROOM_FULL_NAME"], needle) | contains_needle(fclt_rooms["ORGANIZATION_NAME"], needle)
matches_current = fclt_rooms.loc[mask_current].copy()

# If nothing in current, look into historical to expand candidates
fclt_rooms_hist = tables['table_9'].copy()
for col in ["ROOM_FULL_NAME", "ORGANIZATION_NAME"]:
    if col not in fclt_rooms_hist.columns:
        fclt_rooms_hist[col] = pd.NA
mask_hist = contains_needle(fclt_rooms_hist["ROOM_FULL_NAME"], needle) | contains_needle(fclt_rooms_hist["ORGANIZATION_NAME"], needle)
matches_hist = fclt_rooms_hist.loc[mask_hist].copy()

# If both current and hist are empty, we cannot find via simple 'haynes' keyword.
# Try to find "Summer Haynes" specifically in ROOM_FULL_NAME or ORGANIZATION_NAME
if len(matches_current) == 0 and len(matches_hist) == 0:
    needle_full = "summer haynes"
    mask_current = contains_needle(fclt_rooms["ROOM_FULL_NAME"], needle_full) | contains_needle(fclt_rooms["ORGANIZATION_NAME"], needle_full)
    matches_current = fclt_rooms.loc[mask_current].copy()
    mask_hist = contains_needle(fclt_rooms_hist["ROOM_FULL_NAME"], needle_full) | contains_needle(fclt_rooms_hist["ORGANIZATION_NAME"], needle_full)
    matches_hist = fclt_rooms_hist.loc[mask_hist].copy()

# Prefer current matches; if none, fallback to most recent historical
if len(matches_current) > 0:
    candidates = matches_current.copy()
else:
    # Choose the most recent fiscal period per room/building if available
    if "FISCAL_PERIOD" in matches_hist.columns and len(matches_hist) > 0:
        # Sort by fiscal period descending to get latest first
        matches_hist_sorted = matches_hist.sort_values(by="FISCAL_PERIOD", ascending=False)
        # Keep latest per FCLT_ROOM_KEY if present, else per (FCLT_BUILDING_KEY, ROOM)
        if "FCLT_ROOM_KEY" in matches_hist_sorted.columns:
            candidates = matches_hist_sorted.drop_duplicates(subset=["FCLT_ROOM_KEY"], keep="first").copy()
        elif set(["FCLT_BUILDING_KEY", "ROOM"]).issubset(matches_hist_sorted.columns):
            candidates = matches_hist_sorted.drop_duplicates(subset=["FCLT_BUILDING_KEY", "ROOM"], keep="first").copy()
        else:
            candidates = matches_hist_sorted.copy()
    else:
        candidates = matches_hist.copy()

# If still empty, there is no match
if len(candidates) == 0:
    answer_df = pd.DataFrame(columns=[
        "ROOM", "FLOOR", "FCLT_BUILDING_KEY", "STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"
    ])
else:
    # Normalize columns to join with building address
    # Ensure we have required columns
    for col in ["ROOM", "FLOOR", "FCLT_BUILDING_KEY"]:
        if col not in candidates.columns:
            candidates[col] = pd.NA

    # Pull building address from FCLT_BUILDING_ADDRESS first, then FAC_BUILDING_ADDRESS as fallback
    fclt_baddr = tables['table_4'].copy()  # FCLT_BUILDING_ADDRESS.pkl
    # Standardize address columns
    # Expect columns like: FCLT_BUILDING_KEY, ADDRESS_1, CITY, STATE, POSTAL_CODE (names may vary)
    # Try to coalesce common variants
    def coalesce_address(df):
        out = pd.DataFrame()
        if "FCLT_BUILDING_KEY" in df.columns:
            out["FCLT_BUILDING_KEY"] = df["FCLT_BUILDING_KEY"]
        elif "FAC_BUILDING_KEY" in df.columns:
            out["FCLT_BUILDING_KEY"] = df["FAC_BUILDING_KEY"]
        else:
            out["FCLT_BUILDING_KEY"] = pd.NA

        def pick(*names):
            for n in names:
                if n in df.columns:
                    return df[n]
            return pd.Series(pd.NA, index=df.index)

        out["STREET_ADDRESS"] = pick("ADDRESS_1", "ADDRESS_LINE1", "STREET_ADDRESS")
        out["CITY"] = pick("CITY")
        out["STATE"] = pick("STATE")
        out["POSTAL_CODE"] = pick("POSTAL_CODE", "ZIP", "ZIP_CODE")
        return out

    addr_primary = coalesce_address(fclt_baddr)

    # Fallback to FAC_BUILDING_ADDRESS if needed
    fac_baddr = tables['table_1'].copy()
    addr_fallback = coalesce_address(fac_baddr)

    # Prefer primary; where missing, fill from fallback matching on FCLT_BUILDING_KEY
    addr = addr_primary.copy()
    if "FCLT_BUILDING_KEY" not in addr.columns:
        addr["FCLT_BUILDING_KEY"] = pd.NA
    if len(addr_fallback) > 0:
        addr = addr.merge(
            addr_fallback.add_suffix("_fb"),
            left_on="FCLT_BUILDING_KEY",
            right_on="FCLT_BUILDING_KEY_fb",
            how="left"
        )
        # Fill nulls from fallback
        for col in ["STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"]:
            base = col
            fb = f"{col}_fb"
            if base in addr.columns and fb in addr.columns:
                addr[base] = addr[base].fillna(addr[fb])
        # Drop fallback columns and duplicate key
        drop_cols = [c for c in addr.columns if c.endswith("_fb")]
        addr = addr.drop(columns=drop_cols)
    # Deduplicate addresses in case of multiple address records
    addr = addr.drop_duplicates(subset=["FCLT_BUILDING_KEY"])

    # Build final answer by joining candidates to address
    final_cols = ["ROOM", "FLOOR", "FCLT_BUILDING_KEY"]
    answer = candidates.copy()
    answer = answer[final_cols].drop_duplicates()
    answer = answer.merge(addr, on="FCLT_BUILDING_KEY", how="left")

    # Keep only necessary columns and sort for readability
    answer_df = answer[["ROOM", "FLOOR", "FCLT_BUILDING_KEY", "STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"]].drop_duplicates()

# Package final result under a descriptive key
result = {
    "Professor Summer Haynes Office Location": answer_df
}