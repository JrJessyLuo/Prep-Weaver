import pandas as pd
import numpy as np

# Tables are preloaded in scope:
# tables['table_1'] = Admission table
# tables['table_2'] = IGG lab table
df_adm = tables["table_1"]
df_lab = tables["table_2"]

# Ensure needed columns exist
need_adm = {"ID", "Admission"}
need_lab = {"ID", "IGG", "Date"}
missing_adm = need_adm - set(df_adm.columns)
missing_lab = need_lab - set(df_lab.columns)
if missing_adm:
    raise ValueError(f"Missing columns in admission table: {missing_adm}")
if missing_lab:
    raise ValueError(f"Missing columns in lab table: {missing_lab}")

# Clean / coerce types
df_adm = df_adm.copy()
df_lab = df_lab.copy()

df_adm["ID"] = pd.to_numeric(df_adm["ID"], errors="coerce").astype("Int64")
df_lab["ID"] = pd.to_numeric(df_lab["ID"], errors="coerce").astype("Int64")
df_adm["Admission"] = df_adm["Admission"].astype(str).str.strip()
df_lab["IGG"] = pd.to_numeric(df_lab["IGG"], errors="coerce")

# Join on ID (many-to-many allowed; deduplicate to patient level later)
df_join = df_lab[["ID", "Date", "IGG"]].merge(
    df_adm[["ID", "Admission"]],
    on="ID",
    how="inner",
    validate="many_to_many",
)

# Normal reference range for IGG (common adult serum IgG ref range)
IGG_NORMAL_LOW = 700.0
IGG_NORMAL_HIGH = 1600.0

# Patient-level flags
df_flags = (
    df_join.dropna(subset=["ID"])
    .groupby("ID", as_index=False)
    .agg(
        normal_igg=("IGG", lambda s: bool(s.between(IGG_NORMAL_LOW, IGG_NORMAL_HIGH, inclusive="both").any())),
        admitted=("Admission", lambda s: bool((s == "+").any())),
    )
)

# Question: Of the patients with a normal level of IGG, how many were admitted?
count_normal_and_admitted = int(df_flags.loc[df_flags["normal_igg"] & df_flags["admitted"], "ID"].nunique())

answer_df = pd.DataFrame({"normal_igg_and_admitted_patients": [count_normal_and_admitted]})

result = {"answer": answer_df}