import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Earliest dues payment
t1["date_received"] = pd.to_datetime(t1["date_received"], errors="coerce")
dues = t1[t1["source"].eq("Dues")].dropna(subset=["date_received"])
first_dues = dues.sort_values(["date_received", "income_id"], ascending=[True, True]).head(1)

# Reshape members table (attributes in rows -> columns)
members = (
    t2.set_index("member_id")
      .T
      .reset_index()
      .rename(columns={"index": "member_record_id"})
)

# Join to get full name
out = first_dues.merge(
    members[["member_record_id", "first_name", "last_name"]],
    left_on="link_to_member",
    right_on="member_record_id",
    how="left"
)

out["full_name"] = out["first_name"].astype(str) + " " + out["last_name"].astype(str)

result = {
    "first_paid_dues": out[["full_name"]].head(1).reset_index(drop=True)
}
