import pandas as pd

mail = tables["table_1"].copy()
people = tables["table_10"].copy()

mail["member_krb"] = mail["moira_list_member"].astype(str).str.strip().str.upper()
people["krb_upper"] = people["KRB_NAME_UPPERCASE"].astype(str).str.strip().str.upper()
people["office_location_clean"] = people["OFFICE_LOCATION"].astype("string").str.strip()

bldg24_people = people[
    people["office_location_clean"].str.match(r"^24($|[-\s])", na=False)
][["MIT_ID", "krb_upper"]].drop_duplicates()

bldg24_memberships = mail.merge(
    bldg24_people,
    left_on="member_krb",
    right_on="krb_upper",
    how="inner"
)

counts = (
    bldg24_memberships
    .drop_duplicates(["MOIRA_LIST_KEY", "member_krb"])
    .groupby("MOIRA_LIST_KEY", as_index=False)
    .agg(total_number_of_subscribers=("member_krb", "nunique"))
    .rename(columns={"MOIRA_LIST_KEY": "mailing_list_name"})
    .sort_values(["total_number_of_subscribers", "mailing_list_name"], ascending=[False, True])
    .head(1)
    .reset_index(drop=True)
)

result = {"most_subscribed_mailing_list": counts}
