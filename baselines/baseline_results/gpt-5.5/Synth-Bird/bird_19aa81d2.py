import pandas as pd

# --- Zip -> state lookup from table_1 (wide columns are zip codes) ---
t1 = tables["table_1"].copy()

state_row = t1.loc[t1["zip_code"].astype(str).str.lower().eq("state")]
zip_to_state = (
    state_row.drop(columns=["zip_code"])
    .melt(var_name="zip_code", value_name="state")
    .dropna(subset=["state"])
)

def norm_zip(s):
    s = s.astype(str).str.replace(r"\D", "", regex=True)
    s = s.str.lstrip("0")
    s = s.mask(s.eq(""), pd.NA)
    return s

zip_to_state["zip_code_norm"] = norm_zip(zip_to_state["zip_code"])
zip_to_state = zip_to_state.dropna(subset=["zip_code_norm"]).drop_duplicates("zip_code_norm")

# --- Members table (key-value) -> wide, then find hometown zip field ---
t2 = tables["table_2"].copy()
members = (
    t2.pivot_table(index="member_id", columns="attribute", values="value", aggfunc="first")
    .reset_index()
)

# Choose a likely hometown zip column
cols = [c for c in members.columns if c != "member_id"]
cands = [c for c in cols if ("zip" in str(c).lower() and ("home" in str(c).lower() or "town" in str(c).lower()))]
if not cands:
    cands = [c for c in cols if "zip" in str(c).lower()]
hometown_zip_col = cands[0] if cands else None

if hometown_zip_col is None:
    md_count = 0
else:
    members["zip_code_norm"] = norm_zip(members[hometown_zip_col])

    md_members = members.merge(
        zip_to_state[["zip_code_norm", "state"]],
        on="zip_code_norm",
        how="left"
    )

    md_count = md_members.loc[md_members["state"].astype(str).str.lower().eq("maryland"), "member_id"].nunique()

result = {
    "maryland_hometown_member_count": pd.DataFrame(
        {"number_of_members": [md_count]}
    )
}
