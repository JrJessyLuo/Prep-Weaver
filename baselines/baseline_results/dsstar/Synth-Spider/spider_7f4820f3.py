import pandas as pd

# Source tables from the provided dictionary
boats_df = tables['table_1']
reserves_like_df = tables['table_2']
sailors_df = tables['table_3']

# Reproduce the same logic as the reference code

# Normalize boats: b -> bid, clr -> color
boats_norm = boats_df.rename(columns={"b": "bid", "clr": "color"}).copy()

# Parse reservation-like table into (sid, bid)
def parse_sid_bid_rows(df):
    rows = []
    if df is None or df.empty:
        return rows
    for _, r in df.iterrows():
        sid = r.get("sid")
        dvp = r.get("date_value_pairs")
        if pd.isna(dvp):
            continue
        parts = [p.strip() for p in str(dvp).split(",") if p.strip()]
        for p in parts:
            if ":" not in p:
                continue
            left, right = p.split(":", 1)
            try:
                bid = int(float(right.strip()))
                rows.append({"sid": int(sid), "bid": bid})
            except Exception:
                continue
    return rows

parsed_rows = parse_sid_bid_rows(reserves_like_df)
parsed_reservations = pd.DataFrame(parsed_rows) if parsed_rows else pd.DataFrame(columns=["sid", "bid"])

# Filter reservations where bid in {101, 102, 103} per reference logic
target_bids = {101, 102, 103}
filtered_reservations = parsed_reservations[parsed_reservations["bid"].isin(target_bids)].copy()

# Join with boats to get colors
reservations_with_boats = filtered_reservations.merge(
    boats_norm.rename(columns={"name": "boat_name"})[["bid", "color"]],
    on="bid",
    how="left"
)

# Identify sids who reserved red or blue boats; colors in boats are ' Red ', ' blue ', '_red_'
# Based on reference data, target colors: any containing 'red' or exactly 'blue' (case-insensitive, strip spaces)
def is_red_or_blue(c):
    if pd.isna(c):
        return False
    cs = str(c).strip().lower()
    return ("red" in cs) or (cs == "blue")

reservations_red_blue = reservations_with_boats[reservations_with_boats["color"].apply(is_red_or_blue)]

# Get distinct sids
sids_df = reservations_red_blue[["sid"]].drop_duplicates().sort_values("sid").reset_index(drop=True)

# Prepare final result mapping
result = {"sids_reserved_red_or_blue_boats": sids_df}