import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Parse CustomerID and segment from packed field like "38144-KAM"
parts = t1["CustomerID_Segment"].astype(str).str.rsplit("-", n=1, expand=True)
t1["CustomerID"] = pd.to_numeric(parts[0], errors="coerce").astype("Int64")
t1["ClientSegment"] = parts[1].astype(str)

# Filter to September 2013
t2["Year"] = t2["Year"].astype(str)
t2["Month"] = t2["Month"].astype(str).str.zfill(2)
t2_sep2013 = t2[(t2["Year"] == "2013") & (t2["Month"] == "09")].copy()

# Join to get segments, then aggregate consumption by segment
joined = t2_sep2013.merge(t1[["CustomerID", "ClientSegment"]], on="CustomerID", how="left")
seg_cons = (
    joined.dropna(subset=["ClientSegment"])
    .groupby("ClientSegment", as_index=False)["Consumption"]
    .sum()
    .rename(columns={"Consumption": "TotalConsumption"})
)

# Find segment(s) with minimum total consumption
min_val = seg_cons["TotalConsumption"].min()
out = seg_cons[seg_cons["TotalConsumption"] == min_val].sort_values("ClientSegment").reset_index(drop=True)

result = {"least_consuming_client_segment_sep_2013": out}
