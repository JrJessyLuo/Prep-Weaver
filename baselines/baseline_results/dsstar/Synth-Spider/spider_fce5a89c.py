import pandas as pd

# Access pre-loaded tables
df_sailors = tables['table_1']
df_reserves = tables['table_2']
df_boats = tables['table_3']  # Not strictly needed for this query, but available

# Filter sailors with rating at least 3
eligible_sailors = df_sailors[df_sailors['rtg'] >= 3]

# Identify sailors who reserved a boat by joining with reserves
sailors_with_reservations = eligible_sailors.merge(
    df_reserves, left_on='s_id', right_on='sid', how='inner'
)

# Select distinct sailor id and name
answer_df = sailors_with_reservations[['s_id', 'name']].drop_duplicates().sort_values(['s_id', 'name']).reset_index(drop=True)

# Prepare final result mapping
result = {
    'sailors_with_rtg_at_least_3_and_reserved': answer_df
}