import pandas as pd

# ------------------------------------------------------------------------------
# Inputs are provided in a dict named `tables`
# tables['table_3'] corresponds to SUBJECT_OFFERED.pkl
# There is no explicit mailing list table among provided tables.
# We will follow the exact logic of the reference code but source data from `tables`.
# ------------------------------------------------------------------------------

# Step 1: Load SUBJECT_OFFERED and get 2023FA responsible faculty MIT IDs
df = tables['table_3'].copy()

# Filter for Fall 2023
df_2023fa = df[df["TERM_CODE"] == "2023FA"]

# Select required columns and drop duplicates
fac_2023fa = (
    df_2023fa[["RESPONSIBLE_FACULTY_NAME", "responsible_faculty_mit_id"]]
    .dropna(how="all")
    .drop_duplicates()
    .sort_values(by=["RESPONSIBLE_FACULTY_NAME", "responsible_faculty_mit_id"])
    .reset_index(drop=True)
)

# Build a clean set of MIT IDs (as strings for consistent matching)
fac_ids = (
    fac_2023fa["responsible_faculty_mit_id"]
    .dropna()
    .astype("Int64")
    .astype(str)
    .unique()
    .tolist()
)

# ------------------------------------------------------------------------------
# Step 2: Load mailing list membership data if available among provided tables
# Since no mailing list table is listed in `tables`, we will probe all tables
# to see if any could represent mailing list membership by column heuristics.
# ------------------------------------------------------------------------------

def find_mailing_list_table(candidates: dict) -> pd.DataFrame | None:
    # Try each table to see if it looks like a mailing list membership table.
    # Heuristics: should have a subscriber MIT ID-like column, and either a list id or list name column.
    for key, t in candidates.items():
        cols_lower = {c.lower(): c for c in t.columns}
        # Identify subscriber id column
        subscriber_id_col = None
        for opt in ["subscriber_mit_id", "mit_id", "subscriber_id", "person_mit_id"]:
            if opt in cols_lower:
                subscriber_id_col = cols_lower[opt]
                break
        if subscriber_id_col is None:
            # heuristic: any column with 'mit' and 'id'
            for c in t.columns:
                cl = c.lower()
                if "mit" in cl and "id" in cl:
                    subscriber_id_col = c
                    break
        # Identify list id/name
        list_id_col = None
        for opt in ["list_id", "list_key", "mailing_list_id", "list"]:
            if opt in cols_lower:
                list_id_col = cols_lower[opt]
                break
        list_name_col = None
        for opt in ["list_name", "mailing_list_name", "listtitle", "name"]:
            if opt in cols_lower:
                list_name_col = cols_lower[opt]
                break
        # Consider this table a candidate if it has subscriber_id and either list_id or list_name
        if subscriber_id_col is not None and (list_id_col is not None or list_name_col is not None):
            # Return standardized working copy with metadata on detected columns
            work = t.copy()
            meta = {
                "__subscriber_id_col__": subscriber_id_col,
                "__list_id_col__": list_id_col,
                "__list_name_col__": list_name_col,
            }
            for k, v in meta.items():
                work[k] = v
            return work
    return None

ml_df = find_mailing_list_table(tables)

if ml_df is None:
    # No mailing list-like table found; produce empty result as per reference behavior
    filtered_lists = pd.DataFrame(columns=["LIST_ID", "LIST_NAME", "SUBSCRIBER_MIT_ID"])
