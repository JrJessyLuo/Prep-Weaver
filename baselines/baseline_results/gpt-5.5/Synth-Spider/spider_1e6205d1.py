import pandas as pd

# Load tables
t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# table_1 is transposed: rows are attributes, columns "1".."13" are university ids
u = (
    t1.set_index("University_ID")
      .T
      .reset_index()
      .rename(columns={"index": "uni_id"})
)
u["uni_id"] = pd.to_numeric(u["uni_id"], errors="coerce").astype("Int64")

# Top 3 universities by reputation points
top3 = (
    t2.sort_values(["Reputation_point", "uni_id"], ascending=[False, True])
      .head(3)
      .merge(u[["uni_id", "University_Name"]], on="uni_id", how="left")
      .loc[:, ["University_Name", "cit_p"]]
      .rename(columns={"cit_p": "citation_point"})
      .reset_index(drop=True)
)

result = {"top_3_reputation_universities": top3}
