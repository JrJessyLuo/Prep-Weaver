import pandas as pd
import html
import re

# Inputs are provided as DataFrames in the dict `tables`
a0 = tables['table_1'].copy()  # spider_dd201412_input_0.pkl
a1 = tables['table_2'].copy()  # spider_dd201412_input_1.pkl
a2 = tables['table_3'].copy()  # spider_dd201412_input_2.pkl

# Step 1: Parse name_email_combined to clean author_name
def extract_name(val):
    if pd.isna(val):
        return pd.NA
    s = str(val)
    parts = s.split("|", 1)
    name_raw = parts[0].strip()
    if name_raw.lower() == "nan" or name_raw == "":
        return pd.NA
    name = html.unescape(name_raw)
    name = re.sub(r"\s+", " ", name).strip()
    return name if name else pd.NA

a0["author_name"] = a0["name_email_combined"].map(extract_name)

# Step 2: Identify authors who appear in input_1 (published any paper)
author_ids_any_pub = pd.Index(a1["aid"].dropna().astype("int64").unique())

# Step 3: Identify authors who have any paper in venue "ACL" using input_2
venue_col = None
for c in a2.columns:
    if c.lower() == "venue":
        venue_col = c
        break

authors_with_acl = pd.Index([], dtype="int64")
if venue_col is not None:
    acl_papers = set(
        a2.loc[
            a2[venue_col].astype(str).str.strip().str.lower() == "acl",
            "paper_id",
        ].dropna().astype(str).unique()
    )
    if acl_papers:
        a1_nonnull = a1.dropna(subset=["paper_id", "aid"]).copy()
        a1_nonnull["paper_id"] = a1_nonnull["paper_id"].astype(str)
        a1_nonnull["aid"] = a1_nonnull["aid"].astype("int64")
        authors_with_acl = pd.Index(
            a1_nonnull.loc[a1_nonnull["paper_id"].isin(acl_papers), "aid"].unique()
        )
else:
    possible_acl_cols = [c for c in a2.columns if c.lower() == "acl"]
    if possible_acl_cols:
        c = possible_acl_cols[0]
        mask = a2[c].notna() & (a2[c].astype(str).str.strip() != "")
        acl_papers = set(a2.loc[mask, "paper_id"].dropna().astype(str).unique())
        if acl_papers:
            a1_nonnull = a1.dropna(subset=["paper_id", "aid"]).copy()
            a1_nonnull["paper_id"] = a1_nonnull["paper_id"].astype(str)
            a1_nonnull["aid"] = a1_nonnull["aid"].astype("int64")
            authors_with_acl = pd.Index(
                a1_nonnull.loc[a1_nonnull["paper_id"].isin(acl_papers), "aid"].unique()
            )
    else:
        authors_with_acl = pd.Index([], dtype="int64")

# Step 4: Authors who never published in ACL
authors_never_acl_ids = author_ids_any_pub.difference(authors_with_acl)

# Step 5: Attach clean author_name for the result set
a0_small = a0[["author_id", "author_name"]].drop_duplicates()
a0_small["author_id"] = a0_small["author_id"].astype("int64")

final_df = pd.DataFrame({"author_id": authors_never_acl_ids})
final_df = final_df.merge(a0_small, on="author_id", how="left")

# Prepare final result mapping
result = {
    "authors_never_acl": final_df[["author_id", "author_name"]]
}