else:
    # Extract detected column names from embedded meta
    subscriber_id_col = ml_df["__subscriber_id_col__"].iloc[0]
    list_id_col = ml_df["__list_id_col__"].iloc[0]
    list_name_col = ml_df["__list_name_col__"].iloc[0]

    work = ml_df.drop(columns=["__subscriber_id_col__", "__list_id_col__", "__list_name_col__"]).copy()

    # Build normalized columns
    if list_id_col is None:
        work["__LIST_ID__"] = work[list_name_col].astype(str)
    else:
        work["__LIST_ID__"] = work[list_id_col].astype(str)

    if list_name_col is None:
        work["__LIST_NAME__"] = work["__LIST_ID__"]
    else:
        work["__LIST_NAME__"] = work[list_name_col].astype(str)

    sid = work[subscriber_id_col]
    if pd.api.types.is_float_dtype(sid) or pd.api.types.is_integer_dtype(sid):
        work["__SUBSCRIBER_MIT_ID__"] = pd.to_numeric(sid, errors="coerce").astype("Int64").astype(str)
    else:
        work["__SUBSCRIBER_MIT_ID__"] = sid.astype(str).str.strip()

    # Filter lists that have exactly 10 members
    list_sizes = work.groupby("__LIST_ID__")["__SUBSCRIBER_MIT_ID__"].nunique().reset_index(name="member_count")
    lists_size_10 = list_sizes[list_sizes["member_count"] == 10]["__LIST_ID__"]

    work_10 = work[work["__LIST_ID__"].isin(lists_size_10)].copy()

    # Subset to subscriptions where subscriber MIT IDs match 2023FA responsible faculty MIT IDs
    work_10_fac = work_10[work_10["__SUBSCRIBER_MIT_ID__"].isin(fac_ids)].copy()

    filtered_lists = work_10_fac.rename(
        columns={
            "__LIST_ID__": "LIST_ID",
            "__LIST_NAME__": "LIST_NAME",
            "__SUBSCRIBER_MIT_ID__": "SUBSCRIBER_MIT_ID",
        }
    )[["LIST_ID", "LIST_NAME", "SUBSCRIBER_MIT_ID"]].drop_duplicates().reset_index(drop=True)

# ------------------------------------------------------------------------------
# Step 3: For each qualifying list, compute:
# - the number of faculty in these lists (unique subscribers that are in fac_ids)
# - the number of courses associated with those faculty in 2023FA
# ------------------------------------------------------------------------------

# Prepare mapping from faculty MIT ID to number of courses they are responsible for in 2023FA
fac_courses = (
    df_2023fa[["responsible_faculty_mit_id", "SUBJECT_ID"]]
    .dropna(subset=["responsible_faculty_mit_id", "SUBJECT_ID"])
    .assign(
        responsible_faculty_mit_id=lambda x: pd.to_numeric(x["responsible_faculty_mit_id"], errors="coerce").astype("Int64").astype(str),
        SUBJECT_ID=lambda x: x["SUBJECT_ID"].astype(str),
    )
    .drop_duplicates()
)

courses_per_fac = fac_courses.groupby("responsible_faculty_mit_id")["SUBJECT_ID"].nunique().reset_index(name="num_courses_2023FA")

if filtered_lists.empty:
    final = pd.DataFrame(columns=["LIST_ID", "LIST_NAME", "num_faculty_in_list", "num_courses_for_those_faculty"])
else:
    # Count unique faculty subscribers per list
    fac_counts = (
        filtered_lists.groupby(["LIST_ID", "LIST_NAME"])["SUBSCRIBER_MIT_ID"]
        .nunique()
        .reset_index(name="num_faculty_in_list")
    )

    # Join to get per-subscription faculty course counts
    subs_with_courses = (
        filtered_lists.merge(
            courses_per_fac,
            left_on="SUBSCRIBER_MIT_ID",
            right_on="responsible_faculty_mit_id",
            how="left",
        )
    )

    # Sum number of courses across unique faculty in each list.
    # To avoid double-counting a faculty if they appear multiple times for the same list,
    # first deduplicate at (LIST_ID, SUBSCRIBER_MIT_ID).
    subs_unique = subs_with_courses[["LIST_ID", "LIST_NAME", "SUBSCRIBER_MIT_ID", "num_courses_2023FA"]].drop_duplicates()

    courses_sum = (
        subs_unique.groupby(["LIST_ID", "LIST_NAME"])["num_courses_2023FA"]
        .sum(min_count=1)
        .fillna(0)
        .astype(int)
        .reset_index(name="num_courses_for_those_faculty")
    )

    final = (
        fac_counts.merge(courses_sum, on=["LIST_ID", "LIST_NAME"], how="left")
        .sort_values(["LIST_NAME", "LIST_ID"])
        .reset_index(drop=True)
    )

# ------------------------------------------------------------------------------
# Package final result
# ------------------------------------------------------------------------------
result = {
    "mailing_lists_size10_with_2023FA_responsible_faculty": final
}