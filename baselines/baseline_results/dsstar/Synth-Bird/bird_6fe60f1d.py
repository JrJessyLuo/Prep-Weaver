import pandas as pd

# Input tables are already loaded in `tables`
demo = tables["table_1"]
labs = tables["table_2"]

# ----------------------------
# 1) Prepare/join: select MCTD patients + labs with PLT
# ----------------------------
def norm_id(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip().strip('"').strip("'")
    s = s.replace(".0", "")  # handle float-looking ids like 14872.0
    digits = "".join(ch for ch in s if ch.isdigit())
    return digits if digits != "" else pd.NA

demo2 = demo.copy()
labs2 = labs.copy()

demo2["ID_norm"] = demo2["ID"].map(norm_id)
labs2["ID_norm"] = labs2["ID"].map(norm_id)

# Filter to MCTD (case-insensitive, as a token within Diagnosis)
demo2["Diagnosis_str"] = demo2["Diagnosis"].astype("string")
mctd_demo = demo2[demo2["Diagnosis_str"].str.contains(r"\bMCTD\b", case=False, na=False)].copy()

# Join MCTD demographics with labs
mctd_labs = mctd_demo.merge(
    labs2,
    on="ID_norm",
    how="inner",
    suffixes=("_demo", "_lab"),
)

# ----------------------------
# 2) Filter to normal PLT and parse dates
# ----------------------------
PLT_LOWER, PLT_UPPER = 150, 400

mctd_labs = mctd_labs.copy()
mctd_labs["PLT"] = pd.to_numeric(mctd_labs["PLT"], errors="coerce")
mctd_labs["Date_parsed"] = pd.to_datetime(mctd_labs["Date"], errors="coerce")

mctd_labs_plt_normal = (
    mctd_labs.dropna(subset=["PLT"])
             .loc[lambda d: d["PLT"].between(PLT_LOWER, PLT_UPPER, inclusive="both")]
             .copy()
)

mctd_labs_plt_normal = mctd_labs_plt_normal.sort_values(
    ["ID_norm", "Date_parsed", "PLT"], ascending=[True, True, True]
)

# ----------------------------
# 3) Final formatted output: choose most recent PLT per patient
# ----------------------------
mctd_most_recent = (
    mctd_labs_plt_normal.sort_values(["ID_norm", "Date_parsed", "PLT"], ascending=[True, True, True])
                        .dropna(subset=["Date_parsed"])
                        .groupby("ID_norm", as_index=False)
                        .tail(1)
                        .sort_values(["ID_norm"])
)

final_out = (
    mctd_most_recent.assign(
        ID=lambda d: d["ID_norm"],
        Date=lambda d: d["Date_parsed"].dt.strftime("%Y-%m-%d"),
        PLT=lambda d: d["PLT"].astype(float),
    )[["ID", "Date", "PLT"]]
    .reset_index(drop=True)
)

# Final answer (per evaluation convention)
result = {"mctd_patients_normal_platelet_most_recent": final_out}