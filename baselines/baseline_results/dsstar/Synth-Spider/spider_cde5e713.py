import pandas as pd

# Access pre-loaded tables
df0 = tables['table_1']  # people: ['sid','name','rating','age']
df1 = tables['table_2']  # boats: ['bid','Legacy','Mars','Melon']
df2 = tables['table_3']  # bookings: ['xh','bh','day']

# Filter people with age between 20 and 30 inclusive to get their sids
filtered_sids = df0.loc[df0["age"].between(20, 30, inclusive="both"), "sid"]

# Join bookings with filtered people (xh matches sid)
bookings_filtered = df2[df2["xh"].isin(filtered_sids)]

# Map boat id (bh) to boat name by collapsing boat columns into a single 'boat_name'
# Each row in df1 has exactly one non-null among ['Legacy','Mars','Melon'] indicating the boat name.
boat_name_series = df1.set_index('bid')[['Legacy', 'Mars', 'Melon']].stack(dropna=True)
boat_name_series = boat_name_series.reset_index()
boat_name_series.columns = ['bid', 'col', 'boat_name']
boat_names = boat_name_series[['bid', 'boat_name']]

# Merge bookings with boat names on boat id
merged = bookings_filtered.merge(boat_names, left_on='bh', right_on='bid', how='left')

# Select distinct boat names booked by the filtered people
answer_df = merged[['boat_name']].dropna().drop_duplicates().reset_index(drop=True)

# Prepare final result mapping
result = {"boats_booked_by_age_20_30": answer_df}