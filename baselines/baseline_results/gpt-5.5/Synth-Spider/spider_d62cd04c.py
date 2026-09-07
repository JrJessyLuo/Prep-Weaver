import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Find possible IDs for "John Zoidfarb" (typo-tolerant: match on 'john' + 'zoid')
sender_ids = set()

mask_t1 = (
    t1["xingming"].astype(str).str.contains("john", case=False, na=False)
    & t1["xingming"].astype(str).str.contains("zoid", case=False, na=False)
)
sender_ids.update(t1.loc[mask_t1, "zhanghao"].dropna().astype(int).tolist())

mask_t3 = (
    t3["Name"].astype(str).str.contains("john", case=False, na=False)
    & t3["Name"].astype(str).str.contains("zoid", case=False, na=False)
)
sender_ids.update(t3.loc[mask_t3, "EmployeeID"].dropna().astype(int).tolist())

# Filter packages sent by those IDs
out = t2[t2["FaSongRen"].isin(list(sender_ids))].copy()

# Select relevant columns for "package contents"
out = out.loc[:, ["Shipment", "BaoZhuangHao", "Contents"]].drop_duplicates().reset_index(drop=True)

result = {"package_contents_sent_by_john_zoidfarb": out}
