import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Keep only schools with valid count of >=1500 scorers
t1_s = t1[(t1["rtype"] == "S") & (t1["NumGE1500"].notna())].copy()

# Pick the school with the highest number of test takers scoring >=1500 (tie-breaker: more total test takers)
top_row = (
    t1_s.sort_values(["NumGE1500", "NumTstTakr"], ascending=[False, False])
        .head(1)
)

# Join to get administrator email
top_row["cds"] = pd.to_numeric(top_row["cds"], errors="coerce").astype("Int64")
t2["CDSCode"] = pd.to_numeric(t2["CDSCode"], errors="coerce").astype("Int64")

merged = top_row.merge(t2, left_on="cds", right_on="CDSCode", how="left")

# Best available admin email
email_cols = [c for c in ["AdmEmail1", "AdmEmail2", "AdmEmail3"] if c in merged.columns]
merged["administrator_email"] = merged[email_cols].bfill(axis=1).iloc[:, 0] if email_cols else pd.NA

# School name (prefer Table 2, else build from Table 1 prefix/suffix)
merged["school_name"] = merged.get("School")
if "school_name" not in merged.columns:
    merged["school_name"] = pd.NA
merged["school_name"] = merged["school_name"].fillna(
    (merged["sname_prefix"].fillna("").astype(str).str.strip() + " " +
     merged["sname_suffix"].fillna("").astype(str).str.strip()).str.strip().replace("", pd.NA)
)

out = merged[["school_name", "administrator_email"]].head(1).reset_index(drop=True)

result = {"school_admin_email_for_top_1500_plus": out}
