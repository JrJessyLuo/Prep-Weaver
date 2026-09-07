import pandas as pd

target_list = "beacon-date-date"

def norm_lower(s):
    return s.astype("string").str.strip().str.lower()

def norm_upper(s):
    return s.astype("string").str.strip().str.upper()

# --- Mailing-list metadata and members ---
members = tables["table_3"].copy()
members["_list_key_norm"] = norm_lower(members["MOIRA_LIST_KEY"])
members["_member_krb_upper"] = norm_upper(members["moira_list_member"])
members["_member_full_name_upper"] = norm_upper(members["MOIRA_LIST_MEMBER_FULL_NAME"])
members["_member_mit_id"] = pd.to_numeric(members["MOIRA_LIST_MEMBER_MIT_ID"], errors="coerce")

list_meta = tables["table_4"].copy()
list_meta["_list_key_norm"] = norm_lower(list_meta["MOIRA_LIST_KEY"])
list_meta["_list_name_norm"] = norm_lower(list_meta["MOIRA_LIST_NAME"])

target_meta = list_meta[
    (list_meta["_list_key_norm"].eq(target_list) | list_meta["_list_name_norm"].eq(target_list))
    & (list_meta["IS_MOIRA_MAILING_LIST"].astype("string").str.strip().str.upper().eq("Y"))
]

if target_meta.empty:
    target_members = members[members["_list_key_norm"].eq(target_list)].copy()
else:
    valid_list_ids = set(target_meta["_list_key_norm"].dropna()) | set(target_meta["_list_name_norm"].dropna())
    target_members = members[members["_list_key_norm"].isin(valid_list_ids)].copy()

mailing_list_size = int(target_members["COUNTER"].sum()) if "COUNTER" in target_members.columns else int(len(target_members))

target_krbs = set(target_members["_member_krb_upper"].dropna())
target_names = set(target_members["_member_full_name_upper"].dropna())
target_mit_ids = set(target_members["_member_mit_id"].dropna().astype("int64"))

# --- Build optional person lookup to improve KRB/MIT_ID matching ---
lookup_parts = []

if "table_2" in tables:
    d = tables["table_2"].copy()
    d["_email_upper"] = norm_upper(d["EMAIL_ADDRESS"])
    d["_krb_upper_lookup"] = norm_upper(d["KRB_NAME_UPPERCASE"])
    d["_mit_id_lookup"] = pd.to_numeric(d["MIT_ID"], errors="coerce")
    d["_office_phone_lookup"] = pd.to_numeric(d["OFFICE_PHONE"], errors="coerce")
    lookup_parts.append(d[["_email_upper", "_krb_upper_lookup", "_mit_id_lookup", "_office_phone_lookup"]])

if "table_10" in tables:
    d = tables["table_10"].copy()
    d["_email_upper"] = norm_upper(d["EMAIL_ADDRESS"])
    d["_krb_upper_lookup"] = norm_upper(d["KRB_NAME_UPPERCASE"])
    d["_mit_id_lookup"] = pd.to_numeric(d["MIT_ID"], errors="coerce")
    d["_office_phone_lookup"] = pd.to_numeric(d["OFFICE_PHONE"], errors="coerce")
    lookup_parts.append(d[["_email_upper", "_krb_upper_lookup", "_mit_id_lookup", "_office_phone_lookup"]])

if lookup_parts:
    person_lookup = pd.concat(lookup_parts, ignore_index=True)
    person_lookup = (
        person_lookup.dropna(subset=["_email_upper"])
        .groupby("_email_upper", as_index=False)
        .agg({
            "_krb_upper_lookup": "first",
            "_mit_id_lookup": "first",
            "_office_phone_lookup": "first",
        })
    )
else:
    person_lookup = pd.DataFrame(columns=["_email_upper", "_krb_upper_lookup", "_mit_id_lookup", "_office_phone_lookup"])

# --- Students whose last names start with H ---
students = tables["table_1"].copy()
students["_email_upper"] = norm_upper(students["EMAIL_ADDRESS"])
students["_email_local_krb_upper"] = students["_email_upper"].str.split("@").str[0].str.strip().str.upper()
students["_full_name_upper"] = students["FULL_NAME_UPPERCASE"].astype("string").fillna(norm_upper(students["FULL_NAME"]))
students["_last_name_upper"] = norm_upper(students["LAST_NAME"])

students_h = students[students["_last_name_upper"].str.startswith("H", na=False)].copy()
students_h = students_h.merge(person_lookup, on="_email_upper", how="left")

students_h["_student_krb_upper"] = students_h["_krb_upper_lookup"].fillna(students_h["_email_local_krb_upper"])
students_h["_student_mit_id"] = pd.to_numeric(students_h["_mit_id_lookup"], errors="coerce")

subscribed = students_h[
    students_h["_student_krb_upper"].isin(target_krbs)
    | students_h["_full_name_upper"].isin(target_names)
    | students_h["_student_mit_id"].dropna().astype("int64").reindex(students_h.index).isin(target_mit_ids).fillna(False)
].copy()

subscribed["_department_phone_number"] = pd.to_numeric(subscribed["OFFICE_PHONE"], errors="coerce").combine_first(
    pd.to_numeric(subscribed["_office_phone_lookup"], errors="coerce")
)
subscribed["_department_phone_number"] = subscribed["_department_phone_number"].astype("Int64")
subscribed["mailing_list_size"] = mailing_list_size

answer = (
    subscribed
    .sort_values(["LAST_NAME", "FIRST_NAME", "FULL_NAME"], na_position="last")
    .drop_duplicates(subset=["FULL_NAME", "EMAIL_ADDRESS", "DEPARTMENT_NAME"])
    .rename(columns={
        "FULL_NAME": "student_name",
        "DEPARTMENT_NAME": "department_name",
        "_department_phone_number": "department_phone_number",
    })
    [["student_name", "department_name", "department_phone_number", "mailing_list_size"]]
    .reset_index(drop=True)
)

result = {"students_beacon_date_date": answer}
