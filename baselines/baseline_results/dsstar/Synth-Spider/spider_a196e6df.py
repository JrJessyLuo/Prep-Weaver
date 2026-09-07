import pandas as pd

# Access pre-loaded tables
df0 = tables['table_1']
df1 = tables['table_2']
df_participants = tables['table_3']

# Step A: locate song id(s) for 'The Balkan Girls'
mask_name = (df0["attribute"].astype(str) == "name") & (df0["value"].astype(str) == "The Balkan Girls")
song_ids = df0.loc[mask_name, "id"].dropna().unique()

# Step B: among those ids, keep only those whose language includes 'English'
lang_mask = (df0["attribute"].astype(str).str.lower() == "language")
df0_lang = df0[lang_mask].copy()
df0_lang["value_norm"] = df0_lang["value"].astype(str).str.lower()
eligible_ids = []
for sid in song_ids:
    langs = df0_lang.loc[df0_lang["id"] == sid, "value_norm"].tolist()
    if any("english" in l for l in langs):
        eligible_ids.append(sid)
eligible_ids = pd.unique(pd.Series(eligible_ids))

# Step C: filter DF1 by songs_id in eligible_ids and extract vsq scores
answer_df = df1[df1["songs_id"].isin(eligible_ids)][["participant_id", "songs_id", "vsq", "rt", "sp"]].copy()

# Optional: join participant names if available
if not answer_df.empty and "id" in df_participants.columns:
    answer_df = answer_df.merge(df_participants.rename(columns={"id": "participant_id"}),
                                on="participant_id", how="left")

# Prepare final result mapping as required
result = {"vsq_scores_for_The_Balkan_Girls_English": answer_df}