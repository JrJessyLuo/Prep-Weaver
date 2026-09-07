import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Driver with most races (count appearances in table_2)
race_counts = (
    t2.groupby("Driver_ID", as_index=False)
      .size()
      .rename(columns={"size": "num_races"})
      .sort_values(["num_races", "Driver_ID"], ascending=[False, True])
)

top_driver_id = race_counts.iloc[0]["Driver_ID"]

# Normalize table_1 (key-value lists) and extract Age per driver
t1["Driver_ID"] = (
    t1["siji_id"].astype(str)
      .str.replace('"', '', regex=False)
      .str.strip()
      .astype(int)
)

long = t1.explode(["shuxing", "shuxing_zhi"], ignore_index=True)
age_df = (
    long[long["shuxing"].astype(str).str.lower() == "age"][["Driver_ID", "shuxing_zhi"]]
    .rename(columns={"shuxing_zhi": "Age"})
)
age_df["Age"] = pd.to_numeric(age_df["Age"], errors="coerce")

out = (
    pd.DataFrame({"Driver_ID": [top_driver_id]})
    .merge(age_df.drop_duplicates(subset=["Driver_ID"]), on="Driver_ID", how="left")
)

result = {"driver_with_most_races_age": out}
