import pandas as pd
import numpy as np

def clean_str_col(s):
    return s.astype("string").str.strip()

def fallback_owner_from_key(k):
    if pd.isna(k):
        return pd.NA
    s = str(k).strip()
    u = s.upper()
    for prefix in ("KERBEROS", "STRING", "USER", "LIST"):
        if u.startswith(prefix):
            return s[len(prefix):]
    return s

person_parts = []
for tname in ["table_5", "table_10", "table_2"]:
    df = tables.get(tname)
    if df is None or "MIT_ID" not in df.columns:
        continue

    krb_cols = [c for c in ["KRB_NAME_UPPERCASE", "krb_name", "KRB_NAME"] if c in df.columns]
    if not krb_cols:
        continue

    mit_id_int = pd.to_numeric(df["MIT_ID"], errors="coerce").round().astype("Int64")
    first_norm = clean_str_col(df["FIRST_NAME"]).str.upper() if "FIRST_NAME" in df.columns else pd.Series(pd.NA, index=df.index, dtype="string")
    last_norm = clean_str_col(df["LAST_NAME"]).str.upper() if "LAST_NAME" in df.columns else pd.Series(pd.NA, index=df.index, dtype="string")

    for kc in krb_cols:
        tmp = pd.DataFrame({
            "MIT_ID_INT": mit_id_int,
            "FIRST_NAME_NORM": first_norm,
            "LAST_NAME_NORM": last_norm,
            "KRB_NORM": clean_str_col(df[kc]).str.upper()
        })
        person_parts.append(tmp)

if person_parts:
    people = pd.concat(person_parts, ignore_index=True)
    people = people[people["KRB_NORM"].notna() & (people["KRB_NORM"] != "")]
else:
    people = pd.DataFrame(columns=["MIT_ID_INT", "FIRST_NAME_NORM", "LAST_NAME_NORM", "KRB_NORM"])

krb_lookup = people[people["MIT_ID_INT"].notna()].drop_duplicates("KRB_NORM")
krb_to_mit = krb_lookup.set_index("KRB_NORM")["MIT_ID_INT"].astype("int64") if not krb_lookup.empty else pd.Series(dtype="int64")

faculty = tables["table_3"].copy()
faculty_first = clean_str_col(faculty["FIRST_NAME"]).str.upper()
faculty_last = clean_str_col(faculty["LAST_NAME"]).str.upper()
faculty_title = clean_str_col(faculty["JOB_TITLE"]).str.upper() if "JOB_TITLE" in faculty.columns else pd.Series("", index=faculty.index, dtype="string")
faculty_mit = pd.to_numeric(faculty["MIT_ID"], errors="coerce").round().astype("Int64")

ayden_mask = faculty_first.eq("AYDEN") & faculty_last.eq("HOPKINS")
if "JOB_TITLE" in faculty.columns:
    ayden_mask = ayden_mask & faculty_title.str.contains("PROFESSOR", na=False)

ayden_ids = set(faculty_mit[ayden_mask & faculty_mit.notna()].astype("int64").tolist())

ayden_people_mask = (
    (people["MIT_ID_INT"].isin(ayden_ids) if ayden_ids else pd.Series(False, index=people.index))
    | (people["FIRST_NAME_NORM"].eq("AYDEN") & people["LAST_NAME_NORM"].eq("HOPKINS"))
)
ayden_krbs = set(people.loc[ayden_people_mask, "KRB_NORM"].dropna().astype(str).tolist())

members = tables["table_1"].copy()
members["LIST_KEY_NORM"] = clean_str_col(members["MOIRA_LIST_KEY"]).str.upper()
members["MEMBER_KRB_NORM"] = clean_str_col(members["moira_list_member"]).str.upper()
members["MEMBER_MIT_ID_INT"] = pd.to_numeric(members["MOIRA_LIST_MEMBER_MIT_ID"], errors="coerce").round().astype("Int64")
mapped_mit = pd.to_numeric(members["MEMBER_KRB_NORM"].map(krb_to_mit), errors="coerce").astype("Int64")
members["PERSON_MIT_ID_INT"] = members["MEMBER_MIT_ID_INT"].combine_first(mapped_mit)

ayden_member_mask = pd.Series(False, index=members.index)
if ayden_ids:
    ayden_member_mask = ayden_member_mask | members["PERSON_MIT_ID_INT"].isin(ayden_ids)
if ayden_krbs:
    ayden_member_mask = ayden_member_mask | members["MEMBER_KRB_NORM"].isin(ayden_krbs)
