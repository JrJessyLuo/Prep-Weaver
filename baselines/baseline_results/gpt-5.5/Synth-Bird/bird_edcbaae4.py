import pandas as pd

# Load tables
expenses = tables["table_1"].copy()
members_raw = tables["table_2"].copy()

# ---- Find member record id(s) for "Sacha Harrison" ----
member_ids = []

if "member_id" in members_raw.columns and {"attribute", "value"}.issubset(
    set(members_raw["member_id"].astype(str).str.lower().unique())
):
    # table_2 is a transposed 2-row (attribute/value) layout with member record IDs as columns
    m_long = members_raw.melt(id_vars=["member_id"], var_name="member_rec_id", value_name="cell")
    m_wide = (
        m_long.pivot_table(index="member_rec_id", columns="member_id", values="cell", aggfunc="first")
        .reset_index()
    )
    if "value" in m_wide.columns:
        v = m_wide["value"].astype(str)
        mask = v.str.contains(r"\bSacha\b", case=False, na=False) & v.str.contains(r"\bHarrison\b", case=False, na=False)
        member_ids = m_wide.loc[mask, "member_rec_id"].astype(str).unique().tolist()
else:
    # table_2 is a normal (row-per-member) layout; find rows containing both tokens anywhere
    df = members_raw.copy()
    row_text = df.astype(str).agg(" ".join, axis=1)
    mask = row_text.str.contains(r"\bSacha\b", case=False, na=False) & row_text.str.contains(r"\bHarrison\b", case=False, na=False)
    if "member_id" in df.columns:
        member_ids = df.loc[mask, "member_id"].astype(str).unique().tolist()

# ---- Extract "kind of expenses" incurred by that member ----
meta_cols = [c for c in ["expense_id", "expense_date", "approved", "ys"] if c in expenses.columns]

if member_ids and any(mid in expenses.columns for mid in member_ids):
    # member is encoded as a column in expenses (wide person columns)
    member_exp_cols = [mid for mid in member_ids if mid in expenses.columns]
    exp_values = expenses[member_exp_cols].stack(dropna=True)
else:
    # member is encoded in the 'ys' column (link_to_member)
    exp_cols = [c for c in expenses.columns if c not in meta_cols]
    if member_ids and "ys" in expenses.columns:
        exp_values = expenses.loc[expenses["ys"].astype(str).isin(member_ids), exp_cols].stack(dropna=True)
    else:
        exp_values = pd.Series([], dtype=object)

kinds = (
    exp_values.astype(str)
    .str.split("|", n=1, expand=True)[0]
    .str.split(r"\s*[,;]\s*", regex=True)
    .explode()
    .astype(str)
    .str.strip()
)
kinds = kinds[(kinds != "") & (kinds.str.lower() != "nan")].dropna().drop_duplicates().sort_values()

out = pd.DataFrame({"expense_type": kinds.reset_index(drop=True)})

result = {"sacha_harrison_expense_types": out}
