import pandas as pd
import numpy as np
import re

def norm_key(s):
    return (
        s.astype("string")
         .str.strip()
         .str.upper()
         .replace({"": pd.NA, "NAN": pd.NA, "NONE": pd.NA})
    )

def norm_name(s):
    out = s.astype("string").str.upper().str.strip()
    out = out.str.replace("&", "AND", regex=False)
    out = out.str.replace(r"[^A-Z0-9]+", "", regex=True)
    out = out.str.replace("AND", "", regex=False)
    return out.replace({"": pd.NA, "NAN": pd.NA, "NONE": pd.NA})

# --- Organizations ---
orgs = tables["table_2"].copy()

# Fill/standardize DLC key using mapping table when available
orgs["DLC_KEY_N"] = norm_key(orgs["DLC_KEY"])

if "table_9" in tables:
    org_dlc = tables["table_9"].copy()
    org_dlc["DLC_KEY_N_MAP"] = norm_key(org_dlc["DLC_KEY"])
    orgs = orgs.merge(
        org_dlc[["FCLT_ORGANIZATION_KEY", "DLC_KEY_N_MAP"]],
        on="FCLT_ORGANIZATION_KEY",
        how="left"
    )
    orgs["DLC_KEY_N"] = orgs["DLC_KEY_N"].fillna(orgs["DLC_KEY_N_MAP"])
    orgs = orgs.drop(columns=["DLC_KEY_N_MAP"])

# Exclude organizations 139 and 250
orgs = orgs[~orgs["ORGANIZATION_ID"].astype("string").str.strip().isin(["139", "250"])].copy()

# --- Hierarchy type by DLC ---
hier = tables["table_5"].copy()
hier_key_col = "dlc_key" if "dlc_key" in hier.columns else "DLC_KEY"
hier["DLC_KEY_N"] = norm_key(hier[hier_key_col])
hier = hier[["DLC_KEY_N", "HIERARCHY_TYPE"]].dropna(subset=["DLC_KEY_N"]).drop_duplicates()

org_hier = orgs.merge(hier, on="DLC_KEY_N", how="left")
org_hier["HIERARCHY_TYPE"] = org_hier["HIERARCHY_TYPE"].fillna("No Hierarchy")

# --- Build HR/faculty organization title -> DLC key lookup ---
lookup_parts = []

def add_lookup(df, name_cols, dlc_col):
    tmp_parts = []
    if dlc_col not in df.columns:
        return tmp_parts
    d = df.copy()
    d["DLC_KEY_N"] = norm_key(d[dlc_col])
    for c in name_cols:
        if c in d.columns:
            t = d[[c, "DLC_KEY_N"]].copy()
            t["NAME_KEY"] = norm_name(t[c])
            t = t[["NAME_KEY", "DLC_KEY_N"]]
            tmp_parts.append(t)
    return tmp_parts

lookup_parts += add_lookup(
    tables["table_7"],
    ["HR_ORG_UNIT_NAME", "HR_DEPARTMENT_NAME", "HR_DEPARTMENT_NAME_LONG", "DLC_NAME"],
    "DLC_KEY"
)

lookup_parts += add_lookup(
    tables["table_8"],
    ["HR_ORG_UNIT_TITLE", "HR_DEPARTMENT_NAME", "HR_DEPARTMENT_NAME_LONG", "HR_DEPARTMENT_NAME_ALPHA"],
    "DLC_KEY"
)

lookup_parts += add_lookup(
    orgs,
    ["HR_DEPARTMENT_NAME", "DLC_NAME", "ORGANIZATION_NAME", "DESCRIPTION"],
    "DLC_KEY"
)

name_to_dlc = (
    pd.concat(lookup_parts, ignore_index=True)
      .dropna(subset=["NAME_KEY", "DLC_KEY_N"])
      .drop_duplicates()
      .drop_duplicates(subset=["NAME_KEY"], keep="first")
)

