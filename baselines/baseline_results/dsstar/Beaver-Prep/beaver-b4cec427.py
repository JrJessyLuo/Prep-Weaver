import pandas as pd

# Tables provided in scope:
# tables['table_1'] -> MOIRA_LIST_DETAIL.pkl
# tables['table_2'] -> OPA_PERSON_CURRENT.pkl
# tables['table_3'] -> HR_FACULTY_ROSTER.pkl
# tables['table_4'] -> MOIRA_LIST.pkl
# tables['table_5'] -> EMPLOYEE_DIRECTORY.pkl
# tables['table_6'] -> FCLT_ORGANIZATION_HIST.pkl
# tables['table_7'] -> DRUPAL_EMPLOYEE_DIRECTORY.pkl
# tables['table_8'] -> FCLT_ORGANIZATION.pkl
# tables['table_9'] -> MOIRA_LIST_OWNER.pkl
# tables['table_10'] -> WAREHOUSE_USERS.pkl

# Load DataFrames from provided tables dict
moira_list_detail = tables['table_1'].copy()
moira_list = tables['table_4'].copy()
moira_list_owner = tables['table_9'].copy()
hr_faculty_roster = tables['table_3'].copy()

# Filter MOIRA_LIST to names starting with "R" (case-insensitive)
moira_list_filtered = (
    moira_list.loc[
        moira_list["MOIRA_LIST_NAME"].astype(str).str.startswith("R", na=False, case=False),
        ["MOIRA_LIST_KEY", "MOIRA_LIST_NAME", "MOIRA_LIST_DESCRIPTION"]
    ]
    .copy()
)

# Join the filtered MOIRA_LIST with MOIRA_LIST_DETAIL on MOIRA_LIST_KEY
joined = moira_list_detail.merge(
    moira_list_filtered,
    on="MOIRA_LIST_KEY",
    how="inner"
)

# Normalize the names for robust matching:
def normalize_name(s: pd.Series) -> pd.Series:
    return (
        s.astype(str)
         .str.replace(r"\s+", " ", regex=True)
         .str.strip()
         .str.upper()
    )

joined["NAME_NORM"] = normalize_name(joined["MOIRA_LIST_MEMBER_FULL_NAME"])

# Build target name variants to allow "similar match"
targets = [
    "HOPKINS, AYDEN",
    "AYDEN HOPKINS",
    "HOPKINS AYDEN",
]
targets_norm = set(normalize_name(pd.Series(targets)).tolist())

# Basic exact match on normalized forms
mask_exact = joined["NAME_NORM"].isin(targets_norm)

# Additional heuristic: allow comma vs no-comma differences and extra spaces
joined["NAME_NOCOMMA"] = joined["NAME_NORM"].str.replace(",", "", regex=False)
mask_nocomma = joined["NAME_NOCOMMA"].isin(targets_norm)

# Combine masks
mask = mask_exact | mask_nocomma

# Lists Professor Ayden Hopkins is subscribed to
ayden_lists = (
    joined.loc[mask, ["MOIRA_LIST_KEY", "MOIRA_LIST_NAME", "MOIRA_LIST_DESCRIPTION"]]
    .drop_duplicates(subset=["MOIRA_LIST_KEY"])
    .copy()
)

# If no lists found, prepare empty result with required columns
if ayden_lists.empty:
    final_df = pd.DataFrame(columns=[
        "MOIRA_LIST_NAME",
        "MOIRA_LIST_DESCRIPTION",
        "OWNER_NAME",
        "NUM_PEOPLE_IN_LIST",
        "NUM_TENURED_FACULTY_IN_LIST"
    ])
