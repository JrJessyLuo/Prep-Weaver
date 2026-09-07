import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]
t3 = tables["table_3"]
t4 = tables["table_4"]

# Customer ID for "Hardy Kutch"
hardy_ids = t2.loc[t2["kehu_xinxi"].eq("Hardy Kutch"), "kehu_id"].dropna().unique()

# Services used by Hardy Kutch (via customer-service mapping)
svc_used = t3.loc[t3["Customer_ID"].isin(hardy_ids), "Service_ID"].dropna().unique()

# Services rated "good" in customer interactions
svc_good = t4.loc[t4["xiangxi"].astype(str).str.lower().eq("good"), "Service_ID"].dropna().unique()

# Union of services
svc_ids = pd.Index(pd.unique(pd.Series(list(svc_used) + list(svc_good)))).dropna()

services = (
    pd.DataFrame({"Service_ID": svc_ids.astype(int)})
    .merge(t1[["Service_ID", "Service_Type", "Details"]], on="Service_ID", how="left")
    .drop_duplicates(subset=["Service_ID"])
    .sort_values("Service_ID")
    .reset_index(drop=True)
)

result = {"service_details": services}
