import pandas as pd

# Tables are already loaded in scope as `tables`
events = tables["table_1"]
links = tables["table_2"]
members = tables["table_3"]

laugh_out_loud_event_ids = (
    events.loc[events["event_name"].eq("Laugh Out Loud"), "event_id"]
    .dropna()
    .drop_duplicates()
    .reset_index(drop=True)
)

attendees_full_names = (
    links.assign(
        event_id=links["combined_link"].astype(str).str.split("|").str[0],
        member_id=links["combined_link"].astype(str).str.split("|").str[1],
    )
    .loc[lambda d: d["event_id"].isin(laugh_out_loud_event_ids)]
    .merge(members[["member_id", "first_name", "last_name"]], on="member_id", how="inner")
    .assign(
        full_name=lambda d: d["first_name"].fillna("").str.strip()
        + " "
        + d["last_name"].fillna("").str.strip()
    )
    .loc[lambda d: d["full_name"].str.strip().ne("")]
    .drop_duplicates(subset=["full_name"])[["full_name"]]
    .reset_index(drop=True)
)

result = {"laugh_out_loud_attendees": attendees_full_names}