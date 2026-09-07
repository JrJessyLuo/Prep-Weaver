import pandas as pd

# Tables are already loaded in-scope as `tables`
pub_list_df = tables["table_1"]   # bird_b0715059_input_0.pkl
heroes = tables["table_2"]        # bird_b0715059_input_1.pkl

# Convert publisher lookup list (columns: bh, mc) into a proper mapping table
bh = pub_list_df.loc[0, "bh"]
mc = pub_list_df.loc[0, "mc"]
publishers = pd.DataFrame({"publisher_id": bh, "publisher_name": mc}).dropna(subset=["publisher_name"])

# Determine the publisher_id for "Dark Horse Comics"
target = "Dark Horse Comics"
match = publishers[publishers["publisher_name"].astype(str).str.strip().eq(target)]
publisher_id = match["publisher_id"].iloc[0] if not match.empty else None

# Count heroes where publisher_id equals that id (excluding nulls)
if publisher_id is None:
    dark_horse_count = 0
else:
    dark_horse_count = heroes.loc[heroes["publisher_id"].notna() & (heroes["publisher_id"] == publisher_id)].shape[0]

# Final answer table
answer_df = pd.DataFrame({"dark_horse_comics_superheroes": [dark_horse_count]})

# Required convention: assign final answer to `result`
result = {"answer": answer_df}

# Print the answer
print(dark_horse_count)