if "MOIRA_LIST_MEMBER_FULL_NAME" in members.columns:
    member_full_name = clean_str_col(members["MOIRA_LIST_MEMBER_FULL_NAME"]).str.upper()
    ayden_member_mask = ayden_member_mask | member_full_name.eq("HOPKINS, AYDEN") | member_full_name.str.startswith("HOPKINS, AYDEN ", na=False)

subscribed_keys = set(members.loc[ayden_member_mask, "LIST_KEY_NORM"].dropna().astype(str).tolist())

tenured_mask = (
    faculty_title.str.contains("PROFESSOR", na=False)
    & ~faculty_title.str.contains("ASSISTANT", na=False)
    & ~faculty_title.str.contains(r"WITHOUT TENURE|NON[- ]?TENURE", regex=True, na=False)
)
tenured_ids = set(faculty_mit[tenured_mask & faculty_mit.notna()].astype("int64").tolist())

people_counts = (
    members[members["PERSON_MIT_ID_INT"].notna()]
    .drop_duplicates(["LIST_KEY_NORM", "PERSON_MIT_ID_INT"])
    .groupby("LIST_KEY_NORM", as_index=False)
    .size()
    .rename(columns={"size": "number_of_people_in_list"})
)

tenured_counts = (
    members[members["PERSON_MIT_ID_INT"].isin(tenured_ids)]
    .drop_duplicates(["LIST_KEY_NORM", "PERSON_MIT_ID_INT"])
    .groupby("LIST_KEY_NORM", as_index=False)
    .size()
    .rename(columns={"size": "number_of_tenured_faculty_in_list"})
)

members["OWNER_KEY_RAW"] = clean_str_col(members["MOIRA_LIST_OWNER_KEY"])
members["OWNER_KEY_NORM"] = members["OWNER_KEY_RAW"].str.upper()

owner_per_list = (
    members[members["OWNER_KEY_NORM"].notna() & (members["OWNER_KEY_NORM"] != "")]
    [["LIST_KEY_NORM", "OWNER_KEY_RAW", "OWNER_KEY_NORM"]]
    .drop_duplicates("LIST_KEY_NORM")
)

owners = tables["table_9"].copy()
owners["OWNER_KEY_NORM"] = clean_str_col(owners["MOIRA_LIST_OWNER_KEY"]).str.upper()
owner_lookup = owners[["OWNER_KEY_NORM", "OWNER"]].drop_duplicates("OWNER_KEY_NORM")

owner_per_list = owner_per_list.merge(owner_lookup, on="OWNER_KEY_NORM", how="left")
owner_per_list["owner"] = owner_per_list["OWNER"].where(
    owner_per_list["OWNER"].notna(),
    owner_per_list["OWNER_KEY_RAW"].apply(fallback_owner_from_key)
)
owner_per_list = owner_per_list[["LIST_KEY_NORM", "owner"]]

lists = tables["table_4"].copy()
lists["LIST_KEY_NORM"] = clean_str_col(lists["MOIRA_LIST_KEY"]).str.upper()
lists["name"] = clean_str_col(lists["MOIRA_LIST_NAME"]) if "MOIRA_LIST_NAME" in lists.columns else clean_str_col(lists["MOIRA_LIST_KEY"])
lists["description"] = lists["MOIRA_LIST_DESCRIPTION"] if "MOIRA_LIST_DESCRIPTION" in lists.columns else pd.Series(pd.NA, index=lists.index)

starts_r = lists["name"].str.upper().str.startswith("R", na=False)
mailing_mask = clean_str_col(lists["IS_MOIRA_MAILING_LIST"]).str.upper().eq("Y") if "IS_MOIRA_MAILING_LIST" in lists.columns else pd.Series(True, index=lists.index)

meta = (
    lists[starts_r & mailing_mask & lists["LIST_KEY_NORM"].isin(subscribed_keys)]
    [["LIST_KEY_NORM", "name", "description"]]
    .drop_duplicates("LIST_KEY_NORM")
)

out = (
    meta.merge(owner_per_list, on="LIST_KEY_NORM", how="left")
    .merge(people_counts, on="LIST_KEY_NORM", how="left")
    .merge(tenured_counts, on="LIST_KEY_NORM", how="left")
)

out["number_of_people_in_list"] = out["number_of_people_in_list"].fillna(0).astype(int)
out["number_of_tenured_faculty_in_list"] = out["number_of_tenured_faculty_in_list"].fillna(0).astype(int)

out = out[[
    "name",
    "description",
    "owner",
    "number_of_people_in_list",
    "number_of_tenured_faculty_in_list"
]].sort_values("name", kind="mergesort").reset_index(drop=True)

result = {"mailing_lists": out}
