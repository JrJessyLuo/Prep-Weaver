import pandas as pd
import numpy as np

# Tables are preloaded in a dict named `tables`
df_hero = tables["table_1"]   # bird_f39cebec_input_0.pkl
df_wide = tables["table_2"]   # bird_f39cebec_input_1.pkl

# Treat every column except 'hero_id' as a power column
power_cols = [c for c in df_wide.columns if c != "hero_id"]

def compute_has_power(series: pd.Series) -> pd.Series:
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    if pd.api.types.is_numeric_dtype(series):
        return series.notna() & (series != 0)
    false_markers = {"0", "false", "no", "n", "", "nan", "none", "null"}
    s = series.astype("string")
    s_norm = s.str.strip().str.lower()
    return series.notna() & (~s_norm.isin(false_markers))

# Recompute power_count using robust per-column rule
has_power_df = pd.DataFrame({"hero_id": df_wide["hero_id"]})
for c in power_cols:
    has_power_df[c] = compute_has_power(df_wide[c]).astype(bool)

power_counts = (
    has_power_df.drop(columns=["hero_id"])
    .sum(axis=1)
    .astype(int)
    .to_frame("power_count")
)
power_counts.insert(0, "hero_id", df_wide["hero_id"].values)

max_power_count = int(power_counts["power_count"].max())
max_power_heroes = power_counts.loc[
    power_counts["power_count"] == max_power_count, ["hero_id", "power_count"]
]

answer_df = (
    max_power_heroes.merge(
        df_hero[["id", "superhero_name"]],
        left_on="hero_id",
        right_on="id",
        how="left",
    )
    .drop(columns=["id"])
    .sort_values(["power_count", "hero_id"], ascending=[False, True])
    .head(1)[["superhero_name"]]
    .reset_index(drop=True)
)

result = {"superhero_with_most_powers": answer_df}
print(result["superhero_with_most_powers"].to_string(index=False))