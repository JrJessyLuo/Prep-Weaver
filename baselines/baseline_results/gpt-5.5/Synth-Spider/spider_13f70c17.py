import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Join songs to their ratings (participant_id corresponds to table_1.id)
df = t2.merge(t1, left_on="participant_id", right_on="id", how="inner")

# Filter songs with rhythm tempo above 5
df = df[df["rhythm_tempo"] > 5]

# For each original artist, keep the best (max) voice sound quality among qualifying songs
out = (
    df.groupby("original_artist", as_index=False)["voice_sound_quality"]
      .max()
      .sort_values("voice_sound_quality", ascending=False, kind="mergesort")
      .reset_index(drop=True)
)

result = {"original_artists_by_voice_sound_quality": out}
