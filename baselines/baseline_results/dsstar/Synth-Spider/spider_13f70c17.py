import pandas as pd

# Access preloaded tables
df_songs = tables['table_1']  # songs
df_metrics = tables['table_2']  # metrics
df_participants = tables['table_3']  # participants

# Filter Metrics DF to rows with rhythm_tempo > 5 (as in reference logic)
df_metrics_filtered = df_metrics[df_metrics['rhythm_tempo'] > 5].copy()

# Aggregate by participant_id to compute the maximum voice_sound_quality per participant_id
df_max_voice_quality = (
    df_metrics_filtered
    .groupby('participant_id', as_index=False)['voice_sound_quality']
    .max()
    .rename(columns={'voice_sound_quality': 'max_voice_sound_quality'})
)

# Join participants.id to metrics.participant_id (inferred in reference)
df_joined = df_max_voice_quality.merge(
    df_participants[['id', 'name']],
    left_on='participant_id',
    right_on='id',
    how='left'
).drop(columns=['id'])

# Join with songs on songs.id = participant_id to get original_artist
df_joined = df_joined.merge(
    df_songs[['id', 'original_artist']],
    left_on='participant_id',
    right_on='id',
    how='left'
).drop(columns=['id'])

# Prepare final answer: original artists with rhythm_tempo > 5, ordered by voice sound quality desc
final_df = (
    df_joined[['original_artist', 'max_voice_sound_quality']]
    .sort_values(by='max_voice_sound_quality', ascending=False)
    .reset_index(drop=True)
)

result = {"original_artists_by_voice_quality": final_df}