import re
import pandas as pd

# Access pre-loaded tables
df0 = tables['table_1']  # affiliations: affiliation_id (object), name, address
df1 = tables['table_2']  # paper-author-affiliation

# Helper: derive year from paper_id (ACL Anthology style, e.g., D09-1141 -> 2009)
def year_from_paper_id(pid: str):
    if not isinstance(pid, str) or len(pid) < 3:
        return None
    m = re.match(r"^[A-Z]([0-9]{2})", pid)
    if not m:
        m = re.search(r"([0-9]{2})", pid)
    if not m:
        return None
    yy = int(m.group(1))
    if yy <= 24:
        return 2000 + yy
    else:
        return 1900 + yy

# Extract paper_id from df1.paper_author_combined and derive year
def extract_paper_id_from_combined(s: str):
    if not isinstance(s, str):
        return None
    return s.split("||", 1)[0].strip()

df1_work = df1.copy()
df1_work["paper_id"] = df1_work["paper_author_combined"].apply(extract_paper_id_from_combined)
df1_work["year_from_pid"] = df1_work["paper_id"].apply(year_from_paper_id)

# Filter for year 2009
df1_2009 = df1_work[df1_work["year_from_pid"] == 2009].copy()

# Clean affiliation_id: drop NaNs, cast to normalized string to match df0
df1_2009 = df1_2009[df1_2009["affiliation_id"].notna()].copy()

def norm_aff_id(x):
    if pd.isna(x):
        return None
    try:
        if isinstance(x, float):
            if x.is_integer():
                return str(int(x))
            else:
                return str(x).strip()
        else:
            s = str(x).strip().strip('"').strip("'")
            if re.fullmatch(r"\d+(\.0+)?", s):
                return str(int(float(s)))
            return s
    except:
        return str(x)

df1_2009["affiliation_id_str"] = df1_2009["affiliation_id"].apply(norm_aff_id)

# Prepare df0 affiliation_id similarly
df0_work = df0.copy()
df0_work["affiliation_id_str"] = df0_work["affiliation_id"].apply(norm_aff_id)

# Count distinct paper_ids per affiliation_id (in 2009)
aff_paper_counts = (
    df1_2009.groupby("affiliation_id_str")["paper_id"]
    .nunique()
    .reset_index(name="distinct_papers_2009")
)

# Join with df0 to map names and addresses
aff_enriched = aff_paper_counts.merge(
    df0_work[["affiliation_id_str", "name", "address"]],
    on="affiliation_id_str",
    how="left"
)

# Sort to get top 3 affiliations by distinct papers in 2009
top3 = aff_enriched.sort_values(
    by=["distinct_papers_2009", "name"],
    ascending=[False, True]
).head(3)

# Prepare final result as required
final_df = top3[["affiliation_id_str", "name", "address", "distinct_papers_2009"]].reset_index(drop=True)

result = {
    "top3_affiliations_2009": final_df
}