# --- Faculty/member counts by organization DLC and emeritus status ---
faculty = tables["table_4"].copy()
faculty["NAME_KEY"] = norm_name(faculty["HR_ORG_UNIT_TITLE"])
faculty["EMERITUS_STATUS_GROUP"] = np.where(
    faculty["EMERITUS_STATUS"].astype("string").str.strip().fillna("").ne(""),
    "Emeritus",
    "Non-Emeritus"
)

faculty_mapped = faculty.merge(name_to_dlc, on="NAME_KEY", how="inner")

member_counts = (
    faculty_mapped
    .groupby(["DLC_KEY_N", "EMERITUS_STATUS_GROUP"], as_index=False)
    .agg(EMPLOYER_COUNT=("MIT_ID", "nunique"))
)

# --- Final detail rows ---
detail = org_hier.merge(member_counts, on="DLC_KEY_N", how="inner")

detail["BREAK_GROUP"] = np.where(
    detail["ORGANIZATION_LEVEL"].gt(4) & detail["FCLT_ORG_PARENT_KEY"].notna(),
    detail["FCLT_ORG_PARENT_KEY"],
    detail["ORGANIZATION_ID"]
)

detail["FORMATTED_ORGANIZATION_NAME"] = detail.apply(
    lambda r: ("  " * max(int(r["ORGANIZATION_LEVEL"]) - 4, 0)) + str(r["ORGANIZATION_NAME"]),
    axis=1
)

detail = detail.rename(columns={"EMERITUS_STATUS_GROUP": "EMERITUS_STATUS"})

final_cols = [
    "BREAK_GROUP",
    "ORGANIZATION_ID",
    "ORGANIZATION_NAME",
    "FORMATTED_ORGANIZATION_NAME",
    "EMERITUS_STATUS",
    "ORGANIZATION_NUMBER",
    "ORGANIZATION_LEVEL",
    "EMPLOYER_COUNT",
    "HIERARCHY_TYPE"
]

detail = detail[final_cols].copy()
detail["_row_order"] = 0

# --- Totals for employer counts ---
hier_totals = (
    detail
    .groupby("HIERARCHY_TYPE", as_index=False)["EMPLOYER_COUNT"]
    .sum()
)
hier_totals["BREAK_GROUP"] = pd.NA
hier_totals["ORGANIZATION_ID"] = pd.NA
hier_totals["ORGANIZATION_NAME"] = "Hierarchy Total"
hier_totals["FORMATTED_ORGANIZATION_NAME"] = "Hierarchy Total"
hier_totals["EMERITUS_STATUS"] = "Total"
hier_totals["ORGANIZATION_NUMBER"] = pd.NA
hier_totals["ORGANIZATION_LEVEL"] = pd.NA
hier_totals["_row_order"] = 1
hier_totals = hier_totals[final_cols + ["_row_order"]]

grand_total = pd.DataFrame([{
    "BREAK_GROUP": pd.NA,
    "ORGANIZATION_ID": pd.NA,
    "ORGANIZATION_NAME": "Grand Total",
    "FORMATTED_ORGANIZATION_NAME": "Grand Total",
    "EMERITUS_STATUS": "Total",
    "ORGANIZATION_NUMBER": pd.NA,
    "ORGANIZATION_LEVEL": pd.NA,
    "EMPLOYER_COUNT": detail["EMPLOYER_COUNT"].sum(),
    "HIERARCHY_TYPE": "Grand Total",
    "_row_order": 2
}])

out = pd.concat([detail, hier_totals, grand_total], ignore_index=True)

out["_hier_sort"] = np.where(out["_row_order"].eq(2), "ZZZZZZ", out["HIERARCHY_TYPE"].astype(str))

out = (
    out.sort_values(
        ["_hier_sort", "_row_order", "BREAK_GROUP", "ORGANIZATION_LEVEL", "ORGANIZATION_NAME", "EMERITUS_STATUS"],
        kind="mergesort"
    )
    .drop(columns=["_row_order", "_hier_sort"])
    .reset_index(drop=True)
)

result = {"organization_emeritus_counts_by_hierarchy": out}
