import pandas as pd
import numpy as np

# Use in-scope table per instructions
df = tables["table_2"]

# Parse Date
date_parsed = pd.to_datetime(df["Date"], errors="coerce", infer_datetime_format=True)

# Restrict to Date < 2000-01-01
pre2000_mask = date_parsed < pd.Timestamp("2000-01-01")
df_pre2000 = df.loc[pre2000_mask].copy()

# Normalize SSA to better capture "normal/negative" encodings
ssa = df_pre2000["SSA"]
ssa_str = ssa.astype("string").str.strip()
ssa_norm = ssa_str.str.upper()
ssa_num = pd.to_numeric(ssa_str, errors="coerce")

negative_tokens = {
    "NEGATIVE", "NEG", "(-)", "-", "N", "NORMAL", "NONREACTIVE", "NON-REACTIVE",
    "NON REACTIVE", "NR", "0", "0.0"
}

normal_ssa_mask_expanded = ssa_num.eq(0) | ssa_norm.isin(negative_tokens)

# Count distinct patients (ID) satisfying conditions
distinct_id_count_expanded = df_pre2000.loc[normal_ssa_mask_expanded, "ID"].nunique(dropna=True)

# Final answer table
answer_df = pd.DataFrame(
    {"patients_with_normal_anti_ssa_before_2000": [int(distinct_id_count_expanded)]}
)

result = {"answer": answer_df}