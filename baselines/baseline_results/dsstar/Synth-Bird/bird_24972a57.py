import pandas as pd

# Load input tables from the provided `tables` dict
df_tests = tables["table_1"]  # bird_24972a57_input_0.pkl
df_dir = tables["table_2"]    # bird_24972a57_input_1.pkl

# Filter school directory to MailCity == "Fresno"
filtered_df = df_dir[df_dir["MailCity"] == "Fresno"].copy()

# Deduplicate test-taker dataframe by cds (to avoid double-counting)
df_tests_dedup = df_tests.drop_duplicates(subset=["cds"])

# Inner merge on CDSCode == cds, then sum NumTstTakr
merged = filtered_df.merge(df_tests_dedup, left_on="CDSCode", right_on="cds", how="inner")
num_test_takers_sum = merged["NumTstTakr"].sum()

# Final answer as a DataFrame, stored in `result` dict
answer_df = pd.DataFrame({"num_test_takers": [num_test_takers_sum]})
result = {"fresno_test_takers": answer_df}