import pandas as pd

# Tables are already loaded in-scope as `tables`
cards_df = tables["table_1"]   # bird_78872802_input_0.pkl
sets_df = tables["table_6"]    # card_games_sets.pkl

target_name = "Hauptset Zehnte Edition"

# Verify the correct setCode for the exact set name
match = sets_df.loc[sets_df["name"] == target_name, ["id", "name", "code"]]
if match.empty:
    raise ValueError(f'No set found with name == "{target_name}".')
if len(match) > 1:
    raise ValueError(f'Multiple sets found with name == "{target_name}":\n{match}')

set_code = match["code"].iloc[0]

# Count with exact artist match (same as reference code)
count_exact_artist = cards_df.loc[
    (cards_df["setCode"] == set_code) & (cards_df["artist"] == "Adam Rex")
].shape[0]

# Final answer table
answer_df = pd.DataFrame(
    {"count_designed_by_adam_rex": [int(count_exact_artist)]}
)

result = {"answer": answer_df}