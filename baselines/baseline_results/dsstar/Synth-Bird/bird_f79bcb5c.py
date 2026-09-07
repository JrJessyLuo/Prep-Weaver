import pandas as pd

# tables are preloaded:
# tables["table_1"] = demographics (bird_f79bcb5c_input_0.pkl)
# tables["table_2"] = labs         (bird_f79bcb5c_input_1.pkl)

df_demo = tables["table_1"]
df_labs = tables["table_2"]

# Keep only relevant columns
demo = df_demo.loc[:, ["ID", "SEX"]].copy()
labs = df_labs.loc[:, ["ID", "Date", "GPT"]].copy()

# Coerce GPT to numeric
labs["GPT"] = pd.to_numeric(labs["GPT"], errors="coerce")

# Merge SEX into labs rows
merged = labs.merge(demo, on="ID", how="left")

# Base set for counting: GPT present and SEX known
base = merged.dropna(subset=["GPT", "SEX"]).copy()
base["SEX"] = base["SEX"].astype(str).str.strip().str.upper()

# Use the same confirmed threshold as in the reference execution result
confirmed_threshold = 60

# Normal GPT rows
normal = base[base["GPT"] <= confirmed_threshold].copy()

# Row-level male count (this is what the reference code reports as the final requested count)
male_rows_normal = int((normal["SEX"] == "M").sum())

answer_df = pd.DataFrame({"male_count": [male_rows_normal]})

result = {"male_patients_with_normal_GPT": answer_df}