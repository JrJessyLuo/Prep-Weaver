import pandas as pd
import numpy as np
import re

def _dlc_col(df):
    for c in df.columns:
        if c.lower() == "dlc_key":
            return c
    return None

def _norm_key(s):
    return s.astype("string").str.strip().str.upper()

# Build DLC key/name universe
dlc_parts = []
name_source_priority = {
    "table_2": 1,
    "table_5": 2,
    "table_4": 3,
    "table_3": 4,
    "table_7": 5,
    "table_10": 6,
    "table_9": 7,
    "table_1": 8,
    "table_8": 9,
}

for tname, df in tables.items():
    dc = _dlc_col(df)
    if dc is None:
        continue

    tmp = pd.DataFrame({"DLC_KEY": _norm_key(df[dc])})
    if "DLC_NAME" in df.columns:
        tmp["DLC_NAME"] = df["DLC_NAME"]
    else:
        tmp["DLC_NAME"] = pd.NA

    tmp["_priority"] = name_source_priority.get(tname, 99)
    tmp = tmp[tmp["DLC_KEY"].notna() & (tmp["DLC_KEY"] != "")]
    dlc_parts.append(tmp)

dlc_all = pd.concat(dlc_parts, ignore_index=True) if dlc_parts else pd.DataFrame(columns=["DLC_KEY", "DLC_NAME", "_priority"])
dlc_names = (
    dlc_all.sort_values(["DLC_KEY", "_priority"])
    .drop_duplicates(["DLC_KEY", "DLC_NAME"])
    .sort_values(["DLC_KEY", "_priority"])
)
dlc_names = (
    dlc_names[dlc_names["DLC_NAME"].notna()]
    .drop_duplicates("DLC_KEY", keep="first")[["DLC_KEY", "DLC_NAME"]]
)

base = pd.DataFrame({"DLC_KEY": sorted(dlc_all["DLC_KEY"].dropna().unique())})
base = base.merge(dlc_names, on="DLC_KEY", how="left")

# Total number of facility organizations
facility_pairs = []
for df in tables.values():
    dc = _dlc_col(df)
    if dc is None:
        continue

    org_cols = [c for c in df.columns if c.lower() == "fclt_organization_key"]
    if not org_cols:
        continue

    oc = org_cols[0]
    tmp = pd.DataFrame({
        "DLC_KEY": _norm_key(df[dc]),
        "FCLT_ORGANIZATION_KEY": df[oc]
    })
    tmp = tmp[tmp["DLC_KEY"].notna() & tmp["FCLT_ORGANIZATION_KEY"].notna()]
    facility_pairs.append(tmp)

if facility_pairs:
    facility_counts = (
        pd.concat(facility_pairs, ignore_index=True)
        .drop_duplicates()
        .groupby("DLC_KEY", as_index=False)["FCLT_ORGANIZATION_KEY"]
        .nunique()
        .rename(columns={"FCLT_ORGANIZATION_KEY": "total_number_of_facility_organizations"})
    )
else:
    facility_counts = pd.DataFrame(columns=["DLC_KEY", "total_number_of_facility_organizations"])

# Total number of supervisors
supervisor_parts = []
for df in tables.values():
    dc = _dlc_col(df)
    if dc is None:
        continue

    sup_cols = [
        c for c in df.columns
        if re.search(r"(supervisor|username|user_name)", c, flags=re.I)
    ]
    for sc in sup_cols:
        tmp = pd.DataFrame({"DLC_KEY": _norm_key(df[dc]), "supervisor": df[sc]})
        tmp = tmp[tmp["DLC_KEY"].notna() & tmp["supervisor"].notna()]
        supervisor_parts.append(tmp)

if supervisor_parts:
    supervisor_counts = (
        pd.concat(supervisor_parts, ignore_index=True)
        .drop_duplicates()
        .groupby("DLC_KEY", as_index=False)["supervisor"]
        .nunique()
        .rename(columns={"supervisor": "total_number_of_supervisors"})
    )
else:
    supervisor_counts = pd.DataFrame(columns=["DLC_KEY", "total_number_of_supervisors"])

# Total number of supervisees
supervisee_parts = []
for df in tables.values():
    dc = _dlc_col(df)
    if dc is None:
        continue

    sv_cols = [c for c in df.columns if re.search(r"supervisee", c, flags=re.I)]
    for sc in sv_cols:
        tmp = pd.DataFrame({"DLC_KEY": _norm_key(df[dc]), "supervisee": df[sc]})
        tmp = tmp[tmp["DLC_KEY"].notna() & tmp["supervisee"].notna()]
        supervisee_parts.append(tmp)

if supervisee_parts:
    supervisee_counts = (
        pd.concat(supervisee_parts, ignore_index=True)
        .drop_duplicates()
        .groupby("DLC_KEY", as_index=False)["supervisee"]
        .nunique()
        .rename(columns={"supervisee": "total_number_of_supervisees"})
    )
else:
    supervisee_counts = pd.DataFrame(columns=["DLC_KEY", "total_number_of_supervisees"])

def _sum_metric(patterns, output_col):
    parts = []
    for df in tables.values():
        dc = _dlc_col(df)
        if dc is None:
            continue

        metric_cols = []
        for c in df.columns:
            cl = c.lower()
            if c == dc:
                continue
            if any(re.search(p, cl) for p in patterns):
                metric_cols.append(c)

        for mc in metric_cols:
            vals = pd.to_numeric(df[mc], errors="coerce")
            tmp = pd.DataFrame({"DLC_KEY": _norm_key(df[dc]), output_col: vals})
            tmp = tmp[tmp["DLC_KEY"].notna() & tmp[output_col].notna()]
            parts.append(tmp)

    if not parts:
        return pd.DataFrame(columns=["DLC_KEY", output_col])

    return (
        pd.concat(parts, ignore_index=True)
        .groupby("DLC_KEY", as_index=False)[output_col]
        .sum()
    )

floor_totals = _sum_metric(
    [r"\bfloors?\b", r"number_of_floors", r"floor_count", r"total_floors"],
    "total_number_of_floors"
)

sqft_totals = _sum_metric(
    [r"square.*foot", r"sq.*ft", r"sqft", r"square_footage", r"gross_area", r"net_area"],
    "total_square_footage"
)

height_totals = _sum_metric(
    [r"height"],
    "total_building_heights"
)

out = base.copy()
for agg in [
    floor_totals,
    sqft_totals,
    facility_counts,
    supervisor_counts,
    supervisee_counts,
    height_totals,
]:
    out = out.merge(agg, on="DLC_KEY", how="left")

for col in [
    "total_number_of_floors",
    "total_square_footage",
    "total_number_of_facility_organizations",
    "total_number_of_supervisors",
    "total_number_of_supervisees",
    "total_building_heights",
]:
    out[col] = out[col].fillna(0)

out = out[
    [
        "DLC_KEY",
        "DLC_NAME",
        "total_number_of_floors",
        "total_square_footage",
        "total_number_of_facility_organizations",
        "total_number_of_supervisors",
        "total_number_of_supervisees",
        "total_building_heights",
    ]
].sort_values("DLC_KEY").reset_index(drop=True)

result = {"dlc_summary": out}
