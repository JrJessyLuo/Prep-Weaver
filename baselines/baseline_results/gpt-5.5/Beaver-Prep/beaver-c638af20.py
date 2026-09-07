import pandas as pd

def _norm(s):
    return s.astype("string").str.strip()

def _clean_label(s):
    return _norm(s).replace("", pd.NA)

def _first_mode(s):
    vals = s.dropna()
    if vals.empty:
        return pd.NA
    m = vals.mode()
    return m.iloc[0] if not m.empty else vals.iloc[0]

# ---------- Subject/deartment lookup ----------
subjects = tables["table_6"].copy()
subjects["_so_key"] = _norm(subjects["TIP_SUBJECT_OFFERED_KEY"])
subjects["_subject_id"] = _norm(subjects["SUBJECT_ID"])
subjects["_term_code"] = _norm(subjects["TERM_CODE"])
subjects["_department_name"] = _clean_label(subjects["OFFER_DEPT_NAME"])

dept_by_so = (
    subjects[
        subjects["_so_key"].notna() & (subjects["_so_key"] != "")
    ][["_so_key", "_department_name"]]
    .dropna(subset=["_department_name"])
    .drop_duplicates("_so_key")
)

dept_by_subject_term = (
    subjects[
        subjects["_subject_id"].notna()
        & (subjects["_subject_id"] != "")
        & subjects["_term_code"].notna()
        & (subjects["_term_code"] != "")
    ]
    .groupby(["_subject_id", "_term_code"], as_index=False)["_department_name"]
    .agg(_first_mode)
    .dropna(subset=["_department_name"])
)

dept_by_subject = (
    subjects[
        subjects["_subject_id"].notna() & (subjects["_subject_id"] != "")
    ]
    .groupby("_subject_id", as_index=False)["_department_name"]
    .agg(_first_mode)
    .dropna(subset=["_department_name"])
)

# ---------- TIP material statuses ----------
tip_status = tables["table_2"].copy()
tip_status["_tip_status_key"] = _norm(tip_status["tip_material_status_key"])
tip_status["_material_status"] = (
    _clean_label(tip_status["TIP_MATERIAL_STATUS"])
    .combine_first(_clean_label(tip_status["TIP_MATERIAL_STATUS_CODE"]))
    .combine_first(_clean_label(tip_status["tip_material_status_key"]))
    .fillna("(blank)")
)
tip_status = tip_status[["_tip_status_key", "_material_status"]].drop_duplicates("_tip_status_key")

# ---------- TIP material counts ----------
tip = tables["table_1"].copy()
tip["_so_key"] = _norm(tip["TIP_SUBJECT_OFFERED_KEY"])
tip["_subject_id"] = _norm(tip["subject_id"])
tip["_term_code"] = _norm(tip["TERM_CODE"])
tip["_tip_status_key"] = _norm(tip["TIP_MATERIAL_STATUS_KEY"])

tip = tip.merge(dept_by_so.rename(columns={"_department_name": "_dept_from_so"}), on="_so_key", how="left")
tip = tip.merge(
    dept_by_subject_term.rename(columns={"_department_name": "_dept_from_subject_term"}),
    on=["_subject_id", "_term_code"],
    how="left",
)
tip = tip.merge(
    dept_by_subject.rename(columns={"_department_name": "_dept_from_subject"}),
    on="_subject_id",
    how="left",
)
tip = tip.merge(tip_status, on="_tip_status_key", how="left")

tip["department_name"] = (
    tip["_dept_from_so"]
    .combine_first(tip["_dept_from_subject_term"])
    .combine_first(tip["_dept_from_subject"])
    .fillna("Unknown Department")
)
tip["material_status"] = (
    tip["_material_status"]
    .combine_first(_clean_label(tip["TIP_MATERIAL_STATUS_KEY"]))
    .fillna("(blank)")
)
tip["tip_material_count"] = pd.to_numeric(tip["RECORD_COUNT"], errors="coerce").fillna(0)

tip_counts = (
    tip.groupby(["department_name", "material_status"], as_index=False)["tip_material_count"]
    .sum()
)

# ---------- Library material statuses ----------
library_status = tables["table_3"].copy()
library_status["_library_status_key"] = _norm(library_status["LIBRARY_MATERIAL_STATUS_KEY"])
library_status["_material_status"] = (
    _clean_label(library_status["LIBRARY_MATERIAL_STATUS"])
    .combine_first(_clean_label(library_status["LIBRARY_MATERIAL_STATUS_CODE"]))
    .combine_first(_clean_label(library_status["LIBRARY_MATERIAL_STATUS_KEY"]))
    .fillna("(blank)")
)
library_status = library_status[["_library_status_key", "_material_status"]].drop_duplicates("_library_status_key")

# ---------- Library material counts ----------
lib = tables["table_4"].copy()
lib["_subject_id"] = _norm(lib["SUBJECT_ID"])
lib["_term_code"] = _norm(lib["TERM_CODE"])
lib["_library_status_key"] = _norm(lib["LIBRARY_MATERIAL_STATUS_KEY"])

lib = lib.merge(
    dept_by_subject_term.rename(columns={"_department_name": "_dept_from_subject_term"}),
    on=["_subject_id", "_term_code"],
    how="left",
)
lib = lib.merge(
    dept_by_subject.rename(columns={"_department_name": "_dept_from_subject"}),
    on="_subject_id",
    how="left",
)
lib = lib.merge(library_status, on="_library_status_key", how="left")

lib["department_name"] = (
    lib["_dept_from_subject_term"]
    .combine_first(lib["_dept_from_subject"])
    .fillna("Unknown Department")
)
lib["material_status"] = (
    lib["_material_status"]
    .combine_first(_clean_label(lib["LIBRARY_MATERIAL_STATUS_KEY"]))
    .fillna("(blank)")
)
lib["library_material_count"] = 1

library_counts = (
    lib.groupby(["department_name", "material_status"], as_index=False)["library_material_count"]
    .sum()
)

# ---------- Combine TIP and library counts ----------
detail = tip_counts.merge(
    library_counts,
    on=["department_name", "material_status"],
    how="outer",
)

detail["tip_material_count"] = detail["tip_material_count"].fillna(0).astype("int64")
detail["library_material_count"] = detail["library_material_count"].fillna(0).astype("int64")
detail["total_material_count"] = detail["tip_material_count"] + detail["library_material_count"]

# ---------- Department subtotals ----------
subtotals = (
    detail.groupby("department_name", as_index=False)[
        ["tip_material_count", "library_material_count", "total_material_count"]
    ]
    .sum()
)
subtotals["material_status"] = "Subtotal"
subtotals = subtotals[
    ["department_name", "material_status", "tip_material_count", "library_material_count", "total_material_count"]
]

# ---------- Grand total ----------
grand_total = pd.DataFrame([{
    "department_name": "Grand Total",
    "material_status": "Grand Total",
    "tip_material_count": int(detail["tip_material_count"].sum()),
    "library_material_count": int(detail["library_material_count"].sum()),
    "total_material_count": int(detail["total_material_count"].sum()),
}])

detail = detail[
    ["department_name", "material_status", "tip_material_count", "library_material_count", "total_material_count"]
]

detail["_row_order"] = 0
subtotals["_row_order"] = 1
grand_total["_row_order"] = 2

answer = pd.concat([detail, subtotals, grand_total], ignore_index=True)
answer = (
    answer.sort_values(
        ["_row_order", "department_name", "material_status"],
        kind="stable",
    )
    .drop(columns="_row_order")
    .reset_index(drop=True)
)

result = {
    "department_material_status_counts": answer
}
