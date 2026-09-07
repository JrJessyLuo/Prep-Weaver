import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Pivot key-value song metadata to wide format
songs = (
    t1.pivot_table(index="id", columns="attribute", values="value", aggfunc="first")
      .reset_index()
)

# Normalize text fields
if "name" in songs.columns:
    songs["name_norm"] = songs["name"].astype(str).str.strip()
else:
    songs["name_norm"] = ""

if "language" in songs.columns:
    songs["language_norm"] = songs["language"].astype(str).str.strip()
else:
    songs["language_norm"] = ""

# Find song id for 'The Balkan Girls' in English
target_song_ids = songs.loc[
    (songs["name_norm"].eq("The Balkan Girls")) &
    (songs["language_norm"].str.contains(r"\bEnglish\b", case=False, na=False)),
    "id"
].unique()

# Get VSQ scores received for that song
out = (
    t2[t2["songs_id"].isin(target_song_ids)][["participant_id", "vsq"]]
    .sort_values(["participant_id", "vsq"], kind="mergesort")
    .reset_index(drop=True)
)

result = {"voice_sound_quality_scores": out}
