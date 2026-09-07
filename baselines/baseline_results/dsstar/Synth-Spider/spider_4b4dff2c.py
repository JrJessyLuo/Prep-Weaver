import re
import pandas as pd

# The input tables are already loaded into `tables` dict:
# tables['table_1'] -> spider_4b4dff2c_input_0.pkl (affiliation)
# tables['table_2'] -> spider_4b4dff2c_input_1.pkl (author_affil_paper)
# tables['table_3'] -> spider_4b4dff2c_input_2.pkl (paper_meta)
# tables['table_4'] -> aan_1_Author.pkl
# tables['table_5'] -> aan_1_Citation.pkl

aff = tables['table_1']
auth_aff_paper = tables['table_2']
paper_meta = tables['table_3']

def infer_year_from_paper_id(pid: str):
    if not isinstance(pid, str):
        return pd.NA
    m = re.match(r"^[A-Z]+(\d{2})[-_]\d+", pid)
    if not m:
        return pd.NA
    yy = int(m.group(1))
    if 0 <= yy <= 21:
        return 2000 + yy
    elif 70 <= yy <= 99:
        return 1900 + yy
    else:
        return 1900 + yy

auth_aff_paper = auth_aff_paper.copy()
auth_aff_paper["paper_id"] = (
    auth_aff_paper["paper_prefix"].astype(str).str.strip()
    + "-"
    + auth_aff_paper["paper_suffix"].astype(str).str.strip()
)

def to_aff_id_str(x):
    if pd.isna(x):
        return pd.NA
    fx = float(x)
    if float(fx).is_integer():
        return str(int(fx))
    return str(x)

auth_aff_paper["affiliation_id_str"] = auth_aff_paper["affiliation_id"].apply(to_aff_id_str)

aff_join = aff.rename(columns={"affiliation_id": "affiliation_id_str"}).copy()
aff_join["affiliation_id_str"] = aff_join["affiliation_id_str"].astype(str)

aff_stanford = aff_join[aff_join["name"].astype(str).str.contains("Stanford University", case=False, na=False)].copy()

aap_stanford = auth_aff_paper.merge(
    aff_stanford[["affiliation_id_str", "name"]],
    on="affiliation_id_str",
    how="inner"
)

aap_stanford["year"] = aap_stanford["paper_id"].map(infer_year_from_paper_id)

mask_2000s = aap_stanford["year"].between(2000, 2009, inclusive="both")
distinct_papers_2000s = aap_stanford.loc[mask_2000s, "paper_id"].dropna().unique()
count_distinct_papers_2000s = len(distinct_papers_2000s)

answer_df = pd.DataFrame({"count_stanford_papers_2000_2009": [count_distinct_papers_2000s]})
result = {"stanford_papers_2000_2009": answer_df}