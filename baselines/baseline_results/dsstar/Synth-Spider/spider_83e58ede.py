import pandas as pd

# Step 1: Load provided DataFrames from `tables`
input0 = tables['table_1']  # spider_83e58ede_input_0.pkl
input1 = tables['table_2']  # spider_83e58ede_input_1.pkl
input2 = tables['table_3']  # spider_83e58ede_input_2.pkl
# tables['table_4'] not needed for this query

# Step 2: Identify Game_ID for the title "Super Mario World"
games = input0.copy()
target_games = games[games['Title'] == 'Super Mario World'][['Game_ID']]

# Step 3: Clean Player_ID in input_2 and filter for those who played the target game(s)
pmap = input2.copy()
pmap['Player_ID'] = pmap['Player_ID'].astype(str).str.strip('"')
players_for_game = pmap.merge(target_games, on='Game_ID', how='inner')

# Step 4: Reshape input_1 so years map to player metadata (Player_name, Rank_of_the_year)
meta_t = input1.set_index('Player_ID').T
meta_t.index = meta_t.index.map(str)  # ensure index (years) are strings to match Player_ID

# Step 5: Join to get names and ranks for the matched Player_IDs
players_for_game = players_for_game.merge(
    meta_t[['Player_name', 'Rank_of_the_year']],
    left_on='Player_ID',
    right_index=True,
    how='left'
)

# Step 6: Select and deduplicate final columns
final_df = players_for_game[['Player_name', 'Rank_of_the_year']].drop_duplicates().reset_index(drop=True)

# Package result
result = {
    'players_and_ranks_for_super_mario_world': final_df
}