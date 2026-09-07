import pandas as pd

# --- Staff table (table_2) is transposed: rows are attributes, columns are staff ids ---
t2 = tables["table_2"].copy()
t2_long = t2.melt(id_vars=["staff_ID"], var_name="staff_id", value_name="val")
staff_wide = (
    t2_long.pivot_table(index="staff_id", columns="staff_ID", values="val", aggfunc="first")
    .reset_index()
)
staff_wide["staff_id"] = pd.to_numeric(staff_wide["staff_id"], errors="coerce")

canadian_staff_ids = set(
    staff_wide.loc[
        staff_wide["Nationality"].astype(str).str.strip().str.lower().eq("canada"),
        "staff_id",
    ]
    .dropna()
    .astype(int)
    .tolist()
)

# --- Conference-staff links (table_3): parse "conferenceID-staffID" ---
t3 = tables["table_3"].copy()
pairs = t3["conference_staff"].astype(str).str.split("-", n=1, expand=True)
t3["Conference_ID"] = pd.to_numeric(pairs[0], errors="coerce")
t3["staff_id"] = pd.to_numeric(pairs[1], errors="coerce")

conf_ids_with_canadians = (
    t3.loc[t3["staff_id"].isin(canadian_staff_ids), "Conference_ID"]
    .dropna()
    .astype(int)
    .unique()
)

# --- Conference names from key-value table (table_1): use attr=="Conference_ID" to map id -> conf name ---
t1 = tables["table_1"].copy()
conf_map = t1.loc[t1["attr"].astype(str).str.strip().eq("Conference_ID"), ["conf", "value"]].copy()
conf_map["Conference_ID"] = pd.to_numeric(conf_map["value"], errors="coerce")
conf_map["conference_name"] = conf_map["conf"].astype(str).str.strip()
conf_map = conf_map.dropna(subset=["Conference_ID"])

out = (
    conf_map.loc[conf_map["Conference_ID"].isin(conf_ids_with_canadians), ["conference_name"]]
    .drop_duplicates()
    .sort_values("conference_name")
    .reset_index(drop=True)
)

result = {"conferences_with_canadian_staff": out}