else:
    # Owners: join owners for each list, aggregate owner names
    owners = moira_list_owner.merge(
        moira_list_filtered[["MOIRA_LIST_KEY"]],
        on="MOIRA_LIST_KEY",
        how="inner"
    ).copy()

    # Owner display name: prefer OWNER_FULL_NAME if present else constructed from parts if available
    owner_name_cols = [c for c in owners.columns if isinstance(c, str)]
    if "OWNER_FULL_NAME" in owner_name_cols:
        owners["OWNER_NAME"] = owners["OWNER_FULL_NAME"].astype(str)
    else:
        # Fallback assemble from any plausible name parts if they exist
        first = owners[owner_name_cols].filter(regex="FIRST", axis=1)
        last = owners[owner_name_cols].filter(regex="LAST", axis=1)
        if not first.empty and not last.empty:
            owners["OWNER_NAME"] = first.iloc[:,0].astype(str).str.strip() + " " + last.iloc[:,0].astype(str).str.strip()
        else:
            # last resort: use OWNER_KERB or similar
            if "OWNER_KERB" in owner_name_cols:
                owners["OWNER_NAME"] = owners["OWNER_KERB"].astype(str)
            else:
                owners["OWNER_NAME"] = ""

    owners_agg = (
        owners.groupby("MOIRA_LIST_KEY", as_index=False)["OWNER_NAME"]
        .apply(lambda s: ", ".join(sorted({x.strip() for x in s.astype(str) if x.strip()})))
        .rename(columns={"OWNER_NAME": "OWNER_NAME"})
    )

    # Count people in each list from detail table restricted to R-lists
    members_in_r = moira_list_detail.merge(
        moira_list_filtered[["MOIRA_LIST_KEY"]],
        on="MOIRA_LIST_KEY",
        how="inner"
    )
    count_people = (
        members_in_r.groupby("MOIRA_LIST_KEY", as_index=False)["MOIRA_LIST_MEMBER_FULL_NAME"]
        .nunique()
        .rename(columns={"MOIRA_LIST_MEMBER_FULL_NAME": "NUM_PEOPLE_IN_LIST"})
    )

    # Tenured faculty identification:
    # Heuristic: use HR_FACULTY_ROSTER tenure columns if available
    hrf = hr_faculty_roster.copy()
    cols = list(hrf.columns)
    # Try common indicators
    tenure_flag_col = None
    for cand in ["TENURE_STATUS", "TENURE_FLAG", "IS_TENURED", "TENURED_FLAG"]:
        if cand in cols:
            tenure_flag_col = cand
            break

    # Normalize MIT IDs in members and roster for join
    def norm_id(s):
        return (
            s.astype(str)
             .str.replace(r"\D", "", regex=True)
             .str.zfill(9)
        )

    members_in_r["MIT_ID_NORM"] = norm_id(members_in_r.get("MOIRA_LIST_MEMBER_MIT_ID", pd.Series(index=members_in_r.index)))
    if "MIT_ID" in cols:
        hrf["MIT_ID_NORM"] = norm_id(hrf["MIT_ID"])
    elif "EMPLOYEE_ID" in cols:
        hrf["MIT_ID_NORM"] = norm_id(hrf["EMPLOYEE_ID"])
    else:
        hrf["MIT_ID_NORM"] = ""

    if tenure_flag_col is not None:
        # Interpret tenured as:
        # - If numeric/bool: True/1
        # - If string: contains "TENURE" and not "NON", or equals "TENURED"
        tf = hrf[["MIT_ID_NORM", tenure_flag_col]].copy()
        if pd.api.types.is_bool_dtype(tf[tenure_flag_col]) or pd.api.types.is_numeric_dtype(tf[tenure_flag_col]):
            tf["IS_TENURED"] = tf[tenure_flag_col].astype(float).fillna(0) == 1.0
        else:
            s = tf[tenure_flag_col].astype(str).str.upper()
            tf["IS_TENURED"] = s.str.contains("TENUR") & ~s.str.contains("NON")
        tenured_ids = set(tf.loc[tf["IS_TENURED"], "MIT_ID_NORM"])
    else:
        # If no tenure flag available, default to empty set
        tenured_ids = set()

    members_in_r["IS_TENURED"] = members_in_r["MIT_ID_NORM"].isin(tenured_ids)

    tenured_count = (
        members_in_r.loc[members_in_r["IS_TENURED"]]
        .groupby("MOIRA_LIST_KEY", as_index=False)["MIT_ID_NORM"]
        .nunique()
        .rename(columns={"MIT_ID_NORM": "NUM_TENURED_FACULTY_IN_LIST"})
    )

    # Merge all components
    final_df = (
        ayden_lists.merge(owners_agg, on="MOIRA_LIST_KEY", how="left")
        .merge(count_people, on="MOIRA_LIST_KEY", how="left")
        .merge(tenured_count, on="MOIRA_LIST_KEY", how="left")
        .fillna({"OWNER_NAME": "", "NUM_PEOPLE_IN_LIST": 0, "NUM_TENURED_FACULTY_IN_LIST": 0})
        .loc[:, ["MOIRA_LIST_NAME", "MOIRA_LIST_DESCRIPTION", "OWNER_NAME", "NUM_PEOPLE_IN_LIST", "NUM_TENURED_FACULTY_IN_LIST"]]
        .sort_values(["MOIRA_LIST_NAME"])
        .reset_index(drop=True)
    )

# Assign final result mapping
result = {
    "r_lists_ayden_hopkins": final_df
}