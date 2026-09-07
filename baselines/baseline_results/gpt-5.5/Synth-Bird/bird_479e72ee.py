import pandas as pd

# Tables
majors = tables["table_1"].copy()
raw = tables["table_2"].copy()

# Build a column->attribute map from the special "attribute" row
attr_rows = raw.loc[raw["member_id"].astype(str).str.lower().eq("attribute")]
attr_row = attr_rows.iloc[0] if len(attr_rows) else None

col_to_attr = {}
if attr_row is not None:
    for c in raw.columns:
        if c == "member_id":
            continue
        v = attr_row[c]
        if pd.notna(v):
            col_to_attr[c] = str(v)

# Keep only actual member rows (drop the attribute row; also drop a possible "value" header row if present)
members = raw.copy()
members = members[~members["member_id"].astype(str).str.lower().isin(["attribute", "value"])].copy()

# Helper: take first non-null across possibly multiple columns for the same semantic attribute
def first_nonnull_across(df, cols):
    if not cols:
        return pd.Series([pd.NA] * len(df), index=df.index)
    tmp = df[cols].copy()
    # replace string "nan"/"None" with NA
    tmp = tmp.replace({"nan": pd.NA, "None": pd.NA, "": pd.NA})
    return tmp.bfill(axis=1).iloc[:, 0]

tshirt_cols = [c for c, a in col_to_attr.items() if a == "t_shirt_size" and c in members.columns]
major_cols = [c for c, a in col_to_attr.items() if a == "link_to_major" and c in members.columns]

members["t_shirt_size"] = first_nonnull_across(members, tshirt_cols)
members["link_to_major"] = first_nonnull_across(members, major_cols)

# Normalize major link values (can be list-like or scalar)
def norm_major(x):
    if isinstance(x, (list, tuple)):
        return x
    if pd.isna(x):
        return []
    s = str(x).strip()
    if not s:
        return []
    # handle comma-separated / bracketed strings if they occur
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1].strip()
    parts = [p.strip().strip("'").strip('"') for p in s.split(",")] if "," in s else [s]
    return [p for p in parts if p]

members["link_to_major_list"] = members["link_to_major"].apply(norm_major)
members_exploded = members.explode("link_to_major_list", ignore_index=True)

# Identify "Business" majors (by the college/school info stored in majors["value"])
business_major_ids = set(
    majors.loc[majors["value"].astype(str).str.contains("business", case=False, na=False), "record_id"]
)

# Filter: Business members with Medium tee shirt size
mask_business = members_exploded["link_to_major_list"].isin(business_major_ids)
mask_medium = members_exploded["t_shirt_size"].astype(str).str.strip().str.lower().eq("medium")

count_members = members_exploded.loc[mask_business & mask_medium, "member_id"].nunique()

result = {
    "business_medium_t_shirt_member_count": pd.DataFrame(
        {"member_count": [int(count_members)]}
    )
}
