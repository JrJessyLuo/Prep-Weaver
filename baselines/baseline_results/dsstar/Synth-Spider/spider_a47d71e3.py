import pandas as pd

# Access pre-loaded tables
df_sailors = tables['table_1']
df_day_sidbid = tables['table_2']
df_boats = tables['table_3']

# Parse sid and bid from 'sid_bid' column in df_day_sidbid
def split_sid_bid(val):
    if pd.isna(val):
        return pd.NA, pd.NA
    parts = str(val).split("_", 1)
    if len(parts) != 2:
        return pd.NA, pd.NA
    sid_part, bid_part = parts
    try:
        sid_int = int(sid_part)
    except ValueError:
        sid_int = pd.NA
    try:
        bid_int = int(bid_part)
    except ValueError:
        bid_int = pd.NA
    return sid_int, bid_int

sid_bid_parsed = df_day_sidbid["sid_bid"].apply(split_sid_bid)
df_day_sidbid = df_day_sidbid.copy()
df_day_sidbid["sid"] = sid_bid_parsed.apply(lambda x: x[0])
df_day_sidbid["bid"] = sid_bid_parsed.apply(lambda x: x[1])

# Determine sailors who have not reserved any boat
reserved_sids = set(df_day_sidbid["sid"].dropna().unique().tolist())
all_sids = set(df_sailors["sid"].unique().tolist())
not_reserved_sids = sorted(list(all_sids - reserved_sids))

# Prepare final answer DataFrame
answer_df = pd.DataFrame({"sid": not_reserved_sids})

# Assign to result mapping
result = {"sailors_without_reservations": answer_df}