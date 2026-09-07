import pandas as pd

df_pat = tables["table_1"].copy()
df_lab = tables["table_2"].copy()

# Clean/standardize
df_pat["SEX"] = df_pat["SEX"].astype(str).str.strip().str.upper()
df_lab["GPT"] = pd.to_numeric(df_lab["GPT"], errors="coerce")

# Define "normal" GPT range (commonly <= 40 U/L)
normal_ids = df_lab.loc[df_lab["GPT"].notna() & (df_lab["GPT"] >= 0) & (df_lab["GPT"] <= 40), "ID"].dropna().unique()

male_count = (
    df_pat.loc[df_pat["ID"].isin(normal_ids)]
    .drop_duplicates(subset=["ID"])
    .loc[lambda d: d["SEX"].eq("M"), "ID"]
    .nunique()
)

result = {
    "male_patients_with_normal_gpt": pd.DataFrame({"male_count": [male_count]})
}
