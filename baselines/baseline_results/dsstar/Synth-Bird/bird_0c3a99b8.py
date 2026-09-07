import pandas as pd

# Tables are preloaded in `tables`
outcomes = tables["table_1"]  # bird_0c3a99b8_input_0.pkl
labs = tables["table_2"]      # bird_0c3a99b8_input_1.pkl

# -----------------------------
# Derive "normal anti-SM" patient ID set (same logic as reference code)
# -----------------------------
sm = labs["SM"]
sm_str = sm.astype("string")
sm_norm = (
    sm_str
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
    .str.lower()
)

normal_tokens = {
    "", "-", "—", "–",
    "neg", "negative",
    "0", "0.0",
    "(-)", "( - )",
}

is_blank = sm_norm.isna() | (sm_norm == "")
is_token_normal = sm_norm.isin(normal_tokens)
is_threshold_normal = sm_norm.str.match(r"^<\s*\d+(\.\d+)?$", na=False)

is_normal = is_blank | is_token_normal | is_threshold_normal

normal_sm_patient_ids = pd.Index(
    labs.loc[is_normal, "ID"]
    .dropna()
    .astype("int64")
    .unique()
).sort_values()

# -----------------------------
# Filter outcomes to normal-SM IDs and compute patient-level "no thrombosis" count
# -----------------------------
outcomes_f = outcomes.loc[outcomes["ID"].notna()].copy()
outcomes_f["ID"] = outcomes_f["ID"].astype("int64")

outcomes_normal_sm = outcomes_f.loc[outcomes_f["ID"].isin(normal_sm_patient_ids)].copy()

any_thrombosis_per_id = (
    outcomes_normal_sm
    .groupby("ID")["Thrombosis"]
    .apply(lambda s: (s == 1).any())
)

n_no_thrombosis_ids = int((~any_thrombosis_per_id).sum())

answer_df = pd.DataFrame(
    {"patients_with_normal_anti_SM_and_no_thrombosis": [n_no_thrombosis_ids]}
)

result = {"answer": answer_df}