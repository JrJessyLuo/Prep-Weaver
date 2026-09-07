import pandas as pd

df_conf = tables["table_1"].copy()
df_part = tables["table_2"].copy()

# Clean Conference_ID values (remove surrounding quotes)
for df in (df_conf, df_part):
    df["Conference_ID"] = (
        df["Conference_ID"]
        .astype(str)
        .str.strip()
        .str.strip('"')
    )

# Parse conference name and year from ConfName_Year (e.g., "acl#2003", " Naccl #2003")
conf_clean = df_conf["ConfName_Year"].astype(str).str.strip()
parts = conf_clean.str.split("#", n=1, expand=True)

df_conf["conference_name"] = parts[0].astype(str).str.strip()
df_conf["year"] = pd.to_numeric(parts[1].astype(str).str.strip(), errors="coerce").astype("Int64")

# Count participants per conference (distinct staff)
participants = (
    df_part.groupby("Conference_ID", as_index=False)
    .agg(number_of_participants=("staff_ID", "nunique"))
)

out = df_conf.merge(participants, on="Conference_ID", how="left")
out["number_of_participants"] = out["number_of_participants"].fillna(0).astype(int)

out = out.rename(columns={"Conference_ID": "conference_id"})
out = out[["conference_id", "conference_name", "year", "number_of_participants"]].sort_values(
    ["conference_id"]
).reset_index(drop=True)

result = {"conference_participants_by_conference": out}
