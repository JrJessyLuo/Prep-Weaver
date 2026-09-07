import pandas as pd

conf = tables["table_1"].copy()
inst = tables["table_2"].copy()
staff = tables["table_3"].copy()
part = tables["table_4"].copy()

# Conferences in 2004 (extract year from Conference_Info like "ACL-2004")
conf["year"] = pd.to_numeric(conf["Conference_Info"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
conf_2004_ids = conf.loc[conf["year"].eq(2004), "Conference_ID"].dropna().astype(int).unique()

# Staff who participated in any 2004 conference
staff_2004_ids = part.loc[part["huiyi_id"].isin(conf_2004_ids), "yuangong_id"].dropna().astype(int).unique()

# Map staff -> institution (table_3 uses one of the country columns to store Institution_ID)
country_cols = [c for c in staff.columns if c not in ["staff_ID", "name", "Age"]]
staff_inst = (
    staff.melt(id_vars=["staff_ID"], value_vars=country_cols, value_name="Institution_ID")
    .dropna(subset=["Institution_ID"])
)
staff_inst["Institution_ID"] = staff_inst["Institution_ID"].astype(int)

inst_with_2004_participants = staff_inst.loc[
    staff_inst["staff_ID"].isin(staff_2004_ids), "Institution_ID"
].unique()

# Universities with no staff participating in any 2004 conference
out = inst.loc[~inst["Institution_ID"].isin(inst_with_2004_participants), ["Institution_Name", "Location"]].drop_duplicates()
out = out.rename(columns={"Institution_Name": "university_name", "Location": "location"}).reset_index(drop=True)

result = {"universities_without_2004_conference_participants": out}
