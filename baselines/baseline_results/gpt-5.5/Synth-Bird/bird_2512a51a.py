import pandas as pd

# --- Parse key-value patient table (table_1) into wide format ---
t1 = tables["table_1"].copy()

parts = t1["merged_ID_Attribute_Value"].astype(str).str.split(r"\|\|\|", n=2, expand=True)
parts.columns = ["ID", "Attribute", "Value"]
parts["ID"] = parts["ID"].str.strip().str.strip('"').str.strip()
parts["Attribute"] = parts["Attribute"].str.strip()
parts["Value"] = parts["Value"].astype(str).str.strip()

meta = (
    parts.pivot_table(index="ID", columns="Attribute", values="Value", aggfunc="first")
    .reset_index()
)

meta["ID"] = pd.to_numeric(meta["ID"], errors="coerce")
meta["Birthday"] = pd.to_datetime(meta.get("Birthday"), errors="coerce")

# --- Identify male patients with ALB out of typical range ---
labs = tables["table_2"].copy()
labs["ID"] = pd.to_numeric(labs["ID"], errors="coerce")

alb_low, alb_high = 3.5, 5.0
abn_ids = labs.loc[
    labs["ALB"].notna() & ((labs["ALB"] < alb_low) | (labs["ALB"] > alb_high)),
    "ID",
].dropna().unique()

out = meta.loc[
    meta["ID"].isin(abn_ids)
    & meta.get("SEX", pd.Series(index=meta.index, dtype=object)).astype(str).str.upper().eq("M"),
    ["ID", "Birthday"],
].dropna(subset=["Birthday"]).sort_values("Birthday", ascending=False).reset_index(drop=True)

result = {"male_patients_albumin_out_of_range_sorted_by_birthday": out}
