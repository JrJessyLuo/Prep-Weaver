import pandas as pd

# Access pre-loaded tables
df_conf = tables['table_1']
df_roles = tables['table_2']
df_institution = tables['table_3']
df_staff = tables['table_4']

# Parse ConfName_Year into ConfName and Year (split on '#', normalize case)
conf_split = df_conf["ConfName_Year"].str.split("#", n=1, expand=True)
df_conf = df_conf.copy()
df_conf["ConfName"] = conf_split[0].str.lower()
df_conf["Year"] = pd.to_numeric(conf_split[1], errors="coerce")

# Group df_roles by Conference_ID to count participants
participants = (
    df_roles.groupby("Conference_ID", dropna=False)
    .size()
    .reset_index(name="participants")
)

# Left-join participants back to df_conf
merged = df_conf.merge(participants, on="Conference_ID", how="left")

# If no participants found for a conference, fill with 0
merged["participants"] = merged["participants"].fillna(0).astype(int)

# Select requested columns
final_result = merged[["Conference_ID", "ConfName", "Year", "participants"]]

# Package into result dict as required
result = {"conference_participants": final_result}